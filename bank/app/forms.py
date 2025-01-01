from django import forms
from .models import Bank
from django_recaptcha.fields import ReCaptchaField

class Bankform(forms.ModelForm):
    recaptcha = ReCaptchaField()
    class Meta:
        model = Bank
        # fields = "__all__"
        fields = ['name','email','phone','address','image']