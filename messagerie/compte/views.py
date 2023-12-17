from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required(login_url='./login')
def index(request):
    return render(request, 'index.html', {'user':request.user})

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})
    
    def post(self, request):
        passwd = request.POST['passwd']
        username = request.POST['username']
        user = authenticate(request, username=username, password=passwd)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('login')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')