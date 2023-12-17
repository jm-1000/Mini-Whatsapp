from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Utilisateur(AbstractUser):
    num_tel = models.CharField(max_length=15, blank=True)
    info = models.TextField(blank=True, max_length=200)
