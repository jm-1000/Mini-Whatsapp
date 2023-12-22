from django.urls import path
from .views import *

app_name = 'chat'
urlpatterns = [
    path('', GetChatView.as_view(), name='getChat'),
    path('create/', CreateChatView.as_view(), name='createChat'),
    path('create/<int:pk>', CreateMessageView.as_view(), name='createMsg'),
    path('create/group/', CreateGroupView.as_view(), name='createGr'),
]