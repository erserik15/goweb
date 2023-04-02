from django import forms
from ecolifestyle.models import Post

class PostForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    class Meta:
        model = Post
        fields = ['name','address']
