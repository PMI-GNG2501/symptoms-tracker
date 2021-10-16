from django.forms import ModelForm
from therapies.models import Therapies


class TherapiesForm(ModelForm):
    class Meta:
        model = Therapies
        fields = "__all__"
        required = ("datetime", "name", "user")
