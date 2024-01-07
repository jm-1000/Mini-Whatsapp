from collections.abc import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from uuid import uuid4
from django.urls import reverse


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
    
    def to_dict(self):
        return dict(self)
    
    def is_adm(self, user:User):
        return self.adm == user
    
    def get_messages(self):
        return Message.objects.filter(chat=self).order_by('timestamp')
    
    def get_absolute_url(self):
        return reverse("chat:handleGr", args=[str(self.uuid)])


class Message(models.Model):
    Choices = [
                ('Info', 'info'),  
                ('Create', 'create'),  
                ("Join", "join"), 
                ("Left", "left"), 
                ("Normal", "normal")]

    type = models.CharField(choices=Choices, default='normal', max_length=6)
    text = models.TextField(blank=False, max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
        
