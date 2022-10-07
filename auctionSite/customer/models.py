from unicodedata import category
from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

class Category(models.Model):
    categoryId = models.IntegerField()
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class item(models.Model):
    name = models.CharField(max_length=30,null=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)
    description = models.TextField()
    user = models.ForeignKey('userDetails',null=False,on_delete=models.CASCADE)
    initialPrice = models.IntegerField(default=5000)
    closingDate = models.DateTimeField(null=True)
    image = models.ImageField(upload_to='images/',null=True)
    status = models.BooleanField(default=0)

    def __str__(self):
        return self.name

class userDetails(models.Model):
    name = models.CharField(max_length=30, null=False)
    password = models.CharField(max_length=30,null=False)
    contact = models.IntegerField()
    gender = models.BooleanField(default=0)
    email = models.EmailField(unique=True)
    mode = models.BooleanField(default = 0)

    def __str__(self):
        return self.name

class Biddings(models.Model):
    itemId = models.ForeignKey('item',null=False,on_delete=models.CASCADE)
    custId = models.ForeignKey('userDetails',null=False,on_delete=models.CASCADE)
    bidd = models.IntegerField(null=False)


class SoldItems(models.Model):
    itemId = models.ForeignKey('item',null=False,on_delete=models.CASCADE)
    custId = models.ForeignKey('userDetails',null=False,on_delete=models.CASCADE)
    price = models.IntegerField(default=0)

class Comments(models.Model):
    comment = models.TextField()
    product = models.ForeignKey('item',null=False,on_delete=models.CASCADE)
    rating = models.IntegerField()



