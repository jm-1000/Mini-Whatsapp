from django.test import TestCase
from .models import *
import random

# Create your tests here.
class creer_instances(TestCase):
    ju=Utilisateur(nom='juari',num_tel='+12345456',info='hi people!')
    man=Utilisateur(nom='manuel',num_tel='+00999999',info='ola people!')
    fra=Utilisateur(nom='francis',num_tel='+0544999',info='salut!')
    ju.save()
    man.save()
    fra.save()
    c1=Chat(util_1=ju,util_2=man)
    c2=Chat(util_1=fra,util_2=man)
    c3=Chat(util_1=ju,util_2=fra)
    c1.save()
    c2.save()
    c3.save()
    # m1=Message(texte='msg 1',util=ju,chat=c1)
    # m2=Message(texte='msg 2',util=man,chat=c1)
    # m1.save()
    # m2.save()
    getRandom = lambda x: x[random.randint(0,len(x)-1)]
    for i in range(10):
        u = getRandom([man,ju,fra])
        Message(texte=f'{u} : msg {i}',util=u, chat=getRandom([c1,c2,c3])).save()
    
    print()





    # alias test="rm db.sqlite3;python3 manage.py makemigrations;python3 manage.py migrate >/tmp/.null;echo '';python3 manage.py test"