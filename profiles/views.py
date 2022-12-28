from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Profile
from accounts.models import User
from .forms import ProfileForm,ChangePassowdForm
from .decorators import needLogin,profileCheck






class ProfileView(LoginRequiredMixin,View):

    def get(self,request,*args,**kwargs):
         
        username=self.kwargs.get("username")
        profile=get_object_or_404(Profile.objects.select_related("user"),user__username=username)

        contex={
            'profile':profile,
            'ProfileForm':ProfileForm(instance=profile),
            'ChangePassowdForm':ChangePassowdForm()
        }

        return render(request,"profiles/myProfile.html",contex)


    
    def post(self,request,*args,**kwargs):

        username=self.kwargs.get("username")
        profile=get_object_or_404(Profile.objects.select_related("user"),user__username=username)
        form=ProfileForm(self.request.POST,self.request.FILES,instance=profile)
        changeForm=ChangePassowdForm(self.request.POST)


        if form.is_valid() and changeForm.is_valid():
            update=form.save(commit=False)
            update.user=self.request.user
            update.save()
            messages.success(request,"Your Profile Is Updated Now")
            return redirect(self.request.META.get("HTTP_REFERER"))

        # messages.error(request,"Your Form Is Invalid")
        # return redirect(self.request.META.get("HTTP_REFERER"))

        # if changeForm.is_valid():

        #     if newPassword == newPassword2:
        #     if user.check_password(oldPassword):
        #         user.set_password(newPassword)
        #         user.save()
        #         messages.success(request,"New Password Is Set Now")
        #         return redirect("login")
        #     messages.error(request,"current password is incorrect")
        #     return redirect(request.META.get("HTTP_REFERER"))

        messages.error(request,"Your Form Is Invalid")
        return redirect(self.request.META.get("HTTP_REFERER"))




    def dispatch(self, request, *args, **kwargs):

        username=self.kwargs.get("username")
        profile=get_object_or_404(Profile.objects.select_related("user"),user__username=username)
        

        if self.request.user.is_authenticated and self.request.user.is_active:
            if self.request.user == profile.user:
                return super().dispatch(request, *args, **kwargs)
            return redirect("login")

        return redirect("login")
    




@needLogin
@profileCheck
def updatePassword(request,username):

    profile=get_object_or_404(Profile.objects.select_related("user"),user__username=username)
    user=get_object_or_404(User.objects.select_related("profile"),username=profile.user.username)
    if request.method=="POST":
        oldPassword=request.POST.get("oldPassword")
        newPassword=request.POST.get("newPassword")
        newPassword2=request.POST.get("newPassword2")
        if newPassword == newPassword2:
            if user.check_password(oldPassword):
                user.set_password(newPassword)
                user.save()
                print("DONEEEEEEEEEEEEEEEEEE")
                print("DONEEEEEEEEEEEEEEEEEE")
                print("DONEEEEEEEEEEEEEEEEEE")
                print("DONEEEEEEEEEEEEEEEEEE")
                print("DONEEEEEEEEEEEEEEEEEE")
                messages.success(request,"New Password Is Set Now")
                return redirect("login")
            messages.error(request,"current password is incorrect")
            return redirect(request.META.get("HTTP_REFERER"))

        messages.error(request,"your new password is not match")
        return redirect(request.META.get("HTTP_REFERER"))

    return
                



    