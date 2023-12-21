from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import *
from random import randint

# Create your tests here.
def detecte_erreur(func, msg):
    try : func.clean()
    except ValidationError: pass
    else: assert False, f"Non detecté : '{msg}'"

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
        detecte_erreur(chat4, 'Un groupe doit avoir un nom.')
        detecte_erreur(chat1, 'Un groupe doit avoir au moins un utilisateur.')
        chat1.utilisateurs.add(self.james, self.luis, self.daniel, self.john)
        chat2.utilisateurs.add(self.james)
        detecte_erreur(chat2, 'Un chat doit avoir que 2 utilisateurs.')
        chat1.clean()


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
            Message(texte=f'{util} : msg {randint(0,100)}', util=util, chat=chat).save()
        # for chat in chats:
            # print(chat.get_messages())
        