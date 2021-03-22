from django.db import models
from django.contrib.auth.hashers import make_password
# Create your models here.

class voter_data(models.Model):
    aadhar_number=models.CharField(max_length=12,default='')
    key_number=models.IntegerField()
    key=models.CharField(max_length=50,default='')
    password=models.CharField(max_length=100,default='')

    def __str__(self):
         return self.aadhar_number

    class Meta:
        verbose_name_plural = "data"     
