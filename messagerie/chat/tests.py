from django.test import TestCase
from .models import *
import random

# Create your tests here.
plen = lambda x:print(len(x),'\n')
class creer_objects(TestCase):
    ju=Utilisateur(nom='juari',num_tel='+12345456',info='hi people!')
    man=Utilisateur(nom='manuel',num_tel='+00999999',info='ola people!')
    fra=Utilisateur(nom='francis',num_tel='+0544999',info='salut!')
    jm=Utilisateur(nom='jmf',num_tel='+0544999345',info='bonjour!')
    ju.save()
    jm.save()
    man.save()
    fra.save()
    c1=Chat(util_1=ju,util_2=man)
    c2=Chat(util_1=fra,util_2=man)
    c3=Chat(util_1=ju,util_2=fra)
    c4=Chat(util_1=man,util_2=jm)
    c4.save()
    c1.save()
    c2.save()
    c3.save()
    getRandom = lambda x: x[random.randint(0,len(x)-1)]
    for c in [c1,c1,c1,c2,c2,c3,c3,c4,c4]:
        u = getRandom([c.util_1,c.util_2])
        Message(texte=f'{u} : msg {c}',util=u, chat=c).save()
    # plen(c1.get_messages())

class remover_objects(TestCase):
    Message.objects.get(id=1).delete()
    Chat.objects.get(id=2).delete()
    Utilisateur.objects.get(id=4).delete()





    # alias test="rm db.sqlite3 2>/dev/null;python3 manage.py makemigrations;python3 manage.py migrate >/tmp/.null;echo '';python3 manage.py test"