from django.shortcuts import render, redirect
from django.http import HttpResponse
from VideoGenerator import VideoGenerator
from .models import RequestLog
import os
import zipfile
from django.http import JsonResponse
from django.conf import settings
import datetime

def index(request):
    text = request.GET.get('text', '')
    recent_requests = RequestLog.objects.exclude(text__exact="").order_by('-id')[:5]

    log = open(str(settings.BASE_DIR) + "/logfile", "a")

    if text != '':
        try:
            log.write(f"{ datetime.datetime.now() } start\n")
            VG = VideoGenerator(text)
            log.write(f"{ datetime.datetime.now() } start movie\n")
            VG.generate_with_moviepy()
            log.write(f"{ datetime.datetime.now() } start game\n")
            VG.generate_with_pygame()
            log.write(f"{ datetime.datetime.now() } start ffmpeg\n")
            VG.generate_with_ffmpeg()
            log.write(f"{ datetime.datetime.now() } start cv\n")
            VG.generate_with_opencv()
        except Exception as e:
            log.write(f"{ datetime.datetime.now() } { e }\n")
        finally:
            log.close()


        # После генерации видео перенаправляем на URL для скачивания файла
        return redirect('download_files')

    context = {
        'page_title': 'Генератор видео с бегущей строкой',
        'text': text,
        'recent_requests': recent_requests,
    }
    return render(request, 'main/index.html', context)

def download_file(request):
    file_path1 = str(settings.BASE_DIR) + "/out/ffmpeg_output.mp4"

    if not os.path.exists(file_path1):
        return HttpResponse(status=404)

    with open(file_path1, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path1)}'
        return response


def download_files(request):

    # Список файлов для скачивания
    files_to_download = [str(settings.BASE_DIR) + "/out/ffmpeg_output.mp4", 
    str(settings.BASE_DIR) + "/out/moviepy_output.mp4", str(settings.BASE_DIR) + "/out/pygame_output.mp4",
		str(settings.BASE_DIR) + "/out/opencv_output.mp4"]

    # Проверяем, что все файлы существуют
    for file_path in files_to_download:
        if not os.path.exists(file_path):
            return HttpResponse(status=404)

    # заголовки 
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=files.zip'

    # создаем ZIP  
    with zipfile.ZipFile(response, 'w') as zip_file:
        for file_path in files_to_download:
            zip_file.write(file_path, os.path.basename(file_path))

    return response

def update_recent_requests(request):
    recent_requests = RequestLog.objects.exclude(text__exact="").order_by('-id')[:5]
    
    recent_requests_html = ''
    for req in recent_requests:
        recent_requests_html += f'<li><a href=\"?text={req.text}\">{req.text}</a></li>'
    
    return JsonResponse({'recent_requests_html': recent_requests_html})

def resume(request):
    return render(request, 'main/resume.html')
