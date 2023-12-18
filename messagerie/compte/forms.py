from django.core.validators import RegexValidator
from django import forms
from .models import Utilisateur

class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'Utilisateur")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput())


class CreateUtilisateurForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Ex : +33746666666"
    )
    num_tel = forms.CharField(validators=[phone_regex], max_length=17, required=False, label="Téléphone")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput())
    username = forms.CharField()
    class Meta:
        model = Utilisateur
        fields = [
            'username',
            'email',
            'num_tel',
            'password',
            'info'
        ]

    def update(self, user):
        data = self.data
        user.username = data['username']
        user.email = data['email']
        user.num_tel = data['num_tel']
        user.info = data['info']
        user.set_password(data['password'])
        user.save()
        
        
    
    