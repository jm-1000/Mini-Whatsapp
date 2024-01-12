from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse
from django.views import View
from .models import User, Chat
from .forms import MessageForm, GroupForm
import pytz

# Create your views here.
class LoginRequired(LoginRequiredMixin):
    login_url = "/compte/login"


class GetIndexView(LoginRequired, View):
    def get(self, request):
        return render( request, 'chat/chat.html', {})
    
class GetChatView(LoginRequired, View):
    def get(self, request):
        latestMsgs = []
        paris_timezone = pytz.timezone('Europe/Paris')
        for chat in request.user.get_chats():
            msg = chat.get_messages().last()
            if msg:
                msg.timestamp = msg.timestamp.astimezone(paris_timezone)
                latestMsgs.append(msg)
        latestMsgs = sorted(latestMsgs, key=lambda x:x.timestamp, reverse=True)
        return render(request, 'chat/getChat.html', {'messages':latestMsgs})
    

class CreateChatView(LoginRequired, View):
    def get(self, request):
        users = User.objects.exclude(id=request.user.id).order_by('username')
        return render(request, 'chat/createChat.html', {'users': users,
                                                        'group': GroupForm()})


class HandleChatView(LoginRequired, View):
    def get(self, request, uuid):
        users = User.objects.exclude(id=request.user.id)
        chat = Chat.objects.get(uuid=uuid)
        if request.user in chat.users.all():
            messages = []
            for msg in chat.get_messages():
                dictMsg = {'date':str(msg.timestamp.date()), 'content':msg}
                messages.append(dictMsg)
            return render(request, 'chat/handleChat.html', {'messages':messages,
                                                            'chat':chat,
                                                            'users':users})
        return HttpResponse('''<div class='divtemp'> <p>Vous n'avez plus accès
                             à ce chat ou groupe</p></div>''')


class HandleGroupView(LoginRequired, View):
    def get(self, request, uuid):
        group = Chat.objects.get(uuid=uuid)
        return render(request, 'chat/chat.html', {  
            'message': MessageForm(initial={'chat':group.id}),
            'chat':group})

