from django.db import models
from django.utils import timezone
# Create your models here.

class backups(models.Model):
    Name = models.CharField( max_length=255,null=True,blank=True)
    Size = models.CharField(max_length=255,null=True,blank=True)
    create_on = models.DateTimeField(default=timezone.now,)
    create_at = models.TimeField(default=timezone.now)
    create_by = models.CharField(max_length=255,null=True,blank=True)
