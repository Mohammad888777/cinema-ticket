from django.shortcuts import render,redirect,get_object_or_404
from movies.models import Movie
from .models import PlayList
from profiles.decorators import needLogin,profileCheck
from profiles.models import Profile
from django.http import JsonResponse
from django.db.models import Q,Avg
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User



@needLogin
def addToFav(request,username,movie_id):

    movie=get_object_or_404(Movie.objects.select_related(
        "parent","sponsor"
    ).prefetch_related(
        "genre","tag","days","times","booked_seats"
    ).annotate(
        avg=Avg("comment__rating")
    ),pk=movie_id)
    stars=[]
    for ac in movie.actors.all():
        if ac.is_star==True:
            stars.append(ac)
        

    profile=get_object_or_404(Profile.objects.select_related("user"),user__username=username)

    playlist=PlayList.objects.select_related("user").prefetch_related("movies"). get(user=profile.user)
    playlist.movies.add(movie)
    playlist.save()

    movieInfo=[
        {
            "movieId":movie.id,
            "movieName":movie.name,
            "movieRate":movie.avg,
            "director":movie.director,
            "stars":stars,
            "movieDescription":movie.description,
            "ageCanSee":movie.ageCanSee,
            "year_made":movie.year_made,
            "movie_time":movie.movie_time

        }
    ]

    return JsonResponse(movieInfo,safe=False)
    




    
class PlayListMovies(LoginRequiredMixin,View):

    def get(self,request,username,*args,**kwargs):

        user=get_object_or_404(User.objects.select_related("profile"),username=username)

        playLists=PlayList.objects.select_related("user").prefetch_related("movies").filter(
            user=user
        )

        xx=[]
        for p in playLists:
            for movie  in p.movies.all():
                xx.append(movie)
        




        profile=get_object_or_404(Profile.objects.select_related("user"),user=user)
        contex={
            'playLists':playLists,
            'playListsLen':len(xx),
            'profile':profile,
            'movies':xx
            
        }

        return render(request,"profiles/playlist.html",contex)

    