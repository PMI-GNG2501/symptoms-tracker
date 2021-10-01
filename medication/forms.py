from django.forms import ModelForm
from medication.models import Medication


class MedicationForm(ModelForm):
    class Meta:
        model = Medication
        fields = "__all__"
        required = ('name', 'user')