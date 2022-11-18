from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


class Roles(models.Model):
	role_id = models.AutoField(primary_key=True)
	role = models.CharField(max_length=255, blank=True, null = True)

	def __str__(self):
		return self.role+" ID: "+str(self.role_id)

class Sex(models.Model):
    sex_id = models.AutoField(primary_key=True)
    sex = models.CharField(max_length=255, blank=True, null = True)
    def __str__(self):
        return self.sex

class Author(models.Model):        
    # required to associate Author model with User model (Important)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)


    # additional fields
    profile_picture = models.ImageField(upload_to = 'uploads/', blank = True, null = True)
    role = models.ForeignKey(Roles, default=1, on_delete=models.SET_DEFAULT)
    position = models.CharField(max_length=255, blank=True, null = True)
    student_or_employee_number = models.CharField(max_length=255, blank=True, null = True)
    year_level = models.CharField(max_length=255, blank=True, null = True)
    course_or_department = models.CharField(max_length=255, blank=True, null = True)
    sex = models.ForeignKey(Sex, null=True, blank=True, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to = 'uploads/', blank = True, null = True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make("Shuttle Ride by "+str(self.user.username))
        canvas = Image.new('RGB', (500, 500), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{str(self.user.username)}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save = False)
        canvas.close()
        super().save(*args, **kwargs)