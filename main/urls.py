from django.urls import path
from .views import download_file, download_files, update_recent_requests, index
#
urlpatterns = [
    path('', index, name='index'),
    path('download/', download_file, name='download_file'),
    path('downloads/', download_files, name='download_files'),
    path('update/', update_recent_requests, name='update_recent_requests'),
]