from django.shortcuts import render,redirect,get_object_or_404
from .models import Movie
from django.views.generic import ListView,DetailView
from django.http import JsonResponse
from django.db.models import Q,Avg
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q,Avg,Count
# from star_ratings.models import Rating
from comments.models import Comment
from comments.forms import CommentForm
from django.views import View
from django.db.models import Q,Avg,Count
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from accounts.forms import SignupForm
from accounts.models import User
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts  import get_current_site
from django.template.loader import render_to_string




def movieList(request):

    movies=Movie.objects.select_related("genre"). prefetch_related("tag","days","times","booked_seats"
        ) .all().order_by("-timeAdded")
    
    contex={
        'object_list':movies
    }
    if request.method=="POST":

        form=SignupForm(request.POST)

        if form.is_valid():
                username=form.cleaned_data.get("username")
                password=form.cleaned_data.get("password")
                email=form.cleaned_data.get("email")
                to_auth=User.objects.filter(email=email).exists()
                if not to_auth:
                    if not User.objects.filter(username=username).exists():
                        user=User.objects.create_user(
                            first_name='...',last_name='...',username=username,password=password,
                            email=email
                        )
                        current_site=get_current_site(request)
                        subject="activate your account"
                        body=render_to_string("accounts/avtivateAccount.html",{
                            "domin":current_site,
                            "user":user,
                            "uid":urlsafe_base64_encode(force_bytes(user.id)),
                            "token":default_token_generator.make_token(user)
                        })
                        mail=EmailMessage(subject=subject,body=body,to=[email])
                        mail.send()
                        messages.success(request,"we sent you email please acivate your account")
                        return redirect("login")
                    messages.error(request,"username already exists")
                    return redirect("register")
                messages.error(request,"email already exists")
                return redirect("register")



    return render(request,"movies/index.html",contex)




# class MoviesList(ListView):

#     template_name: str="movies/index.html"

#     def get_queryset(self) :

#         return Movie.objects.select_related("genre"). prefetch_related("tag","days","times","booked_seats"
#         ) .all().order_by("-timeAdded")
    
#     def get_context_data(self, **kwargs) :

#         movies=Movie.objects.select_related("genre"). prefetch_related("tag","days","times","booked_seats"
#         ).all()
#         filtered=[i for i in movies if i.is_parent==True]
#         print(filtered)

    
#         return super().get_context_data(**kwargs)



class  MovieDetail(View):

    def get(self,request,movie_id,*args,**kwargs):

    
        movie=Movie.objects.select_related("genre"). prefetch_related("tag","days","times","booked_seats"
        ).get(pk=movie_id)

        # content_id=ContentType.objects.get(app_label="movies",model="movie")
        

        movie=Movie.objects.select_related("genre"). prefetch_related("tag","days","times","booked_seats"
        ).get(pk=movie_id)

        # comments=Comment.objects.select_related('movie','user').filter(
        #     movie=movie
        # )
            
        movieImages=None
        if movie.movieimage_set.all():

            movieImages=movie.movieimage_set.all()[:3]
        movieVideos=None
        if movie.movievideo_set.all():
            movieVideos=movie.movievideo_set.all()[:1]

        comments=None
        avg=0

        if movie.comment_set.all():
            comments=Comment.objects.select_related("user","movie",).prefetch_related("tags") .filter(
                movie=movie
            )
        
        findAvg=Comment.objects.select_related("user","movie",).prefetch_related("tags") .filter(
                movie=movie
            ).aggregate(
                avg=Avg("rating")
            )
        if findAvg["avg"] is not None:
                avg=float(findAvg["avg"])
        
        
        

        contex={
            'movie':movie,
            "movieImages":movieImages,
            "movieVideos":movieVideos,
            "comments":comments,
            "form":CommentForm(),
            "avg":avg

        }


        return render(request,"movies/moviesingle.html",contex)
    





    def post(self,request,movie_id,*args,**kwargs):


        movie=get_object_or_404(Movie.objects.select_related(
            "parent","genre","sponsor"
            ).prefetch_related(
                "tag","days","booked_seats","times","actors","comment_set"
            ),id=movie_id)



        print("POSTTT")
        # form=CommentForm(self.request.POST)
        # if form.is_valid():

        body=self.request.POST.get("body")
        rating=self.request.POST.get("rating")
        print("$$$$$$$$$")
        print("$$$$$$$$$")
        print(type(rating))
        print("$$$$$$$$$")
        print("$$$$$$$$$")

        
        new_comment=Comment(
            user=request.user,body=body,movie=movie,
            rating=rating,rate_show=float(rating)
        )
        new_comment.save( )

        x=[]
        x.append({
            "body":new_comment.body,
            "username":new_comment.user.username,
            "movieId":new_comment.movie.id,
            "imageProfile":new_comment.user.profile.image.url,
            "created":new_comment.created,
            # "commentDisplay":new_comment.get_rate_show_display
        })


        if request.is_ajax():
            print("AJAXXXXXX")
            print("AJAXXXXXX")
            # print(new_comment)
            print(new_comment.method_show_display())
            print("AJAXXXXXX")
            print("AJAXXXXXX")
            return JsonResponse(x,safe=False)
        return redirect("movieDetail",movie.id)

        