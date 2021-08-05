from django.db import models
from django.db.models.fields import DateField
from django.contrib.auth.models import User




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
    
class Scan(models.Model):
    sku = models.ForeignKey(Item,on_delete=models.CASCADE)
    where = models.CharField(max_length=100, default="")
    when = models.CharField(max_length=100, default="")
    country = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")
    

      


