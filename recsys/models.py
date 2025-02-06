from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)


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
    products = models.ManyToManyField(Product)
    min_quantity_order = models.PositiveIntegerField(default = 1) #Minimum of Kg by order
    delivery_region = models.PositiveIntegerField(default = 50) #radius in km
    offers_delivery = models.BooleanField(default = False)

    PAYMENT_CHOICES = [('upfront', 'Upfront'), ('credit', 'Credit'), ('any', 'Any')]
    payment_terms = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='any')
    

    BUYER_TYPE_CHOICES = [('personal', 'Personal'), ('market', 'Market'), ('both', 'Both')]
    buyer_choice = models.CharField(max_length=10, choices = BUYER_TYPE_CHOICES, default='both')

    FREQUENCY_CHOICES = [('Weekly', 'weekly'), ('Annually', 'annually'), ('Daily', 'daily'), ('Monthly', 'monthly')]
    supply_frequency = models.CharField(max_length=20, default='weekly', choices=FREQUENCY_CHOICES)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Buyer(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
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

    PAYMENT_CHOICES = [('upfront', 'Upfront'), ('credit', 'Credit'), ('any', 'Any')]
    payment_terms = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='any')

    preferred_products = models.ManyToManyField(Product)
    preferred_order_quantity = models.PositiveIntegerField(default=1)

    FREQUENCY_CHOICES = [('Weekly', 'weekly'), ('Annually', 'annually'), ('Daily', 'daily'), ('Monthly', 'monthly')]
    order_frequency = models.CharField(max_length=20, default='weekly', choices=FREQUENCY_CHOICES)
    can_arrange_transport = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.name}"

class Market(Buyer):
    siege_number = models.IntegerField()
    market_name = models.CharField(max_length=100)


class Personal(Buyer):
    age = models.PositiveIntegerField(validators=[MinValueValidator(18), MaxValueValidator(99)])
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.gender}, Age: {self.age})"
