from django.urls import path
from . import views

urlpatterns=[

    path("",views.movieList,name="movies"),
    path("afterPay/",views.afterPaid,name="afterPay"),


    path("selectSeat/<str:movie_id>/",views.selectSeat,name="selectSeat"),
    # path("SeatsView/<str:movie_id>/",views.SeatsView,name="SeatsView"),




    path("allMovies",views.AllMoviesView.as_view(),name="allMovies"),
    path("allMoviesSearch",views.AllMovieSearch.as_view(),name="allMoviesSearch"),



    path("allListMovies",views.AllListMoviesView.as_view(),name="allListMovies"),
    path("allListMoviesSearch",views.AllListMoviesSearch.as_view(),name="allListMoviesSearch"),




    path("movieDetail/<str:movie_id>/",views.MovieDetail.as_view(),name="movieDetail"),

    path("moiveSeats/<str:movie_id>/",views.SeatsView,name="moiveSeats"),



    path("makeOrder/",views.makeOrder,name="makeOrder"),
    path("myOrder/<str:username>/",views.myOrder,name="myOrder"),

]