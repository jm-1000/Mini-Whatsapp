from django.urls import path
from .views import *

app_name = 'chat'
urlpatterns = [
    path('', GetChatView.as_view(), name='getChat'),
    path('create/', CreateChatView.as_view(), name='createChat'),
    path('create/<int:pk>', HandleChatView.as_view(), name='handleChat'),
    path('create/group/', CreateGroupView.as_view(), name='createGr'),
    path('create/group/<int:pk>', HandleGroupView.as_view(), name='handleGr'),
    path('delete/<int:pk>', DeleteChatView.as_view(), name='deleteChat'),
]