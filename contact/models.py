from django.db import models
from django.utils import timezone
# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=255,null=True,blank=True)
    subject = models.CharField(max_length=255,null=True,blank=True)
    message = models.TextField(max_length=555,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        managed = True
        db_table = 'tbl_contact'
    def __str__(self):
        return self.name

class ContactReply(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="Contact")
    image_file = models.ImageField(upload_to='contact-us/', blank=True, null=True)
    reply = models.CharField(max_length=255,null=True,blank=True)
    subject = models.CharField(max_length=255,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        managed = True
        db_table = 'tbl_contact_reply'
    def __str__(self):
        return self.rely
