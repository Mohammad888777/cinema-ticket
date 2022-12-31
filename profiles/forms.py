from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):

    username=forms.CharField(required=False,label='',)
    email=forms.EmailField(required=True,label='')
    first_name=forms.CharField(required=False,label='',)
    last_name=forms.CharField(required=False,label='',)
    country=forms.CharField(required=False,label='',)
    state=forms.CharField(required=False,label='',)
    image=forms.ImageField(required=False,label='')

    class Meta:

        model=Profile
        fields=["username","email","first_name","last_name","country","state","image"]


class ChangePassowdForm(forms.Form):

    oldPassword=forms.CharField(required=False,label='',widget=forms.PasswordInput(attrs={
        "placeholder":"current password",
    }))

    newPassword=forms.CharField(required=False,label='',widget=forms.PasswordInput(attrs={
        "placeholder":"new password",
    }))

    confirmPassword=forms.CharField(required=False,label='',widget=forms.PasswordInput(attrs={
        "placeholder":"confirm password",
    }))



