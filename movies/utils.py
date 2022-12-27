from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


def handle_paginnator(obj,perPage,page):

    paginator=Paginator(obj,perPage)
    try:
        result=paginator.page(page)

    except PageNotAnInteger:

        result=paginator.page(1)
    except EmptyPage:
        result=paginator.page(paginator.num_pages)
        
    return result






# def paginateWithRange(request, projects, results):

#     page = request.GET.get('page')
#     paginator = Paginator(projects, results)

#     try:
#         projects = paginator.page(page)
#     except PageNotAnInteger:
#         page = 1
#         projects = paginator.page(page)
#     except EmptyPage:
#         page = paginator.num_pages
#         projects = paginator.page(page)

#     leftIndex = (int(page) - 4)

#     if leftIndex < 1:
#         leftIndex = 1

#     rightIndex = (int(page) + 5)

#     if rightIndex > paginator.num_pages:
#         rightIndex = paginator.num_pages + 1

#     custom_range = range(leftIndex, rightIndex)

#     return custom_range, projects

