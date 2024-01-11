from channels.generic.websocket import AsyncWebsocketConsumer
import json, time
from channels.db import database_sync_to_async as db_query 
from .models import Chat, User, Message
import pytz

class GetWebSocket(AsyncWebsocketConsumer):
    connectedUsers = []
    async def connect(self):
        if str(self.scope['user']) != "AnonymousUser":
            self.user = await self.get_user()
            if self.user:
                await self.accept()
                await self.channel_layer.group_add( "user-" + str(self.user), 
                    self.channel_name)
                await self.send(json.dumps({'action':'getChats'}))
                self.connectedUsers.append(str(self.user))
                await self.sendStatusUser(True)
                print(self.user, time.ctime())
        


    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        action = data['action']
        # print(action)
        if action == 'connect':
            self.chat = await db_query(Chat.objects.get)(uuid=data['uuid'])
            await self.channel_layer.group_add(str(self.chat.uuid), 
                                               self.channel_name)
        
        if action == 'disconnect':
            try:
                self.chat = await db_query(Chat.objects.get)(uuid=data['uuid'])
                await self.channel_layer.group_discard(str(self.chat.uuid), 
                                                   self.channel_name)
            except: pass

        elif action == 'userConnected':
            self.chat = await db_query(Chat.objects.get)(uuid=data['uuid'])
            await self.sendStatusUser()

        elif action == 'message':
            self.chat = await db_query(Chat.objects.get)(uuid=data['uuid'])
            if await db_query(lambda x,y: x in y.users.all())(self.user, 
                                                              self.chat):
                await self.handleMsg(data['text'])
            
        elif action == 'createChat':
            await self.createChat(data['usernames'])
            # await self.createChat(data['username'])
            
        elif action == 'createGr':
            await self.createGr(data['text'], data["usernames"])
            # await self.createGr(data['namegr'], data["usernames"])
        
        elif action == 'renameGr':
            await self.manageChat(data['uuid'], data['text'])
            # await self.manageChat(data['uuid'], data['namegr'])

        elif action == 'addUsersGr':
            await self.manageChat(data['uuid'], usernames=data['usernames'])
        
        elif action == 'deleteUserGr':
            await self.manageChat(data['uuid'], usernames=data['usernames'], 
            # await self.manageChat(data['uuid'], usernames=data['username'], 
                                  delete=True)
        
        elif action == 'deleteGr':
            await self.manageChat(data['uuid'], delete=True)


    async def handleMsg(self, text=None, type='normal', username=None, 
                        action='message', uuid=None):
        if action == 'userConnected' : chat = uuid 
        else: chat = str(self.chat.uuid)
        if text and not username:
            if text.isspace(): return 0
            self.message = await db_query(Message.objects.create)(
                                user = self.user,
                                type = type,
                                text = text,
                                chat = self.chat )
            chat = str(self.message.chat.uuid)
        group = chat
        if username: group = f'user-{username}'
        await self.channel_layer.group_send(group, 
                {"type":"sendToChat",
                'action': action,
                "chat": chat,
                'status': text })


    async def createChat(self, username):
        user = await self.get_user(username)
        self.chat = await db_query(self.user.get_or_create_chat)(user.id)
        await self.channel_layer.group_add(str(self.chat.uuid), 
                                           self.channel_name)
        await self.connectChat('newChat', [username])


    async def createGr(self, namegr, usernames):
        self.chat = await db_query(self.user.create_group)(
                    namegr[0].upper() + namegr[1:], usernames)
        await self.channel_layer.group_add(str(self.chat.uuid), 
                                           self.channel_name)
        text = f'{str(self.user).capitalize()} vous a ajouté dans ce groupe.'
        await self.handleMsg(text, 'join')
        text = f'Vous avez créé ce groupe.'
        await self.handleMsg(text, 'create')
        await self.connectChat(usernames=usernames)
        
        
        
    async def connectChat(self, action='message', usernames=None):
        data = {
            'chat': str(self.chat.uuid),
            'action': 'createChat' }   
        await self.send(json.dumps(data))
        for name in usernames + [str(self.user)]:
            await self.handleMsg(username=name, action=action)


    async def sendToChat(self, event):
        data = {
            'chat': event['chat'],
            'action': event['action'],
            'status': event['status'] }   
        await self.send(json.dumps(data))
           

    async def manageChat(self, uuid, namegr=None, usernames=None, 
                         delete=False):
        self.chat = await db_query(Chat.objects.get)(uuid=uuid)
        if await db_query(self.chat.is_adm)(self.user):
            if namegr and namegr!=self.chat.name:
                text = f"Le nom du groupe est passé de '{self.chat}' à '{namegr}'."
                self.chat.name = namegr[0].upper() + namegr[1:]
                await db_query(self.chat.save)()
                await self.handleMsg(text, 'info')
                await self.handleMsg(action='changeChat')

            elif usernames and not delete:
                text1 = lambda x: f'{str(self.user).capitalize()} a ajouté {x.capitalize()} dans le groupe.'
                text2 = lambda x: f'Vous avez ajouté {x.capitalize()} dans le groupe.'
                for name in usernames:
                    try:
                        user = await self.get_user(name)
                        await db_query(self.chat.users.add)(user)
                        await self.handleMsg(text1(name), 'join')
                        await self.handleMsg(text2(name), 'create')
                        await self.handleMsg(username=name)
                    except: print('Error adding')
                await self.handleMsg(action='changeChat')

            elif usernames and delete:
                text1 = lambda x: f'{str(self.user).capitalize()} a supprimé {x.capitalize()} du groupe.'
                text2 = lambda x: f'Vous avez supprimé {x.capitalize()} du groupe.'
                try:
                    user = await self.get_user(usernames)
                    await db_query(self.chat.users.remove)(user)
                    await self.handleMsg(text1(usernames), 'left')
                    await self.handleMsg(text2(usernames), 'create')
                    await self.handleMsg(action='changeChat')
                    await self.handleMsg(username=usernames, action='deleteChat')
                except: print('Error deleting')

            elif delete:
                users = await db_query(self.chat.users.all)()
                usernames = await db_query(lambda x: [str(user) for user in x])(users)
                for name in usernames + [str(self.user)]:
                    await self.handleMsg(username=name, action='deleteChat')
                await db_query(self.chat.delete)()

        elif delete:
            if await db_query(lambda x,y: x in y.users.all())(self.user, self.chat):
                if self.chat.groupe:
                    text = lambda x: f'{x.capitalize()} a sorti du groupe.'
                    await self.handleMsg(text(str(self.user)), 'left')
                    await db_query(self.chat.users.remove)(self.user)
                    await self.handleMsg(action='changeChat')
                else:
                    usernames = await db_query(lambda x: [str(y) for y in x.users.all()])(self.chat)
                    for name in usernames :
                        await self.handleMsg(username=name, action='deleteChat')
                    await db_query(self.chat.delete)()

    async def sendStatusUser(self, all=None):
        paris_timezone = pytz.timezone('Europe/Paris')
        getUser2 = lambda x, y: x[1] if y != x[1] else x[0]
        if all:
            chats = await db_query(self.user.get_chats)(group=False)
            chats = await db_query(lambda x: [[str(y), 
                                               str(y.uuid)] for y in x])(chats)
            for chat in chats:
                if self.user.username in self.connectedUsers:
                    text = "En ligne"
                else:
                    text = str(self.user.last_login.astimezone(paris_timezone))[:16]
                user = getUser2((chat[0]).split(' - '), self.user.username)
                await self.handleMsg(text, username=user, action='userConnected', 
                                     uuid=chat[1])
        
        elif not self.chat.groupe:
            user = getUser2(str(self.chat).split(' - '), self.user.username)
            if user in self.connectedUsers:
                await self.send(json.dumps({'action':'userConnected', 
                                            'status': "En ligne",
                                            'chat': str(self.chat.uuid) }))
            else:
                user = await self.get_user(user)
                await self.send(json.dumps({'action':'userConnected', 
                                            'status': str(user.last_login.astimezone(paris_timezone))[:16],
                                            'chat': str(self.chat.uuid) }))

    @db_query
    def get_user(self, username=None):
        if username: return User.objects.get(username=username)
        return User.objects.get(username=self.scope['user'])


    async def disconnect(self, code):
        self.connectedUsers.remove(str(self.user))
        await self.sendStatusUser(True)
        print(time.ctime())


'''
elif action == 'createChat':
            # await self.createChat(data['usernames'])
            await self.createChat(data['username'])
            
        elif action == 'createGr':
            # await self.createGr(data['text'], data["usernames"])
            await self.createGr(data['namegr'], data["usernames"])
        
        elif action == 'renameGr':
            # await self.manageChat(data['uuid'], data['text'])
            await self.manageChat(data['uuid'], data['namegr'])

        elif action == 'addUsersGr':
            await self.manageChat(data['uuid'], usernames=data['usernames'])
        
        elif action == 'deleteUserGr':
            # await self.manageChat(data['uuid'], usernames=data['usernames'], 
            await self.manageChat(data['uuid'], usernames=data['username'], 
                                  delete=True)

'''
