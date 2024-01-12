from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4
from django.urls import reverse
import pytz


# Create your models here.
User = get_user_model()


class Chat(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False)
    name = models.CharField(default='Chat', max_length=30)
    groupe = models.BooleanField(default=False)
    users = models.ManyToManyField(User)
    adm = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="adm")

    def rename_chat(self):
        if not self.groupe:
            users = self.users.all()
            self.name = f"{users[0]} - {users[1]}"
        self.save()

    def __str__(self):
        return self.name  
    
    def changeStatus(self, status, user):
        message = Message.objects.filter(chat=self).filter(type='normal').last()
        if message:
            if message.user != user:
                if message.status == 'sent' and status == 'delivered':
                    message.status = 'delivered'
                    message.save()
                elif message.status == 'delivered' and status == 'received':
                    message.status = status
                    message.save()
                    msgs = Message.objects.filter(chat=self, type='normal')
                    msgs = msgs.exclude(status=status)
                    for msg in msgs:
                        msg.status = status
                        msg.save()
                return message.user.username
        
    
    def is_adm(self, user:User):
        return self.adm == user
    
    def get_messages(self):
        paris_timezone = pytz.timezone('Europe/Paris')
        messages = Message.objects.filter(chat=self).order_by('timestamp')
        if messages:
            for msg in messages:
                msg.timestamp = msg.timestamp.astimezone(paris_timezone)
        return messages
    
    def get_absolute_url(self):
        return reverse("chat:handleGr", args=[str(self.uuid)])


class Message(models.Model):
    typeChoices = [
                ('Info', 'info'),  
                ('Create', 'create'),  
                ("Join", "join"), 
                ("Left", "left"), 
                ("Normal", "normal")]
    statusChoices = [
                ('sent', 'Sent'),  
                ('Delivered', 'delivered'),  
                ("Received", "received"), ]

    type = models.CharField(choices=typeChoices, default='normal', max_length=6)
    status = models.CharField(choices=statusChoices, default='sent', max_length=9)
    text = models.TextField(blank=False, max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
        
