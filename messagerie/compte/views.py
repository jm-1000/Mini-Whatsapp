from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import CreateUtilisateurForm, LoginForm
from django.db.utils import IntegrityError


# Create your views here.
@login_required(login_url = '/login')
def index(request):
    return render(request, 'compte/index.html', {'user':request.user})

class LoginView(View):
    def get(self, request):
        return render(request, 'compte/login.html', {'form':LoginForm()})
    
    def post(self, request):
        form, user = LoginForm(request.POST), None
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            return redirect('chat:getChat')
        else:
            return self.get(request)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('compte:login')


class CreateUserView(View):
    def render_page(self, args): 
        return render(args[0], 'compte/create_user.html', {'form':args[1]})
    
    def get(self, request):
        if request.user.is_authenticated:
            form = CreateUtilisateurForm(instance=request.user)
        else: 
            form = CreateUtilisateurForm()
        return self.render_page([request, form])
    
    def post(self, request):
        form = CreateUtilisateurForm(request.POST)
        if request.user.is_authenticated:
            try: 
                form.update(request.user)
                return redirect('compte:login')
            except IntegrityError:
                return self.render_page([request, form]) 
        elif form.is_valid():
            form.save()
            return redirect('compte:login')
        return self.render_page([request, form])
        
class DeleteView(View):
    def get(self, request):
        if request.user.is_authenticated:
            request.user.delete()
        return redirect('compte:login')