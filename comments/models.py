from django.db import models
from blog.models import Blog
from accounts.models import User


# Create your models here.

class Comment(models.Model):
    post = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True;
        db_table = 'tbl_comment'

class Reply(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='replies')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True;
        db_table = 'tbl_reply'