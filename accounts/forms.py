from django import forms
from .models import User

class SignupForm(forms.Form):

    username=forms.CharField(required=True,label='',widget=forms.TextInput(attrs={
        "placeholder":"username",
        "class":"input"
    }))

    email=forms.EmailField(max_length=200,required=True,label='',widget=forms.EmailInput(attrs={
        "placeholder":"email",
        "class":"input"
    }))

    password=forms.CharField(required=True,label='',widget=forms.PasswordInput(attrs={
        "placeholder":"password",
        "class":"input"
    }))

    password2=forms.CharField(required=True,label='',widget=forms.PasswordInput(attrs={
        "placeholder":"confirm password",
        "class":"input",
       
    }))


    def clean(self) :

        clean_data= super().clean()
        password=clean_data.get("password")
        password2=clean_data.get("password2")
        if password!=password2:
            raise forms.ValidationError("not match password")
        return clean_data