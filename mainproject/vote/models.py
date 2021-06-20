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

class results_publish_status(models.Model):
    Publish_result  =models.BooleanField(default=False)

    def __str__(self):
        if self.Publish_result:
            return "Results are Published"
        else:
            return "Results are not Published"    
    class Meta:
        verbose_name_plural = "results_publish_status" 

class transactions(models.Model):
    node_id             =models.IntegerField(default=-1)
    hash_value          =models.CharField(max_length=64,default='',)
    catagory            =models.CharField(max_length=20,default='')
    checksum            =models.CharField(max_length=100,default='')
    pid                 =models.IntegerField(default=-1)
    input_value         =models.TextField()

    def __str__(self):
        return self.checksum
    class Meta:
        verbose_name_plural = "transactions"


class parties(models.Model):
    checksum            =models.CharField(max_length=100,default='')
    candidate_id        =models.IntegerField(default=-1)
    symbol              =models.ImageField(upload_to='symbols/',default='')

    def __str__(self):
        return str(self.candidate_id)
    class Meta:
        verbose_name_plural = "parties"
