from django.forms import ModelForm
from medication_log.models import MedicationLog


class MedicationLogForm(ModelForm):
    class Meta:
        model = MedicationLog
        fields = "__all__"
        required = ("user", "medication")
