from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import itertools
from .models import Genres



def handle_paginnator(obj,perPage,page):

    paginator=Paginator(obj,perPage)
    try:
        result=paginator.page(page)

    except PageNotAnInteger:

        result=paginator.page(1)
    except EmptyPage:
        result=paginator.page(paginator.num_pages)
        
    return result





all_genres=Genres.objects.all()
genresNames=[]
for i in all_genres:
    genresNames.append(i.genres_name)


a=list(itertools.combinations(genresNames,1))

full_list=[]
for i in range(1,len(genresNames)+1):
    a=list(itertools.combinations(genresNames,i))
    full_list.append(a)

last=[]
for i in full_list:
    for j in i:
        last.append(j)

onItems=[''.join(list(i)) for i in last if len(i)==1]
moreItems=[i for i in last if len(i)!=1]
moreItems.extend(onItems)


