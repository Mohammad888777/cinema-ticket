from django.db import models
from accounts.models import User
from django.core.validators import FileExtensionValidator
# from django.contrib.contenttypes.fields import GenericRelation
# import comments.views
from django.db.models import Q,Avg



class Genres(models.Model):

    genres_name=models.CharField(max_length=200,)

    def __str__(self) -> str:
        return self.genres_name


class Tag(models.Model):

    tag_name=models.CharField(max_length=200,)
    def __str__(self) -> str:
        return self.tag_name


class Seat(models.Model):


    number=models.IntegerField()

    CHOICES=(
        ("selected","selected"),
        ("occupied","occupied"),
        ("not_selected","not_selected"),
    )
    movie=models.ForeignKey('Movie',on_delete=models.CASCADE,null=True,blank=True)
    day=models.ForeignKey('Day',on_delete=models.CASCADE,null=True,blank=True)
    seat_status=models.CharField(max_length=200,choices=CHOICES,null=True,default="not_selected")
    

    


    occupant_first_name=models.CharField(max_length=200,blank=True,null=True)
    occupant_last_name=models.CharField(max_length=200,blank=True,null=True)
    occupant_email_name=models.CharField(max_length=200,blank=True,null=True)
    is_purchased=models.BooleanField(default=False)
    purchase_time=models.DateTimeField(auto_now_add=True)



    def __str__(self) -> str:
        return str(self.movie)





class Time(models.Model):

    time=models.CharField(max_length=200,null=True,blank=True)

    def __str__(self) -> str:
        return str(self.time)
    


class Day(models.Model):

    day_week=models.CharField(max_length=200,null=True,blank=True)
    times=models.ManyToManyField(Time,related_name="times",blank=True)
    seats=models.ManyToManyField(Seat,related_name="seats",blank=True)
    movie=models.ForeignKey('Movie',on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self) -> str:
        return self.day_week+' '+str(self.movie)

        


class MovieManager(models.Manager):

    def tt(self):
        return 
        Movie.objects.select_related("genre"). prefetch_related("tag","days","times","booked_seats"
        ).filter(
            is_parent=True            
        )
    

class CompanySponser(models.Model):

    company_name=models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.company_name


def save_actor_image(instance,filename):

    return f'{instance.actor_name}/{filename}'


class Role(models.Model):
    role_name=models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.role_name


class Actor(models.Model):

    actor_name=models.CharField(max_length=200)
    actor_image=models.ImageField(default="a.png",null=True,blank=True,upload_to=save_actor_image)
    is_star=models.BooleanField(default=False)

    role=models.ForeignKey(Role,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self) -> str:
        return self.actor_name


class Movie(models.Model):

    SHOW_TYPE=(
        (1,"online"),
        (2,"offline"),
    )

    

 
    parent=models.ForeignKey("self",on_delete=models.CASCADE,related_name="+",null=True,blank=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    ticket_price=models.IntegerField(null=True,blank=True,default=0)
    user_ip=models.CharField(max_length=200,null=True,blank=True)
    movie_time=models.TimeField(null=True,blank=True)
    genre=models.ManyToManyField(Genres,related_name="genre",blank=True)
    timeAdded=models.DateTimeField(auto_now_add=True)
    show_type=models.IntegerField(choices=SHOW_TYPE,null=True,blank=True)
    is_seen_by_user=models.BooleanField(default=False,null=True,blank=True)
    online_count=models.IntegerField(default=0,null=True,blank=True)
    offline_count=models.IntegerField(default=0,null=True,blank=True)
    poster=models.ImageField(upload_to="MoviesPoster",null=True,blank=True,default="a.png")
    description=models.TextField(null=True,blank=True)
    tag=models.ManyToManyField(Tag,related_name="tags",blank=True)
    days=models.ManyToManyField(Day,related_name="days",blank=True)
    # times=models.ManyToManyField(Time,related_name="times",blank=True)
    point=models.IntegerField(default=0)
    # cast=models.ForeignKey(Cast,on_delete=models.CASCADE,null=True,related_name="cast")
    sponsor=models.ForeignKey(CompanySponser,on_delete=models.CASCADE,null=True,related_name="sponsor")
    # booked_seats=models.ManyToManyField(Seat,blank=True)
    year_made=models.IntegerField(null=True,blank=True)
    # ratings = GenericRelation(Rating, related_query_name='foos')
    language=models.CharField(max_length=200,null=True,blank=True)
    countryItMade=models.CharField(max_length=200,null=True,blank=True)
    ageCanSee=models.IntegerField(null=True,blank=True)

    actors=models.ManyToManyField(Actor,blank=True,related_name="actors")
    director=models.CharField(max_length=200,null=True,blank=True)
    writer=models.CharField(max_length=200,null=True,blank=True)
    producer=models.CharField(max_length=200,null=True,blank=True)
    photographer=models.CharField(max_length=200,null=True,blank=True)
    editor=models.CharField(max_length=200,null=True,blank=True)
    cameraman=models.CharField(max_length=200,null=True,blank=True)
    
    created=models.DateTimeField(auto_now_add=True,null=True)
    updated=models.DateTimeField(auto_now=True,null=True)

    def __str__(self) -> str:
        return self.name


    @property
    def children(self):
        return Movie.objects. prefetch_related("genre","tag","days").filter(
            parent=self            
        )
    
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    
    def is_parent2(self):
        if self.parent is None:
            return True
        return False

    is_parent2.boolean=True
    objects=MovieManager()








def images_directory_path(instance, filename):

    return f'{instance.movie.name}/{filename}'



class MovieImage(models.Model):

    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    image=models.ImageField(upload_to=images_directory_path,null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=["png","jpg","jpeg"])])

    def __str__(self) -> str:
        return self.movie.name





def video_directory_path(instance, filename):

    return f'{instance.movie.name}/{filename}'



class MovieVideo(models.Model):

    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    video=models.FileField(upload_to=video_directory_path,null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=["mp4","mp3","mk4"])])
    poster=models.ImageField(upload_to="VideoReviewPoster",null=True,blank=True,default="a.png")
    subject=models.CharField(max_length=200,null=True,blank=True)
    video_time=models.CharField(max_length=200,null=True,blank=True)

    def __str__(self) -> str:
        return self.movie.name





class Order(models.Model):
    # referrer=models.URLField()
    ORDER_STATUS=(

        (1,"cancle"),
        (2,"paid"),
        (3,"in progress"),
        
    )

    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    ip_address=models.CharField(max_length=200,null=True)
    movie_title=models.CharField(max_length=255)
    seat_number=models.CharField(max_length=200)
    order_status=models.CharField(max_length=200,choices=ORDER_STATUS)
    show_day=models.CharField(max_length=200)
    total_to_pay=models.CharField(max_length=200,null=True,blank=True)
    total_count=models.CharField(max_length=200,null=True,blank=True)



    


class Payment(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    payment_id=models.CharField(max_length=150)
    payment_method=models.CharField(max_length=150)
    amount_paid=models.CharField(max_length=150)
    status=models.CharField(max_length=150)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return str(self.payment_id)