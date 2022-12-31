from django.db import models
from movies.models import Movie
from accounts.models import User


class PlayList(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    movies=models.ManyToManyField(Movie,related_name="movies",blank=True)
    

    def __str__(self) -> str:
        return self.user.username


