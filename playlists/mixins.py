from django.shortcuts import redirect,get_object_or_404
from comments.models import Comment


class CommentSeeEachUser():

    def dispatch(self,request,username,*args,**kwargs):
        
        comments=Comment.objects.select_related("movie","user").filter(

        )

