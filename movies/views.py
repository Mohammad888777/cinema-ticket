from django.shortcuts import render,redirect,get_object_or_404
from .models import Movie,Genres
from django.views.generic import ListView,DetailView
from django.http import JsonResponse
from django.db.models import Q,Avg
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q,Avg,Count
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
from accounts.forms import SignupForm
from accounts.models import User
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts  import get_current_site
from django.template.loader import render_to_string
from .utils import handle_paginnator,full_list,moreItems
from datetime import datetime



def movieList(request):

    movies=Movie.objects. prefetch_related("genre","tag","days","times","booked_seats"
        ).annotate(avg=Avg("comment__rating")).all().order_by("-timeAdded")

    for m in movies:
        print(m.avg,type(m.avg))
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






class  MovieDetail(View):


    def get(self,request,movie_id,page=None,page_for_relatedMovies=None,*args,**kwargs):

    
        # movie=Movie.objects. prefetch_related("genre","tag","days","times","booked_seats"
        # ).exclude(parent=None).get(pk=movie_id)
        


        movie=Movie.objects. prefetch_related("genre","tag","days","times","booked_seats"
        ).get(pk=movie_id)


            
        movieImages=None
        if movie.movieimage_set.all():

            movieImages=movie.movieimage_set.all()[:3]
        movieVideos=None
        if movie.movievideo_set.all():
            movieVideos=movie.movievideo_set.all()[:1]


        page=self.request.GET.get("page",1)
        per_page=self.request.GET.get("per_page",2)
        filter_status=self.request.GET.get("status","Rating_Ascending")

        comments=None
        res=None
        how_to_order=""

        if movie.comment_set.all():

            if filter_status:
                match filter_status:
                    case "Rating_Ascending":
                        how_to_order="-rating"
                    case "Rating_Descending":
                        how_to_order="rating"
                    case "Release_date_Descending":
                        how_to_order="created"
                    case "Release_date_Ascending":
                        how_to_order="-created"
                    

                comments=Comment.objects.select_related("user","movie",).prefetch_related("tags") .filter(
                        Q(movie=movie)
                    ).order_by(how_to_order)

                res=handle_paginnator(comments,per_page,page)

        avg=0
        findAvg=Comment.objects.select_related("user","movie",).prefetch_related("tags") .filter(
                movie=movie
            ).aggregate(
                avg=Avg("rating")
            )

        if findAvg["avg"] is not None:
                avg=round(float(findAvg["avg"]),1)
        
        last_comment=Comment.objects.select_related("user","movie").prefetch_related("tags").filter(
            movie=movie
        ).last()

        movie_genres_ids=[]
        for g in movie.genre.all():
            movie_genres_ids.append(g.id)
        
        page_for_relatedMovies=self.request.GET.get("page_for_relatedMovies",1)
        per_page_relatedMovies=self.request.GET.get("per_page_relatedMovies",2)
        filter_status_relatedMovies=self.request.GET.get("status_for_relatedMovies","Rating_Ascending")

        res2=None
        how_to_order2=""
        related_movies=None

        if filter_status_relatedMovies:

            match filter_status_relatedMovies:
                case "Rating_Ascending":
                    how_to_order2="-avg"
                case "Rating_Descending":
                    how_to_order2="avg"
                case "Release_date_Descending":
                    how_to_order2="created"
                case "Release_date_Ascending":
                    how_to_order2="-created" 
            
            related_movies=Movie.objects.select_related(
                        "parent","sponsor"
                    ).prefetch_related(
                        "genre","tag","days","times","booked_seats"
                    ).annotate(
                        avg=Avg("comment__rating")).filter(
                        ~Q(id=movie.id) &Q(genre__in=movie_genres_ids)
                    ).order_by(how_to_order2)

            res2=handle_paginnator(related_movies,per_page_relatedMovies,page_for_relatedMovies)


        related_movies_count=Movie.objects.prefetch_related(
            "genre","tag","days","times","booked_seats"
        ). exclude(
                parent=None
        ). filter(

            ~Q(id=movie.id) &Q(genre__in=movie_genres_ids)
        )

        contex={

            'movie':movie,
            "movieImages":movieImages,
            "movieVideos":movieVideos,
            "comments":res,
            "form":CommentForm(),
            "avg":avg,
            'per_page':per_page,
            'per_page_relatedMovies':per_page_relatedMovies,
            'filter_status':filter_status,
            'filter_status_relatedMovies':filter_status_relatedMovies,
            'last_comment':last_comment,
            'related_movies':res2,
            'related_movies_count':related_movies_count,


        }


        return render(request,"movies/moviesingle.html",contex)
    

    def post(self,request,movie_id,*args,**kwargs):


        movie=get_object_or_404(Movie.objects.prefetch_related(
                "tag","days","booked_seats","times","actors","comment_set","genre"
            ),id=movie_id)

        body=self.request.POST.get("body")
        rating=self.request.POST.get("rating")


        
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
            "rating":new_comment.rating
            # "commentDisplay":new_comment.get_rate_show_display
        })

        if request.is_ajax():

            return JsonResponse(x,safe=False)
        return redirect("movieDetail",movie.id)




def relatedReviewView(request,movie_id):

    movie=get_object_or_404(Movie.objects.select_related(
            "parent","sponsor"
        ).prefetch_related(
             "genre","tag","days","times","booked_seats"
    ),pk=movie_id)

    movie_genres_ids=[]
    for g in movie.genre.all():
        movie_genres_ids.append(g.id)

    related_movies=Movie.objects.select_related(
            "parent","sponsor"
        ).prefetch_related(
            "genre","tag","days","times","booked_seats"
        ).annotate(
            avg=Avg("comment__rating")).filter(

            ~Q(id=movie.id) &Q(genre__in=movie_genres_ids)
        )
    
    related_movies_count=Movie.objects.prefetch_related(
            "genre","tag","days","times","booked_seats"
        ). exclude(
                parent=None
        ). filter(

            ~Q(id=movie.id) &Q(genre__in=movie_genres_ids)
        )

    contex={
        'related_movies':related_movies,
        'movie':movie,
        'related_movies_count':related_movies_count
    }
    
    return render(request,"movies/movieRelatedView.html",contex)




class AllMoviesView(View):

    def get(self,request,*args,**kwargs):

        page=self.request.GET.get("page",1)
        perPage=self.request.GET.get("perPage",2)
        filter_status=self.request.GET.get("status","Rating_Ascending")

        movies=None
        res=None
        how_to_order=None

        if filter_status:
            match filter_status:
                case "Rating_Ascending":
                        how_to_order="-avg"
                case "Rating_Descending":
                    how_to_order="avg"
                case "Release_date_Descending":
                    how_to_order="created"
                case "Release_date_Ascending":
                    how_to_order="-created"
            
            movies=Movie.objects.select_related(
                    "sponsor","parent"
                ).prefetch_related(
                "genre","tag","days","times","booked_seats"
                ).annotate(
                    avg=Avg("comment__rating")
                ).all().order_by(how_to_order)
            res=handle_paginnator(movies,perPage,page)

        now=datetime.now()

        contex={

            'movies':res,
            'filter_status':filter_status,
            'perPage':perPage,
            'allGenres':Genres.objects.all(),
            'from':[i for i in range(1970,now.year)],
            'to':[i for i in range(1970,now.year)],

        }

        return render(request,"movies/allMovies.html",contex)





class AllListMoviesView(View):


    def get(self,request,*args,**kwargs):

        page=self.request.GET.get("page",1)
        perPage=self.request.GET.get("perPage",2)
        filter_status=self.request.GET.get("status","Rating_Ascending")
        ratingRange=self.request.GET.get("ratingRange",'7,10')

        movies=None
        res=None
        how_to_order=None

        if filter_status:
            match filter_status:
                case "Rating_Ascending":
                        how_to_order="-avg"
                case "Rating_Descending":
                    how_to_order="avg"
                case "Release_date_Descending":
                    how_to_order="created"
                case "Release_date_Ascending":
                    how_to_order="-created"
            
            movies=Movie.objects.select_related(
                    "sponsor","parent"
                ).prefetch_related(
                "genre","tag","days","times","booked_seats"
                ).annotate(
                    avg=Avg("comment__rating")
                ).all().order_by(how_to_order)
            res=handle_paginnator(movies,perPage,page)

        contex={

            'movies':res,
            'filter_status':filter_status,
            'perPage':perPage,
            'ratingRange':ratingRange,

        }

        return render(request,"movies/movielist.html",contex)




class AllMovieSearch(View):

    def get(self,request,*args,**kwargs):

        now=datetime.now()

        page=self.request.GET.get("page",1)
        perPage=self.request.GET.get("perPage",2)
        filter_status=self.request.GET.get("status","Rating_Ascending")

        movieName=self.request.GET.get("movieName","")

        ratingRange=self.request.GET.get("ratingRange",'7,10')
        splitedRatingRange=ratingRange.split(",")
        
        yearFrom=self.request.GET.get("yearFrom",1970)

        yearTo=self.request.GET.get("yearTo",now.year)
        genre=self.request.GET.get("genre","")

        founded=None
        GenreId=None

        if Genres.objects.filter(genres_name=genre).exists():
            founded=Genres.objects.get(genres_name=genre)
            GenreId=founded.id

        res=None
        movies=None

        if movieName and not genre  :
             print("FIRST")
             movies=Movie.objects.select_related(
                    "parent","sponsor"
                ).prefetch_related(
                    "genre","tag","days","times","booked_seats"
                ).annotate(
                    avg=Avg("comment__rating")
                ).filter(

                    Q(name__icontains=movieName) &
                    # Q(avg__gt=float(splitedRatingRange[0])) & Q(avg__lt=float(splitedRatingRange[1])) &
                    # # Q(genre__in=genresId) &
                    Q(year_made__gt=yearFrom)&
                    Q(year_made__lt=yearTo)&
                    ~Q(parent=None)
                )
        elif movieName and genre:
            print("SECOND")
            movies=Movie.objects.select_related(
                    "parent","sponsor"
                ).prefetch_related(
                    "genre","tag","days","times","booked_seats"
                ).annotate(
                    avg=Avg("comment__rating")
                ).filter(

                    Q(name__icontains=movieName) &
                    Q(avg__gt=float(splitedRatingRange[0])) & Q(avg__lt=float(splitedRatingRange[1])) &
                    Q(genre__in=[GenreId]) &
                    Q(year_made__gt=yearFrom)&
                    Q(year_made__lt=yearTo)&
                    ~Q(parent=None)
                )
   
        elif not movieName and not genre :
            print("FOURTH")
            movies=Movie.objects.select_related(
                    "parent","sponsor"
                ).prefetch_related(
                    "genre","tag","days","times","booked_seats"
                ).annotate(
                    avg=Avg("comment__rating")
                ).filter(

                    # Q(name__icontains=movieName) &
                    Q(avg__gte=float(splitedRatingRange[0])) & Q(avg__lte=float(splitedRatingRange[1])) &
                    # # Q(genre__in=genresId) &
                    Q(year_made__gte=yearFrom)&
                    Q(year_made__lte=yearTo)&
                    ~Q(parent=None)
                )
        elif not movieName and genre:

            movies=Movie.objects.select_related(
                    "parent","sponsor"
                ).prefetch_related(
                    "genre","tag","days","times","booked_seats"
                ).annotate(
                    avg=Avg("comment__rating")
                ).filter(

                    # Q(name__icontains=movieName) &
                    Q(avg__gte=float(splitedRatingRange[0])) & Q(avg__lte=float(splitedRatingRange[1])) &
                    Q(genre__in=[GenreId]) &
                    Q(year_made__gte=yearFrom)&
                    Q(year_made__lte=yearTo)&
                    ~Q(parent=None)
                )
 
        else:
            print("ELSE")
            movies=Movie.objects.select_related(
                    "parent","sponsor"
                ).prefetch_related(
                    "genre","tag","days","times","booked_seats"
                ).annotate(
                    avg=Avg("comment__rating")
                ).filter(

                    ~Q(parent=None)
                )

        how_to_order=None
        if filter_status:
            match filter_status:
                case "Rating_Ascending":
                    how_to_order="-avg"
                case "Rating_Descending":
                    how_to_order="avg"
                case "Release_date_Descending":
                    how_to_order="created"
                case "Release_date_Ascending":
                    how_to_order="-created"

        res=handle_paginnator(movies.order_by(how_to_order),perPage,page)

        contex={
            'movies':res,
            'filter_status':filter_status,
            'perPage':perPage,
            'ratingRange':ratingRange,
            'yearFrom':yearFrom,
            'yearTo':yearTo,
            'gens':genre,
            'allGenres':moreItems,
            'movieName':movieName

        }

        return render(request,"movies/allMoviesSearch.html",contex)




class AllListMoviesSearch(View):

    def get(self,request,*args,**kwargs):

        now=datetime.now()

        page=self.request.GET.get("page",1)
        perPage=self.request.GET.get("perPage",2)
        filter_status=self.request.GET.get("status","Rating_Ascending")

        movieName=self.request.GET.get("movieName","")

        ratingRange=self.request.GET.get("ratingRange",'7,10')
        splitedRatingRange=ratingRange.split(",")
        
        yearFrom=self.request.GET.get("yearFrom",1970)

        yearTo=self.request.GET.get("yearTo",now.year)
        genre=self.request.GET.get("genre","")

        founded=None
        GenreId=None

        if Genres.objects.filter(genres_name=genre).exists():
            founded=Genres.objects.get(genres_name=genre)
            GenreId=founded.id

        res=None
        movies=None

        if movieName and not genre  :
             print("FIRST")
             movies=Movie.objects.select_related(
                    "parent","sponsor"
                ).prefetch_related(
                    "genre","tag","days","times","booked_seats"
                ).annotate(
                    avg=Avg("comment__rating")
                ).filter(

                    Q(name__icontains=movieName) &
                    # Q(avg__gt=float(splitedRatingRange[0])) & Q(avg__lt=float(splitedRatingRange[1])) &
                    # # Q(genre__in=genresId) &
                    Q(year_made__gt=yearFrom)&
                    Q(year_made__lt=yearTo)&
                    ~Q(parent=None)
                )
        elif movieName and genre:
            print("SECOND")
            movies=Movie.objects.select_related(
                    "parent","sponsor"
                ).prefetch_related(
                    "genre","tag","days","times","booked_seats"
                ).annotate(
                    avg=Avg("comment__rating")
                ).filter(

                    Q(name__icontains=movieName) &
                    Q(avg__gt=float(splitedRatingRange[0])) & Q(avg__lt=float(splitedRatingRange[1])) &
                    Q(genre__in=[GenreId]) &
                    Q(year_made__gt=yearFrom)&
                    Q(year_made__lt=yearTo)&
                    ~Q(parent=None)
                )
   
        elif not movieName and not genre :
            print("FOURTH")
            movies=Movie.objects.select_related(
                    "parent","sponsor"
                ).prefetch_related(
                    "genre","tag","days","times","booked_seats"
                ).annotate(
                    avg=Avg("comment__rating")
                ).filter(

                    # Q(name__icontains=movieName) &
                    Q(avg__gte=float(splitedRatingRange[0])) & Q(avg__lte=float(splitedRatingRange[1])) &
                    # # Q(genre__in=genresId) &
                    Q(year_made__gte=yearFrom)&
                    Q(year_made__lte=yearTo)&
                    ~Q(parent=None)
                )
        elif not movieName and genre:

            movies=Movie.objects.select_related(
                    "parent","sponsor"
                ).prefetch_related(
                    "genre","tag","days","times","booked_seats"
                ).annotate(
                    avg=Avg("comment__rating")
                ).filter(

                    # Q(name__icontains=movieName) &
                    Q(avg__gte=float(splitedRatingRange[0])) & Q(avg__lte=float(splitedRatingRange[1])) &
                    Q(genre__in=[GenreId]) &
                    Q(year_made__gte=yearFrom)&
                    Q(year_made__lte=yearTo)&
                    ~Q(parent=None)
                )
 
        else:
            print("ELSE")
            movies=Movie.objects.select_related(
                    "parent","sponsor"
                ).prefetch_related(
                    "genre","tag","days","times","booked_seats"
                ).annotate(
                    avg=Avg("comment__rating")
                ).filter(

                    ~Q(parent=None)
                )

        how_to_order=None
        if filter_status:
            match filter_status:
                case "Rating_Ascending":
                    how_to_order="-avg"
                case "Rating_Descending":
                    how_to_order="avg"
                case "Release_date_Descending":
                    how_to_order="created"
                case "Release_date_Ascending":
                    how_to_order="-created"

        res=handle_paginnator(movies.order_by(how_to_order),perPage,page)

        contex={
            'movies':res,
            'filter_status':filter_status,
            'perPage':perPage,
            'ratingRange':ratingRange,
            'yearFrom':yearFrom,
            'yearTo':yearTo,
            'gens':genre,
            'allGenres':moreItems,
            'movieName':movieName

        }

        return render(request,"movies/allListMoviesSearch.html",contex)
        