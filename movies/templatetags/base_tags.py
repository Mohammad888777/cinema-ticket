from django import template
from ..models import Movie

register=template.Library()

@register.inclusion_tag("movies/movie_navbar.html")
def forNavbar():

    movies=Movie.objects. prefetch_related("tag","days","genre"
        ).all()
    filtered=[i for i in movies if i.is_parent==True]

    return {
        "movies":filtered
    }

    