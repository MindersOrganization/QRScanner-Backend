from django.contrib import admin

from .models import Attendee , PotentialAttendee

admin.site.register(Attendee)

admin.site.register(PotentialAttendee)