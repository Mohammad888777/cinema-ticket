from django.urls import path
from . import views


urlpatterns=[

    path("addToFav/<str:username>/<str:movie_id>/",views.addToFav,name="addToFav"),
    path("Favsplaylists/<str:username>/",views.PlayListMovies.as_view(),name="playlists"),
    path("ratedMovies/<str:username>/",views.RatedMovies.as_view(),name="ratedMovies"),
    
]