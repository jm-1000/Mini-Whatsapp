from django.db.utils import IntegrityError
from django.test import TestCase, Client
from .models import Utilisateur
from django.urls import reverse

# Create your tests here.
class Creer_supprimer_users(TestCase):
    def setUp(self):
        self.client = Client(headers={"user-agent": "curl/7.7"})

    def test_model_user(self):
        Utilisateur.objects.create_superuser('adm', '', 'x')
        Utilisateur.objects.create_user('james','','user',info='ola people!')
        try : Utilisateur.objects.create_user('adm', '', 'y')
        except IntegrityError: pass
    
    def test_client_web(self):
        payloads =[{'username': 'adm', 'password':'testpass'}, {'username': 'adm', 'password':'x'}]
        status = [302, 200]
        for i in range(len(payloads)):
            reponse = self.client.post(reverse('createUser'), payloads[i])
            self.assertEqual(reponse.status_code, status[i])
      

class Login_user(TestCase):
    def setUp(self):
        self.client = Client(headers={"user-agent": "curl/7.7"})
        self.user = Utilisateur.objects.create_user('test', '', 'passtest')

    def test_redirection(self):
        name_urls = ["index","deleteUser"]
        for name in name_urls:
            reponse = self.client.get(reverse(name))
            self.assertEqual(reponse.status_code, 302)

    def test_login(self):
        creds = [{"username":"test", "password":"passtest"}, {"username":"anonymous", "password":"x"}]
        status = [302, 200]
        for i in range(len(creds)):
            reponse = self.client.post(reverse('login'),creds[i])
            self.assertEqual(reponse.status_code, status[i])
    

    
            

    