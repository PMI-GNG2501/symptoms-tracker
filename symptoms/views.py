from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string

from weasyprint import HTML
from datetime import datetime, timedelta

from medication.models import Medication
from symptoms.models import Symptoms
from symptoms.forms import SymptomsForm


@login_required
def index(request):
    symptoms = Symptoms.objects.all().filter(user_id=request.user.id)
    return render(request, "symptoms/index.html", {"symptoms": symptoms})


@login_required
def new(request):
    if request.method == "POST":
        updated_form = request.POST.copy()
        updated_form.update({"user": request.user, "datetime": datetime.now()})
        form = SymptomsForm(updated_form)
        if form.is_valid():
            try:
                form.save()
                return redirect("/symptoms")
            except Exception as e:
                print(e)
                print("error")
    medications = Medication.objects.all().filter(user=request.user)
    return render(request, "symptoms/new.html", {"medications": medications})


@login_required
def edit(request, id):
    symptom = Symptoms.objects.get(id=id)
    medications = Medication.objects.all().filter(user=request.user)
    medication_list = symptom.medication.all().values_list("id", flat=True)
    return render(
        request,
        "symptoms/edit.html",
        {
            "symptom": symptom,
            "medications": medications,
            "medication_list": medication_list,
        },
    )


@login_required
def update(request, id):
    symptom = Symptoms.objects.get(id=id)
    updated_form = request.POST.copy()
    updated_form.update({"user": symptom.user, "datetime": symptom.datetime})
    form = SymptomsForm(updated_form, instance=symptom)
    if form.is_valid():
        form.save()
        return redirect("/symptoms")
    medications = Medication.objects.all().filter(user=request.user)
    medication_list = symptom.medication.all().values_list("id", flat=True)
    return render(
        request,
        "symptoms/edit.html",
        {
            "symptom": symptom,
            "medications": medications,
            "medication_list": medication_list,
        },
    )


@login_required
def destroy(request, id):
    symptoms = Symptoms.objects.get(id=id)
    symptoms.delete()
    return redirect("/symptoms")


def generate_pdf(request):
    symptoms = Symptoms.objects.all().filter(user_id=request.user.id).filter(created_at__range=(datetime.today() - timedelta(days=30), datetime.today() + timedelta(days=1)))

    html_string = render_to_string('pdf/symptoms_summary.html', {'symptoms': symptoms, 'name': request.user.name})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/symptoms_summary.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('symptoms_summary.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="symptoms_summary.pdf"'
        return response

    return response