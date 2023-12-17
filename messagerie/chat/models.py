from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# Create your models here.
# class Utilisateur(AbstractUser, models.Model):
#     nom = models.CharField(max_length=30, blank=False)
#     num_tel = models.CharField(max_length=15, blank=False)
#     info = models.TextField(blank=True, max_length=200)

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['nom', 'num_tel'], name="%(app_label)s_%(class)s_unique")
#         ]

#     def __str__(self):
#         return self.nom


class Message(models.Model):
    texte = models.TextField(blank=False, max_length=2000)
    date = models.DateField(auto_now_add=True)
    heure = models.TimeField(auto_now_add=True)
    util = models.ForeignKey('Utilisateur', on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)

    def __str__(self):
        return self.texte[:100]


class Chat(models.Model):
    util_1 = models.ForeignKey('Utilisateur', to_field='id', on_delete=models.CASCADE, related_name="chat_util_1")
    util_2 = models.ForeignKey('Utilisateur', to_field='id', on_delete=models.CASCADE, related_name="chat_util_2")
   
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['util_1', 'util_2'], name="%(app_label)s_%(class)s_unique")
        ]

    def __str__(self):
        return f"{self.util_1} - {self.util_2}"
    
    def get_messages(self):
        return Message.objects.filter(chat=self)
    
