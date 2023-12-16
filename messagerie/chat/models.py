from django.db import models
from datetime import date
from time import asctime

# Create your models here.
class Utilisateur(models.Model):
    nom = models.CharField(max_length=30, blank=False)
    num_tel = models.CharField(max_length=15, blank=False)
    info = models.TextField(blank=True, max_length=200)

    def __str__(self):
        return self.nom

class Message(models.Model):
    texte = models.TextField(blank=False, max_length=2000)
    date = models.DateTimeField(auto_now_add=True)
    heure = models.TimeField(auto_now_add=True)
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE)

    def __str__(self):
        return self.texte[:100]
    