from django.db import models
from django.utils import timezone

class RequestLog(models.Model):
    text = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)
    endpoint = models.CharField(max_length=255)
    status_code = models.IntegerField()
    client_ip = models.CharField(max_length=45)

    class Meta:
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.text} - {self.timestamp}"
