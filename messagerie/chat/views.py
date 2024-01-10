from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from .models import User, Message, Chat
from .forms import MessageForm, GroupForm
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
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
                if (msg.type == 'normal' and msg.user != request.user and 
                    msg.status != 'delivered'):
                    msg.status = 'delivered'
                    msg.save()
                    sendToConsumers(chat.uuid, msg.user)
                latestMsgs.append(msg)
        latestMsgs = sorted(latestMsgs, key=lambda x:x.timestamp, reverse=True)
        return render(request, 'chat/getChat.html', {'messages':latestMsgs})
    

class CreateChatView(LoginRequired, View):
    def get(self, request):
        users = User.objects.exclude(id=request.user.id)
        return render(request, 'chat/createChat.html', {'users': users,
                                                        'group': GroupForm()})
    

class HandleChatView(LoginRequired, View):
    def get(self, request, uuid):
        users = User.objects.exclude(id=request.user.id)
        chat = Chat.objects.get(uuid=uuid)
        if request.user in chat.users.all():
            messages = []
            for msg in chat.get_messages():
                if (msg.type == 'normal' and msg.status != 'received' and 
                    msg.user != request.user):
                    msg.status = 'received'
                    msg.save()
                    sendToConsumers(chat.uuid, msg.user)
                dictMsg = {'date':str(msg.timestamp.date()), 'content':msg}
                messages.append(dictMsg)
            return render(request, 'chat/handleChat.html', {'messages':messages,
                                                            'chat':chat,
                                                            'users':users})
        return HttpResponse('''<div class='divtemp'> <p>Vous n'avez plus accès
                             à ce chat ou groupe</p></div>''')



def sendToConsumers(uuid, user):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('user-' + str(user), {
                                             'type':'sendToChat', 
                                             'action':'changeChat', 
                                             'chat':str(uuid), 'status':'' })
#     def post(self, request, pk):
#         target_user = User.objects.get(pk=pk)
#         data = request.POST
#         chat = Chat.objects.get(id=data['chat'])
#         while True:
#             chat_users= chat.users.all()
#             if len(chat_users) == 0:
#                 chat.adm = request.user
#                 chat.users.add(target_user, request.user)
#             elif len(chat_users) == 2 and request.user in chat_users and target_user in chat_users:
#                 break
#             chat = Chat.get_or_create(user=request.user, req_user=User.objects.get(pk=pk))
#         Message(text=data['text'], user=request.user, chat=chat).save()
#         return redirect('chat:handleChat', target_user.id)
        
    

# class CreateGroupView(LoginRequired, View):
#     def get(self, request):
#         users = User.objects.exclude(id=request.user.id)
#         return render(request, 'chat/chat.html', {'group': GroupForm(), 'users':users})

#     def post(self, request):
#         id_users = dict(request.POST)['users']
#         name_group = request.POST['name'].capitalize()
#         if name_group != '':
#             chat,_ = Chat.objects.get_or_create(name=name_group, groupe=True)
#             chat.users.add(request.user) 
#             chat.adm = request.user
#             for id in id_users:
#                 chat.users.add(User.objects.get(id=id)) 
#             return redirect('chat:handleGr', chat.pk)
#         return redirect('chat:createChat')



class HandleGroupView(LoginRequired, View):
    def get(self, request, uuid):
        group = Chat.objects.get(uuid=uuid)
        return render(request, 'chat/chat.html', {  
            'message': MessageForm(initial={'chat':group.id}),
            'chat':group})
    
#     def post(self, request, pk):
#             group = Chat.objects.get(pk=request.POST['chat'])
#             Message(text=request.POST['text'], user=request.user, chat=group).save()
#             return redirect('chat:handleGr', group.id)
    
    
# class DeleteChatView(LoginRequired, View):
#     def get(self, request, pk):
#         chat = Chat.objects.get(pk=pk)
#         if chat.adm == request.user:
#             chat.delete()
#         elif request.user in chat.users.all():
#             chat.users.remove(request.user)
#         return redirect('chat:getChat')