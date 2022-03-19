from django.db import models
from accounts.models import User

# Create your models here.


class Room(models.Model):
    subscribers = models.ManyToManyField(User, blank=True)
    name = models.CharField(max_length=200, null=True,blank=True)
    owner = models.ForeignKey(User,related_name="chat_receiver",on_delete=models.CASCADE)


class Chating(models.Model):
    sender_user = models.ForeignKey(User,related_name="chat_sender",on_delete=models.CASCADE)
    receiver_user = models.ForeignKey(User,related_name="chat_receiver",on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    deleted_by_sender = models.IntegerField(default=0,blank=True,null=True)
    deleted_by_receiver = models.IntegerField(default=0,blank=True,null=True)

    class Meta:
        managed = True;
        db_table = 'chating'


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField(null=True,blank=True)
    link = models.URLField(null=True,blank=True)
    image = models.ImageField(upload_to="chating",null=True,blank=True)
    is_read = models.BooleanField(default=False)
    chating_id = models.ForeignKey(Chating,related_name="messages",on_delete=models.CASCADE)
    deleted_by_sender = models.IntegerField(default=0,blank=True,null=True)
    deleted_by_receiver = models.IntegerField(default=0,blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True;
        db_table = 'message'