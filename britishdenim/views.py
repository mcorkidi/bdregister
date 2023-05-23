from django.shortcuts import render, redirect
from .models import Item, Consumer, Scan, Coupon
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.translation import gettext as _
from django.contrib import messages
from django.views import View
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from .serializers import ItemSerializer, LoginSerializer, LogoutSerializer

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
    items = Item.objects.all()
    try: 
        if ipCall['bogon'] ==True:
            print("Invalid IP")
            city = 'City'
            where = 'NotDetected'   
            country = 'NotDetected'
        else:
            city = ipCall['city']
            where = ipCall['region']    
            country = ipCall['country']
    except:
        city = ipCall['city']
        where = ipCall['region']   
        country = ipCall['country']
    when = datetime.now()

    if request.method == 'POST':
       
        print(request.POST)
        print(ipCall)
        registeredSku = request.POST.get('inputSku',"")
        email = request.POST.get('email',"")
        username = email 
       
        password = request.POST.get('inputPassword',"")
        first_name = request.POST.get('first_name',"")
        last_name = request.POST.get('last_name',"")
        
        city = request.POST.get('city', "city")
        
        
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
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Error: Correo ya registrado, intenta nuevamente con otro correo.')
                return render(request, 'britishdenim/registration.html')
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

    if sku == '_':
        pass
    else:
        try: 
            item=items.get(sku=sku)
            if country=='HK' or country=='CN':
                pass
            else:
                newScan = Scan(sku=item,where=where,when=when,country=country,city=city)
                newScan.save()
        except:
            pass

    city = city.replace(" ", "_")    
    context = {'sku': sku, 'city': city}  

    return render(request, 'britishdenim/registration.html', context)

def contact(request):

    return render(request, 'britishdenim/contact.html')

@login_required
def rewards(request):

    coupons = Coupon.objects.all()

    return render(request, 'britishdenim/rewards.html', {'coupons': coupons})

@staff_member_required
def stats(request):
    scans = Scan.objects.all()
    totalScans = scans.count()
    scansByCountry = {}
    for scan in scans:
        if scan.country in scansByCountry:
            scansByCountry[scan.country] += 1
        else:
            scansByCountry[scan.country] = 1
    
    print(scansByCountry)
    context = {'totalScans': totalScans, 'scansByCountry': scansByCountry}
   
    return render(request, 'britishdenim/stats.html', context)

# API VIEWS

class ProductViewSet(viewsets.GenericViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def create(self,request):
    # Override create method to prevent duplicate object creation
        serializer = self.serializer_class(data=self.request.data)

        serializer.is_valid(raise_exception=True)
        sku = serializer.validated_data['sku']
        name = serializer.validated_data['name']
        obj, created = Item.objects.get_or_create(sku=sku, name=name)
        if created:
            obj.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_409_CONFLICT)


class LoginAPIView(viewsets.GenericViewSet,
                   mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth = authenticate(request, username=serializer.data['username'], password=request.data['password'])
        if auth:
            login(request, auth)
            
        else:
            return Response({'error': 'Username or password is error'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.serializer_class(self.request.user).data)




class LogOutAPIView(viewsets.GenericViewSet,
                    mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = LogoutSerializer

    def create(self, request, *args, **kwargs):
        logout(self.request)
        return Response({'status': 'Log out success'})


class LoggedInUser(viewsets.GenericViewSet,
                   mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def list(self, request, *args, **kwargs):
        """
        Here you will get the logged in user
        """
        
        return Response(self.serializer_class(self.request.user, many=False).data)





