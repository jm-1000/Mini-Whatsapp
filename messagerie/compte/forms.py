from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from django import forms
from .models import User
import re

class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'Utilisateur")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput())

    def clean(self):
        username = self.cleaned_data['username'].lower()
        password = self.cleaned_data['password']
        if username and password:
            if not authenticate(username=username, password=password):
                self.add_error('username', 'Utilisateur ou mot de passe invalide.')
        return self.cleaned_data


class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'num_tel',
            'password',
            'info'
        ]
    
    def clean_username(self,*args,**kwargs):
        username = self.cleaned_data['username']
        regex = r"^[a-zA-Z][a-zA-Z0-9_-]*$"
        try: user = User.objects.get(username=username.lower())
        except: user = None
        if user:
            raise forms.ValidationError('Un utilisateur avec ce nom existe déjà')
        if not username or not re.match(regex, username):
            raise forms.ValidationError('Nom invalide.')
        return username
    
    def clean_num_tel(self,*args,**kwargs):
        tel = self.cleaned_data['num_tel']
        regex=r'^\+?1?\d{9,15}$'
        if tel and not re.match(regex, tel):
            raise forms.ValidationError('Numéro invalide. Ex : +33746666666')
        return tel
    
    def clean_password(self,*args,**kwargs):
        password = self.cleaned_data['password']
        regex = r"^(?=.*[A-Z])(?=.*[a-z]).{6,}$"
        if not password or not re.match(regex, password):
            raise forms.ValidationError('Mot de pass pas assez robuste. Ex : Mo?2pA2s')
        return password


    def save(self):
        user = super(CreateUserForm, self).save(commit=False)
        user.username = self.cleaned_data['username'].lower()
        user.set_password(self.cleaned_data['password'])
        user.save()
        

class UpdateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    class Meta:
        model = User
        fields = [
            'email',
            'num_tel',
            'password',
            'info'
        ]
    
    def clean_num_tel(self,*args,**kwargs):
        tel = self.cleaned_data['num_tel']
        regex=r'^\+?1?\d{9,15}$'
        if tel and not re.match(regex, tel):
            raise forms.ValidationError('Numéro invalide. Ex : +33746666666')
        return tel
    
    def clean_password(self,*args,**kwargs):
        password = self.cleaned_data['password']
        regex = r"^(?=.*[A-Z])(?=.*[a-z]).{6,}$"
        if password and not re.match(regex, password):
            raise forms.ValidationError('Mot de pass pas assez robuste. Ex : Mo?2pA2s')
        return password

    def update(self, user):
        data = self.data
        user.email = data['email']
        user.num_tel = data['num_tel']
        user.info = data['info']
        if data['password']:
            user.set_password(data['password'])
        user.save()
        
        
    
    