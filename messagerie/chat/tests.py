from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import *
from random import randint

# Create your tests here.
class Creer_users(TestCase):
    def setUp(self):
        user_modal = get_user_model()
        self.james = user_modal.objects.create_user('james','','x')
        self.luis = user_modal.objects.create_user('luis','','x')
        self.daniel = user_modal.objects.create_user('daniel','','x')
        self.john = user_modal.objects.create_user('john','','x')

class Creer_chat(Creer_users, TestCase):
        def test_model_chat(self):
            self.james.get_or_create_chat(self.luis.id)
            self.daniel.create_group('GrTest1', [self.james.id, self.luis.id, self.john.id])
                 
    
class Creer_chat(TestCase):
        user_modal = get_user_model()
        Chat.objects.all().delete()
        user_modal.objects.all().delete()
        adm = user_modal.objects.create_superuser('adm','','x')
        james = user_modal.objects.create_user('james','','x')
        luis = user_modal.objects.create_user('luis','','x')
        daniel = user_modal.objects.create_user('daniel','','x')
        john = user_modal.objects.create_user('john','','x')
        
        james.get_or_create_chat(john)
        john.get_or_create_chat(luis)
        daniel.get_or_create_chat(luis)
        
        john.create_group('GrTest1', [james, luis, daniel])
        daniel.create_group('GrTest2', [ luis, john])
        james.create_group('GrTest3', [daniel, luis, john])
        adm.create_group('GrTest4', [daniel, james, luis, john])
        
        getRandom = lambda x: x[randint(0,len(x)-1)]
        for chat in Chat.objects.all():
            for i in range(0, randint(5,20)):
                user = getRandom(chat.users.all())
                Message(text=f'{user} : msg {randint(100, 1000)}', user=user, chat=chat).save()