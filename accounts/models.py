from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from sorl.thumbnail import get_thumbnail
from django.utils.translation import ugettext_lazy as _

alphanumeric = RegexValidator(r'^[a-zA-Z ]*$', 'Only alpha characters are allowed.')

number = RegexValidator(r'^^(\+\d{1,3})?,?\s?\d{8,13}', 'Only numbers are allowed.')

STATUS = ((1, "Active"),(2,"Inactive"),(3,"Deleted"))

USER_ROLE = ((1, "SuperAdmin"),(2, "Users"))

DEVICE_TYPE = [
    (1,'Android'),
    (2,'ios'),
        ]

class User(AbstractUser):
    username = models.CharField(max_length=150,unique=True,validators=[alphanumeric],blank=True, null=True)
    full_name = models.CharField(max_length=150,validators=[alphanumeric],null=True,blank=True)
    first_name = models.CharField(max_length=150,validators=[alphanumeric],null=True,blank=True)
    last_name = models.CharField(max_length=150,validators=[alphanumeric],null=True,blank=True)
    description = models.CharField(max_length=256, blank=True,null=True)
    email = models.EmailField("email address",unique=True)
    mobile_no = models.CharField(max_length=100,validators=[number], null=True, blank=True, unique=True)
    gender = models.CharField(max_length=10, blank=True,null=True)
    profile_pic = models.ImageField(upload_to='profile_pic/', blank=True, null=True)
    dob = models.DateField(null=True,blank=True)
    address = models.TextField(null=True, blank=True)
    latitude = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)
    role_id = models.PositiveIntegerField(default=1,choices=USER_ROLE)
    state_id = models.PositiveIntegerField(default=1, choices=STATUS)
    otp = models.CharField(max_length=10,blank=True,null=True)
    otp_verify = models.BooleanField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True;
        db_table = 'tbl_user'


    def __str__(self):
        return str(self.username)

class Activities(models.Model):
    performed_by = models.CharField(max_length=200, null=True,blank=True)
    user = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
    action_taken = models.CharField(max_length=200,null=True,blank=True)
    performed_for = models.CharField(max_length=200,null=True,blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    created_on_time = models.TimeField(auto_now_add=True)

    class Meta:
        managed = True;
        db_table = 'tbl_activities'

    def __str__(self):
        return str(self.performed_for)




 
