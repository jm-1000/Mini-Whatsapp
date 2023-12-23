from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .models import User, Message, Chat
from .forms import MessageForm, GroupForm

# Create your views here.
class LoginRequired(LoginRequiredMixin):
    login_url = "/compte/login"


class GetChatView(LoginRequired, View):
    def get(self, request):
        # Chat.objects.filter(id__gt=10).delete()
        return render(request, 'chat/chat.html', {'chats':request.user.get_chats()})
    

class CreateChatView(LoginRequired, View):
    def get(self, request):
        users = User.objects.exclude(id=request.user.id)
        return render(request, 'chat/chat.html', {'users': users})
    

class HandleChatView(LoginRequired, View):
    def get(self, request, pk):
        if pk != request.user.id:
            chat = Chat.get_or_create(user=request.user, req_user=User.objects.get(pk=pk))
            return render(request, 'chat/chat.html', {'message': MessageForm(initial={'chat':chat.id})})
        return redirect('chat:createChat')

    def post(self, request, pk):
        target_user = User.objects.get(pk=pk)
        data = request.POST
        chat = Chat.objects.get(id=data['chat'])
        while True:
            chat_users= chat.users.all()
            if len(chat_users) == 0:
                chat.users.add(target_user, request.user)
            elif len(chat_users) == 2 and request.user in chat_users and target_user in chat_users:
                break
            chat = Chat.get_or_create(user=request.user, req_user=User.objects.get(pk=pk))
        Message(text=data['text'], user=request.user, chat=chat).save()
        return redirect('chat:handleChat', target_user.id)
        
    

class CreateGroupView(LoginRequired, View):
    def get(self, request):
        return render(request, 'chat/chat.html', {'group': GroupForm()})

    def post(self, request):
        id_users = dict(request.POST)['users']
        name_group = request.POST['name'].capitalize()
        if name_group != '':
            chat,_ = Chat.objects.get_or_create(name=name_group, groupe=True)
            chat.users.add(request.user) 
            for id in id_users:
                chat.users.add(User.objects.get(id=id)) 
            return redirect('chat:handleGr', chat.pk)
        return redirect('chat:createChat')



class HandleGroupView(LoginRequired, View):
    def get(self, request, pk):
        group = Chat.objects.get(pk=pk)
        return render(request, 'chat/chat.html', {'message': MessageForm(initial={'chat':group.id})})
    
    def post(self, request, pk):
            group = Chat.objects.get(pk=request.POST['chat'])
            Message(text=request.POST['text'], user=request.user, chat=group).save()
            return redirect('chat:handleGr', group.id)