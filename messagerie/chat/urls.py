
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
import uuid 

app_name = 'chat'
urlpatterns = [
    path('', GetIndexView.as_view(), name='indexChat'),
    path('chat/', GetChatView.as_view(), name='getChat'),
    path('chat/<uuid:uuid>', HandleChatView.as_view(), name='handleChat'),
    path('chat/create/', CreateChatView.as_view(), name='createChat')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)