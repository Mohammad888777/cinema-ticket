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
import json
from movies.utils import handle_paginnator
from django.db.models import Avg
from comments.models import Comment
from django.views.generic import ListView





@needLogin
def addToFav(request,username,movie_id):

    movie=get_object_or_404(Movie.objects.select_related(
        "parent","sponsor"
    ).prefetch_related(
        "genre","tag","days"
    ).annotate(
        avg=Avg("comment__rating")
    ),pk=movie_id)
    stars=[]
    for ac in movie.actors.all():
        if ac.is_star==True:
            stars.append(ac.actor_name)
        

    profile=get_object_or_404(Profile.objects.select_related("user"),user__username=username)

    playlist=PlayList.objects.select_related("user").prefetch_related("movies"). get(user=profile.user)

    is_added_or_not=False

    if movie in playlist.movies.all():
        playlist.movies.remove(movie)
        is_added_or_not=False
    else:
        playlist.movies.add(movie)
        is_added_or_not=True

    playlist.save()

    if request.is_ajax():
        return JsonResponse({"is_added_or_not":is_added_or_not})
    return redirect(request.META.get("HTTP_REFERER"))

    




    
class PlayListMovies(LoginRequiredMixin,View):


    def get(self,request,username,*args,**kwargs):

        page=self.request.GET.get("page",1)
        perPage=self.request.GET.get("perPage",2)

        
        profile=get_object_or_404(Profile.objects.select_related("user"),user__username=username)


        playLists=PlayList.objects.select_related("user").prefetch_related("movies").filter(
            user=profile.user
        )
    
        xx=[]
        for p in playLists:
            for movie  in p.movies.all().annotate(avg=Avg("comment__rating")):
                xx.append(movie)
        
        res=handle_paginnator(xx,perPage,page)


        contex={
            'playLists':playLists,
            'playListsLen':len(xx),
            'profile':profile,
            'movies':res,
            "perPage":perPage,
        }

        return render(request,"profiles/playlist.html",contex)
    
    def dispatch(self, request, *args, **kwargs) :

        username=self.kwargs.get("username")

        profile=Profile.objects.get(user__username=username)

        if self.request.user.is_authenticated:
            if self.request.user ==profile.user:
                return super().dispatch(request, *args, **kwargs)
            return redirect("myProfile",self.request.user)
        return redirect("login")








class RatedMovies(LoginRequiredMixin,ListView):
    
    template_name: str="profiles/ratedMovie.html"

    def get_queryset(self):
        username=self.kwargs.get("username")

        profile=Profile.objects.get(user__username=username)
        comments=Comment.objects.select_related("movie","user").filter(
            user=profile.user
        )

        return comments

        
    def get_context_data(self, **kwargs) :

        username=self.kwargs.get("username")
        profile=Profile.objects.get(user__username=username)

        contex= super().get_context_data(**kwargs)

        contex["profile"]=profile

        return contex
    
    def dispatch(self, request, *args, **kwargs) :

        username=self.kwargs.get("username")

        profile=Profile.objects.get(user__username=username)

        if self.request.user.is_authenticated:
            if self.request.user ==profile.user:
                return super().dispatch(request, *args, **kwargs)
            return redirect("myProfile",self.request.user)
        return redirect("login")
    
        
