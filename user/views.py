from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from britishdenim.models import Item, Consumer
from user.models import Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.models import User

# Create your views here.

@login_required
def profile(request):

    items = Item.objects.all()
    consumer = Consumer.objects.filter(user_id=request.user)

    context = {'items': items, 'consumer': consumer}

    return render(request, 'user/profile.html', context)


def signin(request):
    if request.method == 'POST':
        print(request.POST)
        email =request.POST.get('username')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if password != password1:
                messages.error(request, 'Error, revisa que la contraseña sea igual a la confirmacion.')
                return render(request,  'user/signin.html')
        try:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Error: Correo ya registrado, intenta nuevamente con otro correo.')
                return render(request, 'user/signin.html')
            newUser = User.objects.create_user(username, email, password)
            newUser.first_name = first_name
            newUser.last_name = last_name
            newUser.save()
        except Exception as e:
            print(e)
            messages.error(request, 'Error en el registro intenta nuevamente con otro usuario.')
            return render(request, 'user/signin.html')

        newProfile = Profile.objects.create(user=newUser)
        newProfile.save()

        auth = authenticate(request, username=username, password=password)
        if auth:
            login(request, auth)
            messages.success(request, f'Welcome {auth.first_name}, you are logged in.')
            return redirect('profile')

    
    return render(request, 'user/signin.html')


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
