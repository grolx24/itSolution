from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download/', views.download_file, name='download_file'),
    path('downloads/', views.download_files, name='download_files'),
    path('update/', views.update_recent_requests, name='update_recent_requests'),
    path('resume/', views.resume, name='resume'),
]
