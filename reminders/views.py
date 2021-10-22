import os
from django.http import JsonResponse
from datetime import timedelta, date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import timezone, datetime, timedelta
import django_rq
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from medication.models import Medication
from medication_log.models import MedicationLog
from reminders.models import Reminder
from reminders.forms import RemindersForm
from therapies.models import Therapies

scheduler = django_rq.get_scheduler(os.getenv("REDIS_QUEUE", "high"))


@login_required
def index(request):
    reminders = Reminder.objects.all().filter(user_id=request.user.id)
    return render(request, "reminders/index.html", {"reminders": reminders})


@login_required
def new(request):
    if request.method == "POST":
        updated_form = request.POST.copy()
        updated_form.update({"user": request.user, "scheduler_id": "0"})
        form = RemindersForm(updated_form)
        if form.is_valid():
            try:
                saved_reminder = form.save()
                job_id = setup_scheduler(updated_form.get("time"), saved_reminder.id)
                Reminder.objects.filter(id=saved_reminder.id).update(
                    scheduler_id=job_id
                )
                return redirect("/reminders")
            except Exception as e:
                print(e)
                print("error")
    medications = Medication.objects.all().filter(user=request.user)
    return render(request, "reminders/new.html", {"medications": medications})


@login_required
def edit(request, id):
    reminder = Reminder.objects.get(id=id)
    medications = Medication.objects.all().filter(user=request.user)
    medication_list = reminder.medication.all().values_list("id", flat=True)
    return render(
        request,
        "reminders/edit.html",
        {
            "reminder": reminder,
            "medications": medications,
            "medication_list": medication_list,
        },
    )


@login_required
def update(request, id):
    reminder = Reminder.objects.get(id=id)
    updated_form = request.POST.copy()
    scheduler.cancel(reminder.scheduler_id)
    job_id = setup_scheduler(updated_form.get("time"), id)
    updated_form.update({"user": reminder.user, "scheduler_id": job_id})
    form = RemindersForm(updated_form, instance=reminder)
    if form.is_valid():
        form.save()
        return redirect("/reminders")
    medications = Medication.objects.all().filter(user=request.user)
    medication_list = reminder.medication.all().values_list("id", flat=True)
    return render(
        request,
        "reminders/edit.html",
        {
            "reminder": reminder,
            "medications": medications,
            "medication_list": medication_list,
        },
    )


@login_required
def destroy(request, id):
    reminder = Reminder.objects.get(id=id)
    reminder.delete()
    return redirect("/reminders")


@login_required
def calendar(request):
    return render(
        request,
        "reminders/calendar.html",
    )


@login_required
def calendar_info(request):
    events = []

    # Medication to take
    reminders = Reminder.objects.all().filter(user_id=request.user.id)
    for reminder in reminders:
        event = {}
        medication_list = list(reminder.medication.all().values_list("name", flat=True))
        event['title'] = "Take " + ', '.join(str(p) for p in medication_list)
        event['daysOfWeek'] = [0, 1, 2, 3, 4, 5, 6]
        event['startTime'] = reminder.time.strftime("%H:%M:%S")
        event['endTime'] = (datetime.combine(date.today(), reminder.time) + timedelta(minutes=15)).strftime("%H:%M:%S")
        events.append(event)

    # Therapy
    therapies = Therapies.objects.all().filter(user_id=request.user.id)
    for therapy in therapies:
        event = {}
        event['title'] = therapy.name
        event['start'] = therapy.datetime.strftime("%Y-%m-%dT%H:%M:%S")
        event['end'] = (therapy.datetime + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
        events.append(event)

    return JsonResponse(events, safe=False)


def setup_scheduler(time, reminder_id):
    local_datetime = datetime.strptime(time, "%H:%M")

    time = datetime.now().replace(
        hour=local_datetime.hour, minute=local_datetime.minute, second=0, microsecond=0
    )

    if datetime.now() > time:
        time = time + timedelta(days=1)

    utc_time = time.astimezone(timezone.utc)

    job = scheduler.schedule(
        scheduled_time=utc_time,  # Time for first execution, in UTC timezone
        func=send_reminder,  # Function to be queued
        kwargs={
            "reminder_id": reminder_id
        },  # Keyword arguments passed into function when executed
        interval=60 * 60 * 24,  # Time before the function is called again, in seconds
        repeat=None,  # Repeat this number of times (None means repeat forever)
    )
    return job.id


def send_reminder(reminder_id: int):
    from django.core.mail import send_mail

    reminder = Reminder.objects.get(id=reminder_id)
    medication_log = MedicationLog(user=reminder.user, datetime=datetime.now())
    medication_log.save()
    medication_log.medication.add(*reminder.medication.all())

    html_message = render_to_string('emails/medication_reminder.html', {'user': reminder.user, 'medications': reminder.medication.all})
    plain_message = strip_tags(html_message)

    send_mail(
        "Take your medications",
        plain_message,
        "afeti047@uottawa.ca",
        [reminder.user.email],
        fail_silently=False,
    )
