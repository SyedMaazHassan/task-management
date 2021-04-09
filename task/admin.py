from django.contrib import admin
from .models import Customer,Task,Note
# Register your models here.

admin.site.register(Customer)
admin.site.register(Task)
admin.site.register(Note)