from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, LoginForm, UpdateUserForm
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
            user = authenticate(request, username=data['username'].lower(), 
                                password=data['password'])
        if user:
            login(request, user)
            return redirect('chat:indexChat')
        return render(request, 'compte/login.html', {'form':form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('compte:login')


class CreateUserView(View):
    def render_page(self, args): 
        return render(args[0], 'compte/create_user.html', {'form':args[1]})
    
    def get(self, request):
        if request.user.is_authenticated:
            form = UpdateUserForm(instance=request.user)
        else: 
            form = CreateUserForm()
        return self.render_page([request, form])
    
    def post(self, request):
        if request.user.is_authenticated:
            form = UpdateUserForm(request.POST)
            if form.is_valid():
                form.update(request.user)
                login(request, request.user)
                return redirect('chat:indexChat')
            
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(request, username=form.cleaned_data['username'].lower(),
                                password=form.cleaned_data['password'])
            login(request, user)
            return redirect('chat:indexChat')
        return self.render_page([request, form])
        

class DeleteView(View):
    def get(self, request):
        if request.user.is_authenticated:
            request.user.delete()
        return redirect('compte:login')