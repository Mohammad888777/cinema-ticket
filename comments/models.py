from django.db import models
from accounts.models import User
from movies.models import Movie,Tag
from django.core.validators import FileExtensionValidator
# from star_ratings.models import Rating
from decimal import Decimal




def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

"✬"

class Comment(models.Model):

    USER_BOOK_RATING = (
         
        ("1.0", "★☆☆☆☆☆☆☆☆☆"),
        ("1.5", "★✬☆☆☆☆☆☆☆☆"),
        ("2.0", "★★☆☆☆☆☆☆☆☆ "),
        ("2.5", "★★✬☆☆☆☆☆☆☆ "),
        ("3.0", "★★★☆☆☆☆☆☆☆ "),
        ("3.5", "★★★✬☆☆☆☆☆☆ "),
        ("4.0", "★★★★☆☆☆☆☆☆ "),
        ("4.5", "★★★★✬☆☆☆☆☆ "),
        ("5.0", "★★★★★☆☆☆☆☆ "),
        ("5.5", "★★★★★✬☆☆☆☆ "),
        ("6.0", "★★★★★★☆☆☆☆ "),
        ("6.5", "★★★★★★✬☆☆☆ "),
        ("7.0", "★★★★★★★☆☆☆ "),
        ("7.5", "★★★★★★★✬☆☆ "),
        ("8.0", "★★★★★★★★☆☆ "),
        ("8.5", "★★★★★★★★✬☆ "),
        ("9.0", "★★★★★★★★★☆ "),
        ("9.5", "★★★★★★★★★✬ "),
        ("10.0", "★★★★★★★★★★ "),
     
    )


    user=models.ForeignKey(User,on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    body=models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to=user_directory_path,blank=True, null=True,validators=[FileExtensionValidator(allowed_extensions=["jpg","png","jpeg"])])
    
    tags=models.ManyToManyField(Tag,blank=True)

    rating=models.FloatField(null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    rate_show=models.CharField(max_length=200,null=True,choices=USER_BOOK_RATING)
    


    def __str__(self) -> str:
        return self.body
    

    def method_show_display(self):
        return str(self.get_rate_show_display())
    

   


Newcom=Comment