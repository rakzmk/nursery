from django.db import models
from django.contrib.auth.models import User
from user.models import *
from django.utils.datetime_safe import datetime

# Create your models here.
class Categories(models.Model):
    category = models.CharField(max_length=50)

class Products(models.Model):
    product = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete = models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    description = models.TextField()
    image1 = models.ImageField(upload_to="myimage")
    image2 = models.ImageField(upload_to="myimage")
    image3 = models.ImageField(upload_to="myimage")
    

    @property
    def imageurl(self):
        if self.image1== '':
            image = ''
        else:
            image = self.image1.url
        return image

    @property
    def imageurl2(self):
        if self.image2== '':
            image = ''
        else:
            image = self.image2.url
            return image

    @property
    def imageurl3(self):
        if self.image3=='':
            image = ''
        else:
            image = self.image3.url
            return image





    # these are the STATUS
    # delivered = models.CharField(max_length=50)
    #  confirmed = models.CharField(max_length=50)
    #  order_pending = models.CharField(max_length=50)
    #  cancelled = models.CharField(max_length=50)
