from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class Myvoter_dataManager(BaseUserManager):
    def create_user(self,aadhar_number,key_number,key,password=None):
        if not aadhar_number:
            raise ValueError("USERS SHOULD HAVE AADHAR NUMBER")
        if not key_number:
            raise ValueError("USERS SHOULD HAVE KEY_NUMBER")
        if not key:
            raise ValueError("USERS SHOULD HAVE KEY")

        user= self.model(
            aadhar_number=aadhar_number,
            key_number=key_number,
            key=key
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,aadhar_number,key_number,key,password):
        user= self.create_user(
            aadhar_number=aadhar_number,
            key_number=key_number,
            key=key,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class voter_data(AbstractBaseUser):
    aadhar_number       =models.CharField(max_length=12,default='')
    key_number          =models.IntegerField()
    key                 =models.CharField(max_length=50,default='',unique=True)
    date_joined         =models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login          =models.DateTimeField(verbose_name='last login',auto_now=True)
    is_admin            =models.BooleanField(default=False)
    is_active           =models.BooleanField(default=True)
    is_staff            =models.BooleanField(default=False)
    is_superuser        =models.BooleanField(default=False)
    is_verified         =models.BooleanField(default=False)

    USERNAME_FIELD='key'
    REQUIRED_FIELDS=['aadhar_number','key_number',]

    objects=Myvoter_dataManager()

    def __str__(self):
         return self.aadhar_number

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name_plural = "data"     
