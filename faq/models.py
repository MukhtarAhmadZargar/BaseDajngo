from django.db import models
from accounts.models import User
from ckeditor.fields import RichTextField


class Faq(models.Model):
	question = models.CharField(max_length=250,null=True,blank=True)
	answer = RichTextField(null=True,blank=True)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

	class Meta:
		managed = True;
		db_table = 'tbl_faq'