from django.db import models
from django.contrib.auth.models import User, auth
from datetime import datetime
# Create your models here.


# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver


class Customer(models.Model):
    first_name=models.CharField(max_length=70, null = True)
    last_name=models.CharField(max_length=70, null = True)
    email=models.EmailField(null = True)
    account_name= models.CharField(max_length = 70, default = "No account name")
    renewal_date = models.DateField(default = datetime.now().date())
    revenue = models.FloatField(default = 0.0)
    added_by = models.ForeignKey(User, on_delete = models.CASCADE, null = True)

    def __str__(self):
        if self.first_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return self.account_name

    def __unicode__(self):
        return f'{self.first_name}'
    
    def all_data(self):
        all_info = myFieldValue.objects.filter(customer = self)
        return all_info

class myField(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	field_name = models.CharField(max_length = 255)
	field_type = models.CharField(max_length = 255)
	is_requied = models.BooleanField()

	def titleName(self):
		new_name = self.field_name.replace("_", " ")
		new_name = new_name.split(" ")
		for i in range(len(new_name)):
			first_letter = new_name[i][0]
			new_name[i] = first_letter.upper() + new_name[i][1:]

		return " ".join(new_name)

	def required(self):
		temp_var = ''
		if self.is_requied:
			temp_var = 'required'
		return temp_var
			

class myFieldValue(models.Model):
	field = models.ForeignKey(myField, on_delete = models.CASCADE)
	value = models.CharField(max_length = 255, null = True)
	customer = models.ForeignKey(Customer, on_delete = models.CASCADE)

	def get_value(self):
		if not self.value:
			return "Not provided"
		
		my_value = self.value

		if self.field.field_type == 'date':
			if '/' in my_value:
				my_value = "-".join(my_value.split("/")[::-1])
			
			make_date_object = datetime.strptime(my_value, "%Y-%m-%d")
			my_value = make_date_object.date()

		if self.field.field_type == 'number' and self.field.field_name.lower() != "age":
			if len(my_value) < 10:
				my_value = f'$ {my_value}'

		return my_value

class dynamicFieldStatus(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)

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
			wording = "OPEN"
			class_name = "on-going-label"	
			box_class = "ongoing"

		if self.status == -1:
			wording = "OVERDUE"
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

	def incomplete_now(self):
		self.status = 0
		self.completed_at = None
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
	
	def text_with_line(self):
		return self.note_text.replace("\n", "<br>")

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


