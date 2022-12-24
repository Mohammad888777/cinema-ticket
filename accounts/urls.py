from django.urls import path
from . import views

urlpatterns=[

    path("login/",views.loginView,name="login"),
    path("signup/",views.register,name="register"),
    path("activate/<uidb64>/<token>/",views.activate,name="activate"),
    
]