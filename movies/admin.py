from django.contrib import admin
from .models import (
    Movie,Seat,Genres,Day,Time,Tag,
    MovieImage,MovieVideo,Actor,
    CompanySponser,Role,
    Order
    
)
from django.db.models import Avg
from comments.models import Comment

admin.site.register([Genres,Day,Time,Tag,MovieImage,MovieVideo,Actor,CompanySponser,Role,Order])


class MovieAdmin(admin.ModelAdmin):
    list_display=["name","is_parent2","year_made","avg","genres_are"]

    def avg(self,obj):
        return Comment.objects.filter(
            movie=obj
        ).aggregate(avg=Avg("rating"))
    
    def genres_are(self,obj):
        return [i.genres_name for i in obj.genre.all() ]


class AdminSeat(admin.ModelAdmin):
    list_display=["movie","number","seat_status"]

admin.site.register(Seat,AdminSeat)


admin.site.register(Movie,MovieAdmin)
