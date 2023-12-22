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
            chat1 = Chat(nom_groupe='G1', groupe=True)
            chat2 = Chat()
            chat4 = Chat(groupe=True)
            chat2.save()
            chat1.save()
            chat4.save()
            chat4.utilisateurs.add(self.james, self.luis, self.john)
            chat1.utilisateurs.add(self.james, self.luis, self.daniel, self.john)
            chat2.utilisateurs.add(self.james)


class Creer_message(Creer_users, TestCase):
    def test_model_message(self):
        chats = []
        for i in range(3):
            chat = Chat.objects.create()
            chat.save()
            chats.append(chat)
        chats[0].utilisateurs.add(self.james, self.luis, self.daniel, self.john)
        chats[2].utilisateurs.add(self.james, self.daniel)
        chats[1].utilisateurs.add(self.john, self.luis)
        getRandom = lambda x: x[randint(0,len(x)-1)]
        for chat in chats*10:
            util = getRandom(chat.utilisateurs.all())
            Message(texte=f'{util} : msg {randint(0, 100)}', util=util, chat=chat).save()
        # for chat in chats:
            # print(chat.get_messages())
    
# class Creer_chat(TestCase):
#         user_modal = get_user_model()
#         james = user_modal.objects.create_user('james','','x')
#         luis = user_modal.objects.create_user('luis','','x')
#         daniel = user_modal.objects.create_user('daniel','','x')
#         john = user_modal.objects.create_user('john','','x')
#         james.save()
#         luis.save()
#         daniel.save()
#         john.save()
#         chat1 = Chat(nom_groupe='G1', groupe=True)
#         chat2 = Chat(nom_groupe='G2', groupe=True)
#         chat4 = Chat(nom_groupe='G3', groupe=True)
#         chat2.save()
#         chat1.save()
#         chat4.save()
#         chat4.utilisateurs.add(james, luis, john, daniel)
#         chat1.utilisateurs.add(james, luis, daniel)
        # chat2.utilisateurs.add(john, daniel)
        
        # getRandom = lambda x: x[randint(0,len(x)-1)]
        # for chat in Chat.objects.all():
        #     for i in range(0, randint(5,20)):
        #         util = getRandom(chat.utilisateurs.all())
        #         Message(texte=f'{util} : msg {randint(0, 100)}', util=util, chat=chat).save()