from accounts.models import User
from .models import Profile
from django.db.models.signals import post_save


def auto_create(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(
            user=instance
        )

post_save.connect(auto_create,sender=User)
