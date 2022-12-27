from django.urls import path
from . import views

urlpatterns=[

    path("",views.movieList,name="movies"),
    path("allMovies",views.AllMoviesView.as_view(),name="allMovies"),
    path("allListMovies",views.AllListMoviesView.as_view(),name="allListMovies"),
    path("movieDetail/<str:movie_id>/",views.MovieDetail.as_view(),name="movieDetail"),
    # path("movieDetail/<str:movie_id>/<str:page>/",views.MovieDetail.as_view(),name="movieDetail"),

    # path("relatedReviewView/<str:movie_id>/",views.relatedReviewView,name="relatedReviewView"),

    
]