from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



# Create your models here.

class Item(models.Model):
    sku = models.CharField(max_length=200)
    name = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.sku



class Consumer(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    sku = models.ForeignKey(Item,on_delete=models.CASCADE)
    where = models.CharField(max_length=100, default="")
    when = models.CharField(max_length=100, default="")
    country = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")
    getInfo = models.BooleanField(default = True)

    def __str__(self):
        return self.sku
    
class Scan(models.Model):
    sku = models.ForeignKey(Item,on_delete=models.CASCADE)
    where = models.CharField(max_length=100, default="")
    when = models.CharField(max_length=100, default="")
    country = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.sku
    
class Coupon(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    issuer = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100, default='')
    creationDate = models.DateTimeField(auto_now_add=True)
    expirationDate = models.DateTimeField(default= timezone.now())
    details = models.TextField(default="")
    image = models.ImageField(default='coupon.jpg', upload_to='coupon_images')
    industry = models.CharField(max_length=100, default='')
    link = models.URLField(default='')
    

      


