from django.urls import path
from .views import index, download_file, download_files

urlpatterns = [
    path('', index, name='index'),
    path('download/', download_file, name='download_file'),
    path('downloads/', download_files, name='download_files'),
]