from django.shortcuts import render, redirect
from .models import Item, Consumer
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from datetime import datetime

def ipInfo(addr=''):
    from urllib.request import urlopen
    from json import load
    if addr == '':
        url = 'https://ipinfo.io/json'
    else:
        url = 'https://ipinfo.io/' + addr + '/json'
    res = urlopen(url)
    #response from url(if res==None then check connection)
    data = load(res)
    #will load the json response into data
    for attr in data.keys():
        #will print the data line by line
        print(attr,' '*13+'\t->\t',data[attr])
    return data


def index(request):
    return render(request, 'index.html')

def register(request, sku):
    #register with sku in url
    
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    ip = get_client_ip(request)
    print(ip)
    ipCall = ipInfo(ip)
    city = ipCall['city']

    items = Item.objects.all()
    
    if request.method == 'POST':
       
        print(request.POST)
        print(ipCall)
        registeredSku = request.POST.get('inputSku',"")
        email = request.POST.get('email',"")
        username = email 
       
        password = request.POST.get('inputPassword',"")
        first_name = request.POST.get('first_name',"")
        last_name = request.POST.get('last_name',"")
        country = ipCall['country']
        city = request.POST.get('city', "city")
        where = ipCall['region']
        when = datetime.now()
        telephone = request.POST.get('telephone', '')
        getInfo = request.POST.get('getInfo', 'Off')
        
        if getInfo == 'on':
            getInfo = True
        else:
            getInfo = False
        #item must exist in db
        item=items.get(sku=registeredSku)
        
        #if user does not exist, create new user, if user exist, request login, if session authenticated, continue
        if request.user.is_authenticated:
            user = request.user
            pass
        else:
            user = User.objects.create_user(username,email,password)
            user.first_name = first_name
            user.last_name = last_name
            user.email_address = email
            user.save()

        #create consumer registration
        newConsumer = Consumer(user_id=user,sku=item, where=where,when=when,country=country,city=city,getInfo=getInfo )
        newConsumer.save()

        #inform user everything saved ok and direct to profile to view registered products
        return redirect('profile')


    context = {'sku': sku, 'city': city}  

    return render(request, 'britishdenim/registration.html', context)

def contact(request):

    return render(request, 'britishdenim/contact.html')





