from django.shortcuts import render,redirect,get_object_or_404
from .models import User
from django.urls import reverse 
from django.views import View
from .forms import SignupForm
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts  import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from profiles.models import Profile




def register(request):

    if request.method=="POST":
        form=SignupForm(request.POST)

        if form.is_valid():
                username=form.cleaned_data.get("username")
                password=form.cleaned_data.get("password")
                email=form.cleaned_data.get("email")
                to_auth=User.objects.filter(email=email).exists()
                if not to_auth:
                    if not User.objects.filter(username=username).exists():
                        user=User.objects.create_user(
                            first_name='...',last_name='...',username=username,password=password,
                            email=email
                        )
                        current_site=get_current_site(request)
                        subject="activate your account"
                        body=render_to_string("accounts/avtivateAccount.html",{
                            "domin":current_site,
                            "user":user,
                            "uid":urlsafe_base64_encode(force_bytes(user.id)),
                            "token":default_token_generator.make_token(user)
                        })
                        mail=EmailMessage(subject=subject,body=body,to=[email])
                        mail.send()
                        messages.success(request,"we sent you email please acivate your account")
                        return redirect("login")
                    messages.error(request,"username already exists")
                    return redirect("register")
                messages.error(request,"email already exists")
                return redirect("register")
    else:
        contex={
            'form':SignupForm()
        }

        return render(request,"accounts/register.html",contex)


            
def activate(request,uidb64,token):

    try:
        uid=urlsafe_base64_decode(uidb64)
        user=User._default_manager.get(pk=uid)
    except User.DoesNotExist:
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"your account is verfied successfully")
        return redirect("movies")
    else:
        messages.error(request,"your activation code is incorrect send again")
        return redirect("register")

 

def loginView(request):

    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        try:
            user=User.objects.get(username=username.lower())
        except User.DoesNotExist:
            user=None
        if user:
            auth=authenticate(email=user.email,password=password)
            if auth is not None:
                print("Weeeeeeeee")
                print("Weeeeeeeee")
                print("Weeeeeeeee")
                print("Weeeeeeeee")
                print("Weeeeeeeee")
                login(request,auth)
                return redirect("movies")
                

            else:
                messages.error(request,"user does not found")
                return redirect("login")
        else:
            messages.error(request,"username or password is invalid")
            return redirect("login")

    

    return render(request,"accounts/login.html")



def logoutView(request):
    logout(request)
    return redirect("movies")