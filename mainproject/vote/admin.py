from django.contrib import admin

# Register your models here.

from .models import voter_data

admin.site.register(voter_data)