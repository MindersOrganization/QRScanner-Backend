from django.db import models
from QRScanner.models import Attendee

class FirstStepEvent(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images', blank=True, null=True)
    cover = models.ImageField(upload_to='event_covers', blank=True, null=True)
    date = models.DateTimeField()

    def __str__(self):
        return self.name

class UserEvent(models.Model):
    first_step_event = models.ForeignKey(FirstStepEvent, on_delete=models.CASCADE, related_name='user_events')
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE, related_name='user_events')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.attendee.full_name} - {self.first_step_event.name}'
