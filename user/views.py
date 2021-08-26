from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SigninForm
from britishdenim.models import Item, Consumer
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views import View

# Create your views here.

@login_required
def profile(request):

    items = Item.objects.all()
    consumer = Consumer.objects.filter(user_id=request.user)

    context = {'items': items, 'consumer': consumer}

    return render(request, 'user/profile.html', context)


def signin(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            
            form.save()
            
            return redirect('login')
    else:
        form = SigninForm()
    return render(request, 'user/signin.html', {'form':form})


class LoginView(View):
    def get(self, request):

        return render(request, 'user/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        auth = authenticate(request, username=username, password=password)
        if auth:
            login(request, auth)
            messages.success(request, f'Welcome {auth.first_name}, you are logged in.')
            return redirect('profile')
        else:
            messages.error(request, "Wrong credentials please try again.")
            return redirect('login')
