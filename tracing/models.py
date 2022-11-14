from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class fever(models.Model):
	fever = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.fever)

class cold(models.Model):
	cold = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.cold)


class body_pain(models.Model):
	body_pain = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.body_pain)

class loss_of_smell(models.Model):
	loss_of_smell = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.loss_of_smell)

class loss_of_taste(models.Model):
	loss_of_taste = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.loss_of_taste)

class headache(models.Model):
	headache = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.headache)

class Contact_tracing(models.Model):
	trip_date = models.DateTimeField(null=True, blank=True, auto_now=True)
	employee_student_number = models.IntegerField(null=True, blank=True)
	origin = models.CharField(max_length=200, null=True, blank=True)
	destination = models.CharField(max_length=200, null=True, blank=True)
	ticket_number = models.IntegerField(null=True, blank=True)
	shuttle_number = models.CharField(max_length=200, null=True, blank=True)
	drivers_name = models.CharField(max_length=200, null=True, blank=True)
	trip_distance = models.IntegerField(null=True, blank=True)
	feedback = models.CharField(max_length=200, null=True, blank=True)
	trip_rating = models.IntegerField(null=True, blank=True)

	fever = models.ForeignKey(fever, null=True, blank=True, on_delete = models.CASCADE)
	cold = models.ForeignKey(cold, null=True, blank=True, on_delete = models.CASCADE)
	body_pain = models.ForeignKey(body_pain, null=True, blank=True, on_delete = models.CASCADE)
	loss_of_smell = models.ForeignKey(loss_of_smell, null=True, blank=True, on_delete = models.CASCADE)
	loss_of_taste = models.ForeignKey(loss_of_taste, null=True, blank=True, on_delete = models.CASCADE)
	headache = models.ForeignKey(headache, null=True, blank=True, on_delete = models.CASCADE)

	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.trip_date)+" "+str(self.origin)+" "+str(self.destination)




