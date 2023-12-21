from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


# Create your models here.
Utilisateur = get_user_model()

class Message(models.Model):
    texte = models.TextField(blank=False, max_length=2000)
    date = models.DateField(auto_now_add=True)
    heure = models.TimeField(auto_now_add=True)
    util = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)

    def __str__(self):
        return self.texte[:100]


class Chat(models.Model):
    nom_groupe = models.CharField(max_length=30, blank=True)
    groupe = models.BooleanField(default=False)
    utilisateurs = models.ManyToManyField(Utilisateur)

    def clean(self):
        nb_users = self.utilisateurs.count()
        if self.groupe:
            if self.nom_groupe == '':
                raise ValidationError('Un groupe doit avoir un nom.')
            if nb_users < 1:
                raise ValidationError('Un groupe doit avoir au moins un utilisateur.')
        elif nb_users != 2:
            raise ValidationError('Un chat doit avoir que 2 utilisateurs.')

    def __str__(self):
        return self.nom_groupe  
    
    def get_messages(self):
        return Message.objects.filter(chat=self)
    
