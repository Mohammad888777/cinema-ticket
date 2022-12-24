from django.urls import path
from . import views

urlpatterns=[

    path("",views.movieList,name="movies"),
    path("movieDetail/<str:movie_id>/",views.MovieDetail.as_view(),name="movieDetail"),
    
]