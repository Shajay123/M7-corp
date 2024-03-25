from django.urls import path

from django.conf.urls.static import static
from . import views
from django.conf import settings  # Assuming your views are in the same directory

urlpatterns = [
    path('', views.home, name='home'),
    path('camera/', views.camera, name='camera'),
    path('attendance/', views.attendance, name='attendance'),
    path('salary/', views.salary, name='salary'),
    path('team/', views.team, name='team'),
    path('Approvals/', views.Approvals, name='Approvals'),
    path('signup/',views.signup, name='signup'),
    path('get_leave_requests/', views.get_leave_requests, name='get_leave_requests'),
    path('signup_success/',views.signup_success, name='signup_success'),
]



# Serving media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)