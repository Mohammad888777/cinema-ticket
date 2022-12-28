from django.urls import path
from . import views

urlpatterns=[

    path("<str:username>/",views.ProfileView.as_view(),name="myProfile"),
    path("updatePassword/<str:username>/",views.updatePassword,name="updatePassword"),
    
]