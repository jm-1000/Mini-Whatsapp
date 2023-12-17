from django.test import TestCase
from .models import Utilisateur

# Create your tests here.
class creer_superuser(TestCase):
    Utilisateur.objects.all().delete()
    Utilisateur.objects.create_superuser('adm', '', 'adminJM11').save()

class creer_objects(TestCase):
    ju=Utilisateur.objects.create_user('juari','','user',num_tel='+12345456',info='hi people!')
    man=Utilisateur.objects.create_user('manuel','','user',num_tel='+00999999',info='ola people!')
    fra=Utilisateur.objects.create_user('francis','','user',num_tel='+0544999',info='salut!')
    jm=Utilisateur.objects.create_user('jmf','','user',num_tel='+0544999345',info='bonjour!')
    ju.save()
    jm.save()
    man.save()
    fra.save()
