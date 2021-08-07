from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SigninForm
from britishdenim.models import Item, Consumer

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
            print(form)
            
            form.save()
            
            return redirect('login')

    else:
        form = SigninForm()
    return render(request, 'user/signin.html', {'form':form})
