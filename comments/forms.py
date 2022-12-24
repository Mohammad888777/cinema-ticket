from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    body=forms.CharField(required=False,label='',widget=forms.TextInput(attrs={
        "placeholder":"add comment",
        'rows':4
        
    }))

    class Meta:
        model=Comment
        fields=["body","rating"]