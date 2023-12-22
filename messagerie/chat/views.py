from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .models import Users, Message, Chat
from .forms import MessageForm, GroupForm

# Create your views here.
class LoginRequired(LoginRequiredMixin):
    login_url = "/compte/login"


class GetChatView(LoginRequired, View):
    def get(self, request):
        return render(request, 'chat/chat.html', {'chats':request.user.get_chats()})
    

class CreateChatView(LoginRequired, View):
    def get(self, request):
        users = Users.objects.exclude(id=request.user.id)
        return render(request, 'chat/chat.html', {'users': users})
    

class CreateMessageView(LoginRequired, View):
    def get(self, request, pk):
        if pk != request.user.id:
            requested_user = Users.objects.get(pk=pk)
            chat = Chat.get_or_create(Chat, user=request.user, req_user=requested_user)
            return render(request, 'chat/chat.html', {'message': MessageForm(initial={'chat':chat})})
        return redirect('chat:createChat')

    def post(self, request, pk):
        requested_user = Users.objects.get(pk=pk)
        data = request.POST
        chat = Chat.objects.get(id=data['chat'])
        if chat.utilisateurs.count() == 0:
            chat.utilisateurs.add(requested_user, request.user)
        if chat.utilisateurs.count() == 2:
            Message(texte=data['texte'], util=request.user, chat=chat).save()
        return render(request, 'chat/chat.html', {})
    

class CreateGroupView(LoginRequired, View):
    def get(self, request):
        return render(request, 'chat/chat.html', {'group': GroupForm()})

    def post(self, request):
        data = dict(request.POST)
        if data['nom_groupe'] != '':
            chat = Chat.objects.create(nom_groupe=data['nom_groupe'], groupe=True)
            chat.utilisateurs.add(request.user) 
            for id in data['utilisateurs']:
                chat.utilisateurs.add(Users.objects.get(id=id)) 
            return render(request, 'chat/chat.html', {})
        return redirect('chat:createChat')
