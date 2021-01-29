from django.urls import path
from . import views
#from django.contrib.auth.views import views as auth_views

urlpatterns = [
        path('', views.index, name='index'),
        path('profile.html', views.profile, name='profile'),
        path('login.html', views.login, name='login'),
        path('register.html', views.register, name='register'),
        path('settings.html', views.settings, name='settings'),
        # path('forgotpassword.html', views.forgotpassword, name='forgotpassword'),
        path('youtube.html', views.youtube, name='youtube'),
]