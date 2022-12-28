from django.urls import path
from . import views

urlpatterns=[

    path("",views.movieList,name="movies"),


    path("allMovies",views.AllMoviesView.as_view(),name="allMovies"),
    path("allMoviesSearch",views.AllMovieSearch.as_view(),name="allMoviesSearch"),



    path("allListMovies",views.AllListMoviesView.as_view(),name="allListMovies"),
    path("allListMoviesSearch",views.AllListMoviesSearch.as_view(),name="allListMoviesSearch"),




    path("movieDetail/<str:movie_id>/",views.MovieDetail.as_view(),name="movieDetail"),

    
]