from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('admin/', admin.site.urls),
    path("accounts/",include("accounts.urls")),
    path("movies/",include("movies.urls")),
    path("comments/",include("comments.urls")),
    path("playlists/",include("playlists.urls")),

    
]

# handler404 ="accounts.helpers.views.handle_not_found"


# handler404 = 'mysite.views.my_custom_page_not_found_view'
# handler500 = 'mysite.views.my_custom_error_view'
# handler403 = 'mysite.views.my_custom_permission_denied_view'
# handler400 = 'mysite.views.my_custom_bad_request_view'

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
