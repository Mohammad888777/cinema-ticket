from django.contrib import admin
from .models import (
    Movie,Seat,Genres,Day,Time,Tag,MovieImage,MovieVideo,Actor,CompanySponser,Role
)

admin.site.register([Seat,Genres,Day,Time,Tag,MovieImage,MovieVideo,Actor,CompanySponser,Role])


class MovieAdmin(admin.ModelAdmin):
    list_display=["name","is_parent2"]


admin.site.register(Movie,MovieAdmin)
