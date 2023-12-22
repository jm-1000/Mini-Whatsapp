from django.db import models
from django.contrib.auth.models import AbstractUser
from django.apps import apps


# Create your models here.
class Utilisateur(AbstractUser):
    num_tel = models.CharField(max_length=15, blank=True)
    info = models.TextField(blank=True, max_length=200)

    def get_chats(self):
        all_chats = apps.get_model('chat', 'Chat').objects.all()
        user_chats = []
        for chat in all_chats:
            if self in chat.utilisateurs.all():
                user_chats.append(chat)
        return user_chats