from django.core.validators import RegexValidator
from django import forms
from .models import Message, User, Chat

class MessageForm(forms.ModelForm):
    chat = forms.IntegerField(widget=forms.HiddenInput() ,required=True)
    text = forms.Textarea(attrs={'placeholder':'Taper le message...'})
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
    
        
        
    
    