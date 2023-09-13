import uuid

from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


class PotentialAttendee(models.Model):
    full_name = models.CharField(max_length=255, null=True)
    mobile_number = models.CharField(max_length=20)
    email = models.EmailField()


class Attendee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=20)
    email = models.EmailField()
    has_attended = models.BooleanField(default=False)
    has_received_email = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the Person object first to get an id
        if self.id is not None and not self.qr_code:
            qrcode_img = qrcode.make(self.id)
            canvas = Image.new('RGB', (370, 370), 'white')
            draw = ImageDraw.Draw(canvas)
            canvas.paste(qrcode_img)
            fname = f'qr_code-{self.full_name}.png'
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            self.qr_code.save(fname, File(buffer), save=False)
            canvas.close()
            super().save(*args, **kwargs)  # Save again to save the qr_code
