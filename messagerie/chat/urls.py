from django.urls import path
from .views import *
import uuid 

app_name = 'chat'
urlpatterns = [
    path('', GetIndexView.as_view(), name='indexChat'),
    path('chat/', GetChatView.as_view(), name='getChat'),
    path('chat/<uuid:uuid>', HandleChatView.as_view(), name='handleChat'),
    path('chat/create/', CreateChatView.as_view(), name='createChat'),
    # path('create/<int:pk>', HandleChatView.as_view(), name='handleChat'),
    # path('create/group/', CreateGroupView.as_view(), name='createGr'),
    # path('create/group/<uuid:uuid>', HandleGroupView.as_view(), name='handleGr'),
    # path('delete/<int:pk>', DeleteChatView.as_view(), name='deleteChat'),
]