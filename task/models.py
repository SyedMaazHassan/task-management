from django.db import models
from django.contrib.auth.models import User, auth
from datetime import datetime
# Create your models here.


# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver


class Customer(models.Model):
    first_name=models.CharField(max_length=70)
    last_name=models.CharField(max_length=70)
    email=models.EmailField()
    added_by = models.ForeignKey(User, on_delete = models.CASCADE, null = True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def __unicode__(self):
        return f'{self.first_name}'



class myTask(models.Model):
	task_text = models.CharField(max_length = 255)
	created_on = models.DateTimeField(default = datetime.now())
	due_date = models.DateField()
	added_by = models.ForeignKey(User, on_delete = models.CASCADE)
	added_for = models.ForeignKey(Customer, on_delete = models.CASCADE, null = True)
	completed_at = models.DateTimeField(null = True)
	completed_on_time = models.BooleanField(default = True)
	status = models.IntegerField(default = 0)
	# -1 = late
	# 0 = ongoing
	# 1 = completed

	def get_status(self):
		if self.status == 0:
			wording = "ON GOING"
			class_name = "on-going-label"	
			box_class = "ongoing"

		if self.status == -1:
			wording = "OH LATE"
			class_name = "late-label"
			box_class = "late"

		if self.status == 1:
			wording = "COMPLETED"
			class_name = "completed-label"
			box_class = "complete"

		return {
			"wording": wording,
			"class_name": class_name,
			"box_class": box_class
		}

	def complete_now(self):
		self.status = 1
		self.completed_at = datetime.now()
		self.save()

	def late_now(self):
		if self.status != 1:
			self.status = -1
			self.completed_on_time = False
			self.save()


class myNote(models.Model):
	note_text = models.TextField()
	created_on = models.DateTimeField(default = datetime.now())
	added_by = models.ForeignKey(User, on_delete = models.CASCADE)
	added_for = models.ForeignKey(Customer, on_delete = models.CASCADE, null = True)
	


class Task(models.Model):
 	task_due_date= models.DateTimeField(auto_now_add=True)
 	task= models.CharField(max_length=100)
 	added_by= models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
 	complete= models.BooleanField(default=False)


 	def __str__(self):
 		return self.task





class Note(models.Model):
 	serial_number= models.IntegerField()
 	date= models.DateTimeField(auto_now_add=True)
 	note= models.TextField()
 	added_by= models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)


 	def __str__(self):
 		return self.note


