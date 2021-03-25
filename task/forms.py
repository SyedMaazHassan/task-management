from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Customer,Task,Note

from django.core.exceptions import ValidationError




class UserRegistrationForm(UserCreationForm):
	email=forms.EmailField()
	
	class Meta:
		model=User
		fields=['username','email','password1','password2']


class CustomerForm(forms.ModelForm):
	class Meta:
		model=Customer
		fields=['account_name','renewal_date','revenue']


class TaskForm(forms.ModelForm):
	class Meta:
		model=Task
		fields='__all__'


class NoteForm(forms.ModelForm):
	class Meta:
		model=Note
		fields='__all__'




	def clean_first_name(self):

		fname= self.cleaned_data.get('first_name')

		if not fname:

			raise forms.ValidationError('This field is required')


		for instance in Customer.objects.all():

			if instance.first_name==fname:
				raise forms.ValidationError(fname + ' is already exist')
		return fname




	def clean_last_name(self):

		lname= self.cleaned_data.get('last_name')

		if not lname:

			raise forms.ValidationError('This field is required')


		for instance in Customer.objects.all():

			if instance.last_name==lname:
				raise forms.ValidationError(lname + ' is already exist')
		return lname


	def clean_email(self):

		email= self.cleaned_data.get('email')

		if not email:

			raise forms.ValidationError('This field is required')


		for instance in Customer.objects.all():

			if instance.email==email:
				raise forms.ValidationError(email + ' is already exist')
		return email


		