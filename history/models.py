from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class LoginHistory(models.Model):
    User_Ip = models.CharField( max_length=255,null=True,blank=True)
    User_agent = models.CharField(max_length=255,null=True,blank=True)
    State = models.CharField( default=timezone.now, max_length=255)
    Code = models.CharField( default=timezone.now, max_length=255)
    create_time = models.DateTimeField(default=timezone.now)
    user = models.CharField( max_length=255,null=True,blank=True)

    class Meta:
        verbose_name = _('feed')
        managed = True
        db_table = 'tbl_feeds'
