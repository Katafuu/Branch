from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Farmer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    region = models.CharField(max_length=30)#I think we can make the region a many to many field, tho we ll need a data base
#Tho we ll need a table with all possible regions
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, 
        validators=[MinValueValidator(-90), MaxValueValidator(90)], 
        null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, 
        validators=[MinValueValidator(-180), MaxValueValidator(180)], 
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Buyer(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.name}"

class Market(Buyer):
    siege_number = models.IntegerField()
    market_name = models.CharField

class Personal(Buyer):
    age = models.PositiveIntegerField(MinValueValidator(18), MaxValueValidator(99))
    gender = models.CharField(max_length=50)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, 
        validators=[MinValueValidator(-90), MaxValueValidator(90)], 
        null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, 
        validators=[MinValueValidator(-180), MaxValueValidator(180)], 
        null=True, blank=True
    )
