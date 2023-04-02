from django import forms
from ecolifestyle.models import VolunteerRequest

class VolunteerRequestForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    class Meta:
        model = VolunteerRequest
        fields = ['name','address']
