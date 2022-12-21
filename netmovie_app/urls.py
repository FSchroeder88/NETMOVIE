
from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from user import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from video.views import video
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from user.views import (
    register_view,
    login_view,
    logout_view,
    activate,
    profile_view
)


urlpatterns = [
    path('',login_view, name="login"),
    path('admin/', admin.site.urls),
    path('video/', video, name="video"),
    path('login/', login_view, name="login"),
    path('profile/', profile_view, name="profile"),
    path('logout/', logout_view, name="logout"),
    path('register/', register_view, name="register"),
    path('__debug__/', include('debug_toolbar.urls')),
    path('activate/<uidb64>/<token>/', activate, name="activate"),
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
    #     activate, name="activate"),

] 
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns() 
