from django.db.models.signals import post_save
from .models import PlayList
from accounts.models import User


def autoCreate(sender,instance,created,**kwargs):
    if created:
        PlayList.objects.create(
            user=instance
        )
    
post_save.connect(autoCreate,sender=User)