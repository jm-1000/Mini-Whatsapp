from django.db import models
from django.contrib.auth.models import AbstractUser
from django.apps import apps


# Create your models here.
class Utilisateur(AbstractUser):
    num_tel = models.CharField(max_length=15, blank=True)
    info = models.TextField(blank=True, max_length=200)

    def get_chats(self, user=None):
        if user != None:
            return apps.get_model('chat', 'Chat').objects.filter(users=self).filter(users=user).filter(groupe=False)
        return apps.get_model('chat', 'Chat').objects.filter(users=self)