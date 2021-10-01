from django.forms import ModelForm
from symptoms.models import Symptoms


class SymptomsForm(ModelForm):
    class Meta:
        model = Symptoms
        fields = "__all__"
        required = ("datetime", "user")
