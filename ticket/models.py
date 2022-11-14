from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.utils import timezone

# Create your models here.

class Status(models.Model):        
    # required to associate Author model with User model (Important)
    status_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=255, blank=True, null = True)
    
    def __str__(self):
    	return str(self.status)

class Ticket_status(models.Model):        
    # required to associate Author model with User model (Important)
    ticket_status_id = models.AutoField(primary_key=True)
    ticket_status = models.CharField(max_length=255, blank=True, null = True)
    
    def __str__(self):
        return str(self.ticket_status)

class Tickets(models.Model):        
    # required to associate Author model with User model (Important)
    ticket_id = models.AutoField(primary_key=True)
    start_date = models.DateField(blank=True, null = True)
    start_time = models.TimeField(blank=True, null = True)
    arrival_time = models.TimeField(blank=True, null = True)
    date_filed = models.DateTimeField(blank=True, null = True, auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, null = True)
    destination = models.CharField(max_length=255, blank=True, null = True)
    driver = models.CharField(max_length=255, blank=True, null = True)
    email = models.CharField(max_length=255, blank=True, null = True)
    ticket_status = models.ForeignKey(Ticket_status, null=True, blank=True, on_delete=models.CASCADE)
    cancel_reason = models.CharField(max_length=255, blank=True, null = True)
    qr_code = models.ImageField(upload_to = 'uploads/', blank = True, null = True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    approved_by = models.CharField(max_length=255, blank=True, null = True)

    def __str__(self):
    	return str(self.description)+" Date Filed: "+str(self.date_filed)+" By: "+str(self.user)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make("Approved by the FTS / "+str(self.description))
        canvas = Image.new('RGB', (500, 500), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{str(self.description)}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save = False)
        canvas.close()
        super().save(*args, **kwargs)

class participants(models.Model):        
    # required to associate Author model with User model (Important)
    participant_id = models.AutoField(primary_key=True)
    participant_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Tickets, null=True, blank=True, on_delete=models.CASCADE)
    hdf = models.IntegerField(null=True, blank=True, default = 0)
    qr_code = models.ImageField(upload_to = 'uploads/', blank = True, null = True)
    
    def __str__(self):
        return str(self.participant_user)+""+str(self.ticket)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make("Trip ticket for "+str(self.participant_user)+" "+str(self.ticket))
        canvas = Image.new('RGB', (500, 500), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{str(self.participant_user)}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save = False)
        canvas.close()
        super().save(*args, **kwargs)

class reserve(models.Model):      
    reserve_id = models.AutoField(primary_key=True)  
    reserve_date = models.DateTimeField(blank=True, null = True, auto_now_add=True)
    qr_code = models.ImageField(upload_to = 'uploads/', blank = True, null = True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.reserve_id)+str(self.reserve_date)+str(self.user)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make("Reserved / "+str(self.user))
        canvas = Image.new('RGB', (500, 500), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{str(self.user)}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save = False)
        canvas.close()
        super().save(*args, **kwargs)

class easy_maps(models.Model):        
    # required to associate Author model with User model (Important)
    address = models.CharField(max_length=255, blank=True, null = True)
    
    def __str__(self):
        return str(self.address)

class shuttle(models.Model):        
    # required to associate Author model with User model (Important)
    shuttle = models.CharField(max_length=255, blank=True, null = True)
    driver = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.shuttle)+" "+str(self.driver)

class destination(models.Model):        
    # required to associate Author model with User model (Important)
    destination = models.CharField(max_length=255, blank=True, null = True)
    
    def __str__(self):
        return str(self.destination)

class current_loc(models.Model):        
    # required to associate Author model with User model (Important)
    current_loc = models.CharField(max_length=255, blank=True, null = True)
    
    def __str__(self):
        return str(self.current_loc)

class Stations(models.Model):
    station_id = models.AutoField(primary_key=True)
    lat = models.CharField(max_length=255, blank=True, null = True)
    lon = models.CharField(max_length=255, blank=True, null = True)
    current_loc = models.ForeignKey(current_loc, null=True, blank=True, on_delete=models.CASCADE)
    destination = models.ForeignKey(destination, null=True, blank=True, on_delete=models.CASCADE)
    shuttle = models.ForeignKey(shuttle, null=True, blank=True, on_delete=models.CASCADE)

    a_driver = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.shuttle)+" "+str(self.current_loc)+" "+str(self.a_driver)

class imhere(models.Model):        
    # required to associate Author model with User model (Important)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.user)

class tracing(models.Model):
    station = models.ForeignKey(Stations, null=True, blank=True, on_delete=models.CASCADE)
    today = models.DateTimeField(null = True, blank = True, auto_now_add=True)
    hdf_url = models.CharField(max_length=255, blank=True, null = True)
    qr_code = models.ImageField(upload_to = 'uploads/', blank = True, null = True)

    def __str__(self):
        return str(self.today)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make("http:10.130.4.195:8000/ticket/"+str(self.hdf_url))
        canvas = Image.new('RGB', (500, 500), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{str(self.hdf_url)}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save = False)
        canvas.close()
        super().save(*args, **kwargs)

class answers(models.Model):        
    # required to associate Author model with User model (Important)
    answers = models.CharField(max_length=255, blank=True, null = True)
    def __str__(self):
        return str(self.answers)

class questions(models.Model):        
    # required to associate Author model with User model (Important)

    questions = models.CharField(max_length=255, blank=True, null = True)
    
    def __str__(self):
        return str(self.questions)

class hdf(models.Model):        
    # required to associate Author model with User model (Important)
    q1 = models.ForeignKey(questions, max_length=255, blank=True, null = True, related_name="q1", on_delete=models.CASCADE)
    a1 = models.CharField(max_length=255, blank=True, null = True)
    q2 = models.ForeignKey(questions, max_length=255, blank=True, null = True, related_name="q2", on_delete=models.CASCADE)
    a2 = models.CharField(max_length=255, blank=True, null = True)
    q3 = models.ForeignKey(questions, max_length=255, blank=True, null = True, related_name="q3", on_delete=models.CASCADE)
    a3 = models.CharField(max_length=255, blank=True, null = True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Tickets, null=True, blank=True, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to = 'uploads/', blank = True, null = True)
    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make("Accepted / "+str(self.user))
        canvas = Image.new('RGB', (500, 500), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{str(self.user)}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save = False)
        canvas.close()
        super().save(*args, **kwargs)

class shuttle_driver(models.Model):        
    # required to associate Author model with User model (Important)
    shuttle_driver_id = models.AutoField(primary_key=True)
    driver_name = models.CharField(max_length=255, blank=True, null = True)
    
    def __str__(self):
        return str(self.driver_name)

class shuttle_service_list(models.Model):        
    # required to associate Author model with User model (Important)
    shuttle_service_list_id = models.AutoField(primary_key=True)
    shuttle_name = models.CharField(max_length=255, blank=True, null = True)
    plate_number = models.CharField(max_length=255, blank=True, null = True)
    driver_name = models.ForeignKey(shuttle_driver, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.shuttle_name)+" "+str(self.plate_number)+" "+str(self.driver_name)

class shuttle_service(models.Model):        
    # required to associate Author model with User model (Important)
    shuttle_service_id = models.AutoField(primary_key=True)
    shuttle_name = models.ForeignKey(shuttle_service_list, null=True, blank=True, on_delete=models.CASCADE)
    gps_link = models.CharField(max_length=255, blank=True, null = True)
    
    def __str__(self):
        return str(self.shuttle_name)+" "+str(self.gps_link)



