from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'fts'

urlpatterns = [
    path('', views.fts, name='fts-fts'),
    path('fts1/', views.fts1, name='fts-fts1'),
    path('head/', views.head, name='head-head'),
    path('exec/', views.exec, name='exec-exec'),
    path('driver/', views.driver, name='exec-driver'),
    path('add_driver/', views.add_driver, name='exec-add_driver'),
    path('head/<int:tag>', views.headu, name='exec-head'),
    path('ftsu/<int:tag>', views.ftsu, name='exec-fts'),
    path('execu/<int:tag>', views.execu, name='exec-execu'),
]


