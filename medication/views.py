from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from medication.models import Medication
from medication.forms import MedicationForm


@login_required
def index(request):
    medications = Medication.objects.all()
    return render(request, "medication/index.html", {"medications": medications})


@login_required
def new(request):
    if request.method == "POST":
        form = MedicationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect("/medication/")
            except Exception as e:
                print(e)
                print("error")
    return render(request, "medication/new.html")


@login_required
def edit(request, id):
    medication = Medication.objects.get(id=id)
    return render(request, "medication/edit.html", {"medication": medication})


@login_required
def update(request, id):
    medication = Medication.objects.get(id=id)
    form = MedicationForm(request.POST, instance=medication)
    if form.is_valid():
        form.save()
        return redirect("/medication")
    return render(request, "medication/edit.html", {"medication": medication})


@login_required
def destroy(request, id):
    medication = Medication.objects.get(id=id)
    medication.delete()
    return redirect("/medication")
