from django import template
from ..models import Movie

register=template.Library()

@register.inclusion_tag("movies/movie_navbar.html")
def forNavbar():

    movies=Movie.objects.select_related("genre"). prefetch_related("tag","days","times","booked_seats"
        ).all()
    filtered=[i for i in movies if i.is_parent==True]

    return {
        "movies":filtered
    }

    