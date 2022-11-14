from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from login import views as user_views
from .forms import CustomAuthForm

app_name = 'login'

urlpatterns = [
     path('', auth_views.LoginView.as_view(template_name='login/login.html', redirect_authenticated_user = True, authentication_form=CustomAuthForm), name = 'login-login'),
     path('logout/', auth_views.LogoutView.as_view(template_name='login/logout.html'), name = 'login-logout'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
