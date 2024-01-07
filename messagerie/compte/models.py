from django.db import models
from django.contrib.auth.models import AbstractUser
from django.apps import apps


# Create your models here.

class User(AbstractUser):
    num_tel = models.CharField(max_length=15, blank=True)
    info = models.TextField(blank=True, max_length=200)

    def get_chats(self, req_user=None, group=True):
        Chat = apps.get_model('chat', 'Chat')
        if req_user != None:
            return Chat.objects.filter(users=self).filter(users=req_user).filter(groupe=False)
        if not group:
            return apps.get_model('chat', 'Chat').objects.filter(users=self).filter(groupe=group)
        return apps.get_model('chat', 'Chat').objects.filter(users=self)
    
    def get_or_create_chat(self, req_user):
        Chat = apps.get_model('chat', 'Chat')
        chat = self.get_chats(req_user)
        if not chat:
                new_chat = Chat.objects.create()
                new_chat.users.add(self, req_user)
                new_chat.rename_chat()
                return new_chat
        return chat[0]
    
    def create_group(self, namegr, usernames):
        Chat = apps.get_model('chat', 'Chat')
        group = Chat.objects.create(adm=self, name=namegr, groupe=True)
        group.users.add(self)
        for name in usernames:
            group.users.add(User.objects.get(username=name))
        return group

