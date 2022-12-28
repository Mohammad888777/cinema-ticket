from django.shortcuts import redirect,get_object_or_404
from django.http import Http404
from functools import wraps
from .models import Profile



def needLogin(func):
    @wraps(func)
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        return redirect("login")
    return inner




def profileCheck(func):
    @wraps(func)
    def inner(request,username,*args,**kwargs):
        profile=get_object_or_404(Profile,user__username=username)
        if request.user.is_authenticated:
            if request.user==profile.user:
                return func(request,username,*args,**kwargs)
            return redirect("myProfile",request.user.username)
        return redirect("login")
    return inner


