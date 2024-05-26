from django.utils import timezone
from .models import RequestLog

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        RequestLog.objects.create(
            text=request.GET.get('text', ''),
            timestamp=timezone.now(),
            endpoint=request.path,
            status_code=response.status_code,
            client_ip=self.get_client_ip(request)
        )

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
