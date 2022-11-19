from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required

app_name = 'ticket'

urlpatterns = [
    path('', views.ticket, name='ticket-ticket'),
    path('file/', views.file, name='ticket-file'),
    path('record/', views.record, name='ticket-record'),
    path('dashtrack/', views.dashtrack, name='ticket-dashtrack'),
    path('track/', views.track, name='ticket-track'),
    path('shuttle_track/<int:tag>', views.shuttle_track, name='ticket-shuttle_track'),
    path('hdf/<int:tag>', login_required(views.df), name = "hdf"),
    path('hdf0/<int:tag>', login_required(views.df0), name = "hdf0"),
    path('conf', views.conf, name = "conf"),
    path('admindash/', views.admindash, name = "admindash"),
    path('student_page/', login_required(views.student_page), name='student_page'),
    path('employee_page/', login_required(views.employee_page), name='employee_page'),
    path('fts_page/', login_required(views.fts_page), name='fts_page'),
    path('view_ticket/<int:tag>', login_required(views.view_ticket), name='view_ticket'),
    path('view_ticket1/<int:tag>', login_required(views.view_ticket1), name='view_ticket1'),
    path('fts_ticket/', login_required(views.fts_ticket), name='fts_ticket'),
    path('a/<int:tag>', login_required(views.a), name='a'),
    path('d/<int:tag>', login_required(views.d), name='d'),
    path('cw/', login_required(views.cw), name='cw'),
    path('iscan/', views.iscan, name='iscan'),
    path('hdf_list/', login_required(views.hdf_list), name='hdf_list'),
    path('route/<int:tag>', login_required(views.route), name='route'),
    path('add_shuttle/', login_required(views.add_shuttle), name='add_shuttle'),
    path('delete_shuttle/<int:tag>', login_required(views.delete_shuttle), name='delete_shuttle'),
    path('edit_shuttle/<int:tag>', login_required(views.edit_shuttle), name='edit_shuttle'),
    path('shuttle_options/', login_required(views.shuttle_options), name='shuttle_options'),
    path('cancel_ticket/<int:tag>', login_required(views.cancel_ticket), name='cancel_ticket'),
    path('profile/', login_required(views.profile), name='profile'),
    path('add_shuttle_list/', login_required(views.add_shuttle_list), name='add_shuttle_list'),
    path('add_driver/', login_required(views.add_driver), name='add_driver'),
    path('iscan/<str:con>', login_required(views.iscancon), name='iscancon'),
    path('datav/', login_required(views.datav), name='iscancon'),
    path('add_users/', login_required(views.add_users), name='add_users'),
    path('assign/', login_required(views.assign), name='assign'),
    path('assign_role/<int:us>', login_required(views.assign_role), name='assign_role'),
    path('add_role/<int:us>', login_required(views.add_role), name='add_role'),
    path('delete_role/<int:tag>', login_required(views.delete_role), name='delete_role'),
]

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)


