from django.contrib import admin

# Register your models here.

from .models import voter_data,results_publish_status,transactions

class transactionsAdmin(admin.ModelAdmin):
    list_display = ('checksum','catagory')

admin.site.register(voter_data)
admin.site.register(results_publish_status)
admin.site.register(transactions,transactionsAdmin)