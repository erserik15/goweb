from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username','email','password']
