from django.core.validators import RegexValidator
from django import forms
from .models import Message, Users, Chat

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            'texte',
            'chat'
        ]

class GroupForm(forms.ModelForm):
    nom_groupe = forms.CharField(required=True)
    class Meta:
        model = Chat
        fields = [
            'nom_groupe',
            'utilisateurs'
        ]
    
        
        
    
    