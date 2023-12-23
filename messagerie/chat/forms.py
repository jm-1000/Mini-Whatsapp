from django.core.validators import RegexValidator
from django import forms
from .models import Message, User, Chat

class MessageForm(forms.ModelForm):
    chat = forms.IntegerField(required=True)
    class Meta:
        model = Message
        fields = [
            'text',
            'chat'
        ]

class GroupForm(forms.ModelForm):
    name = forms.CharField(required=True)
    class Meta:
        model = Chat
        fields = [
            'name',
            'users'
        ]
    
        
        
    
    