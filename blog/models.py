from ckeditor.fields import RichTextField
from django.utils import timezone
from accounts.models import User
from django.db import models



class Category(models.Model):
    title = models.CharField(max_length=150, null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by_id = models.ForeignKey(User,related_name="created_by_user",on_delete=models.CASCADE)

    class Meta:
        managed = True;
        db_table = 'tbl_blog_category'


class Blog(models.Model):
    title = models.CharField(max_length=150, null=True,blank=True)
    body = RichTextField(null=True,blank=True)
    views= models.IntegerField(default=0)
    image_file = models.ImageField(upload_to='blog/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on =models.DateTimeField(auto_now=True)
    created_by_id = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        managed = True;
        db_table = 'tbl_blog'


