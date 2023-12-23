from collections.abc import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


# Create your models here.
User = get_user_model()

class Message(models.Model):
    text = models.TextField(blank=False, max_length=2000)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:100]

class Chat(models.Model):
    name = models.CharField(max_length=30, blank=True)
    groupe = models.BooleanField(default=False)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name  
    
    def get_messages(self):
        return Message.objects.filter(chat=self)
    
    def get_or_create(user, req_user):
        chat = Chat.objects.filter(users=user).filter(users=req_user).filter(groupe=False)
        if len(chat) == 0:
            chat = Chat.objects.annotate(num_utilisateurs=models.Count('users')).filter(num_utilisateurs=0)
            if len(chat) == 0:
                return Chat.objects.create()
        return chat[0]



        
