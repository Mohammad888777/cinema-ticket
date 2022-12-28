from django.db import models
from accounts.models import User

def user_profile_images(instance,filename):

    return f"{instance.user.username}/{filename}"


class Profile(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to=user_profile_images,null=True,blank=True,default="a.png")
    bio=models.CharField(max_length=200,null=True)
    username=models.CharField(max_length=200,null=True)
    country=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    first_name=models.CharField(max_length=200,null=True)
    last_name=models.CharField(max_length=200,null=True)
    email=models.EmailField(max_length=200,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.username
    
