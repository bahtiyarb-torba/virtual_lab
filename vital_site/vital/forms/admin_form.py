from django.forms import ModelForm, TextInput
from django import forms
from ..models import Admin_Network_Configuration
from captcha.fields import CaptchaField
from passwords.fields import PasswordField

class Network_creation_Form(ModelForm):
    subnet_start = forms.IntegerField(widget=forms.widgets.NumberInput,label='Start')
    subnet_end = forms.IntegerField(widget=forms.widgets.NumberInput,label='End')
    networks_per_user = forms.IntegerField(widget=forms.widgets.NumberInput,label='Networks per user')

    class Meta:
        model = Admin_Network_Configuration
        fields = ['subnet_start', 'subnet_end','networks_per_user']

class Course_Details_Form(forms.Form):
    course_number = forms.CharField(widget=forms.widgets.TextInput)
    course_name = forms.CharField(widget=forms.widgets.TextInput)

    class Meta:
        fields = ['course_number', 'course_name']

