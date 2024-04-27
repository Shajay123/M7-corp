from django.urls import path

from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('camera/', views.camera, name='camera'),
    path('attendance/', views.attendance, name='attendance'),
    path('team/', views.team, name='team'),
    path('signup/',views.signup, name='signup'),
    path('get_checkin_data/',views.get_checkin_data, name='get_checkin_data'),
    path('signup_success/',views.signup_success, name='signup_success'),
    path('attendance/all_events', views.all_events, name='all_events'),
    path('attendance/add_event', views.add_event, name='add_event'),
    path('attendance/update', views.update, name='update'),
    path('attendance/remove', views.remove, name='remove'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('login_sucess/', views.login_sucess, name='login_sucess'),
    path('send_email/',views.sendEmail, name="send_email"),
]



# Serving media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

