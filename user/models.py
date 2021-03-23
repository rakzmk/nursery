from django.db import models
from django.contrib.auth.models import User
from adminlog.models import Products
from django.utils.datetime_safe import datetime



#Create your models here.
class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=50)


class Cart(models.Model):
    product = models.ForeignKey(Products, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    count = models.IntegerField(default=1)
    date = models.DateField(auto_now_add=True)


class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    house_name = models.CharField(max_length=100)
    address_name = models.CharField(max_length=100, default=None)
    address_mobile = models.CharField(max_length=50,default=None)
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.IntegerField()

class Order(models.Model):
    user_id =  models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Products, on_delete = models.CASCADE)
    address = models.ForeignKey(Address,on_delete= models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    count = models.IntegerField()