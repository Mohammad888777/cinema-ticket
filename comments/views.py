from django.shortcuts import render,redirect,get_object_or_404
from .models import Comment
from movies.models import Movie
from accounts.models import User
from django.http import JsonResponse
from .forms import CommentForm

def addComment(request,movie_id):

    movie=get_object_or_404(Movie.objects.select_related(
        "parent","genre","sponsor"
    ).prefetch_related(
        "tag","days","booked_seats","times","actors","comment_set"
    ),id=movie_id)

    if request.method=="POST":
        print("POSTTT")

        body=request.POST.get("body")
        new_comment=Comment(
            user=request.user,body=body,movie=movie,
        )

        x=[]
        x.append({
            "body":new_comment.body,
            "username":new_comment.user.username,
            "movieId":new_comment.movie.id,
            "imageProfile":new_comment.user.profile.image.url,
            "created":new_comment.created
        })
        if request.is_ajax():
            return JsonResponse(x,safe=False)
        return redirect("movieDetail",movie.id)
    print('NOt POST')
    print('NOt POST')
    print('NOt POST')
    print('NOt POST')
    print('NOt POST')
    print('NOt POST')
    print('NOt POST')
    print('NOt POST')
    print('NOt POST')
    print('NOt POST')
    print('NOt POST')
    print('NOt POST')
    print('NOt POST')
    print('NOt POST')
    print('NOt POST')
    return render(request,"movies/moviesingle.html",{"form":CommentForm()})
        

    
        
