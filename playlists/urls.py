from django.urls import path
from . import views


urlpatterns=[

    path("addToFav/<str:username>/",views.addToFav,name="addToFav"),
    path("playlists/<str:username>/",views.PlayListMovies.as_view(),name="playlists"),
    
]