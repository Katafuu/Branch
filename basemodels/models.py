from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class ProductBase(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return f'{self.name}'

class FarmerBase(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    region = models.CharField(max_length=30)#I think we can make the region a many to many field, tho we ll need a data base
#Tho we ll need a table with all possible regions
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class BuyerBase(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name}"