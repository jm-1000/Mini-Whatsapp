from collections.abc import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


# Create your models here.
Users = get_user_model()

class Message(models.Model):
    texte = models.TextField(blank=False, max_length=2000)
    date = models.DateField(auto_now_add=True)
    heure = models.TimeField(auto_now_add=True)
    util = models.ForeignKey(Users, on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)

    def __str__(self):
        return self.texte[:100]

class Chat(models.Model):
    nom_groupe = models.CharField(max_length=30, blank=True)
    groupe = models.BooleanField(default=False)
    utilisateurs = models.ManyToManyField(Users)

    def __str__(self):
        return self.nom_groupe  
    
    def get_messages(self):
        return Message.objects.filter(chat=self)
    
    def get_or_create(self, user, req_user):
        chat = self.objects.filter(
             models.Q(utilisateurs=user) & 
             models.Q(utilisateurs=req_user) &
             models.Q(groupe=False)
            )
        if len(chat) == 0:
            return self.objects.create()
        else: return chat[0]

        
