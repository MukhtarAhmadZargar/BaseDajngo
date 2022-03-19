from django.db import models
from accounts.models import User
from blog.models import Blog
# Create your models here.

class Rating(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    user =  models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='blog')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(choices=RATING_CHOICES)


    class Meta:
        managed = True;
        db_table = 'tbl_rating'