from django.contrib import admin

from .models import FirstStepEvent, UserEvent

admin.site.register(FirstStepEvent)
admin.site.register(UserEvent)