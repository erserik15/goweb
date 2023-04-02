from django import forms
from ecolifestyle.models import Event

class EventForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    class Meta:
        model = Event
        fields = ['name','address']
