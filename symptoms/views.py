from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from medication.models import Medication
from symptoms.models import Symptoms
from symptoms.forms import SymptomsForm


@login_required
def index(request):
    symptoms = Symptoms.objects.all()
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
