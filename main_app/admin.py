from django.contrib import admin
from .models import Project # import the Project model from models.py
# Register your models here.

admin.site.register(Project) # this line will add the model to the admin panel