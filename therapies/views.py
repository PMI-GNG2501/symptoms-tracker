from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from therapies.models import Therapies
from therapies.forms import TherapiesForm


@login_required
def index(request):
    therapies = Therapies.objects.all().filter(user_id=request.user.id)
    return render(request, "therapies/index.html", {"therapies": therapies})


@login_required
def new(request):
    if request.method == "POST":
        updated_form = request.POST.copy()
        updated_form.update({"user": request.user})
        form = TherapiesForm(updated_form)
        if form.is_valid():
            try:
                form.save()
                return redirect("/therapies")
            except Exception as e:
                print(e)
                print("error")
    return render(request, "therapies/new.html")


@login_required
def edit(request, id):
    therapy = Therapies.objects.get(id=id)
    return render(
        request,
        "therapies/edit.html",
        {
            "therapy": therapy,
        },
    )


@login_required
def update(request, id):
    therapy = Therapies.objects.get(id=id)
    updated_form = request.POST.copy()
    updated_form.update({"user": therapy.user})
    form = TherapiesForm(updated_form, instance=therapy)
    if form.is_valid():
        form.save()
        return redirect("/therapies")
    return render(
        request,
        "therapies/edit.html",
        {
            "therapy": therapy,
        },
    )


@login_required
def destroy(request, id):
    therapy = Therapies.objects.get(id=id)
    therapy.delete()
    return redirect("/therapies")
