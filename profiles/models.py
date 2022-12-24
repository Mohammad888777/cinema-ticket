from django.db import models
from accounts.models import User

def user_profile_images(instance,filename):

    return f"{instance.user.username}/{filename}"


class Profile(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to=user_profile_images,null=True,blank=True,default="a.png")
    bio=models.CharField(max_length=200,null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    
