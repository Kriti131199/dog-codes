from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class FilterForm(forms.Form):
    filter_input = forms.CharField(label='Filter (e.g. 2xx, 203, 20x)', max_length=10)
    list_name = forms.CharField(label='List Name', max_length=100)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)