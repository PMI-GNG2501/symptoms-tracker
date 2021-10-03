from django.forms import ModelForm
from reminders.models import Reminder


class RemindersForm(ModelForm):
    class Meta:
        model = Reminder
        fields = "__all__"
        required = ("time", "user", "medication")
