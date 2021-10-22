from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from medication.models import Medication
from medication_log.models import MedicationLog
from medication_log.forms import MedicationLogForm


@login_required
def index(request):
    medication_logs = MedicationLog.objects.all().filter(user_id=request.user.id)
    return render(request, "medication_log/index.html", {"medication_logs": medication_logs})


@login_required
def new(request):
    if request.method == "POST":
        form = MedicationLogForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect("/medication_log/")
            except Exception as e:
                print(e)
                print("error")
    medications = Medication.objects.all().filter(user=request.user)
    return render(request, "medication_log/new.html", {"medications": medications, "datetime": datetime.now()})


@login_required
def edit(request, id):
    medication_log = Medication.objects.get(id=id)
    return render(request, "medication_log/edit.html", {"medication_log": medication_log})


@login_required
def update(request, id):
    medication_log = Medication.objects.get(id=id)
    form = MedicationLogForm(request.POST, instance=medication_log)
    if form.is_valid():
        form.save()
        return redirect("/medication")
    return render(request, "medication_log/edit.html", {"medication_log": medication_log})


@login_required
def destroy(request, id):
    medication_log = MedicationLog.objects.get(id=id)
    medication_log.delete()
    return redirect("/medication_log")
