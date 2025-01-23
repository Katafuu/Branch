from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Farmer Model
class Farmer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # Region should be normalized as a separate model with a ForeignKey or ManyToManyField
    region = models.CharField(max_length=30)  # You can replace this with a ForeignKey if needed
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


# Buyer Base Model
class Buyer(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return self.name


# Market Model
class Market(Buyer):
    siege_number = models.IntegerField()
    market_name = models.CharField(max_length=100)  # Fix the field definition


# Personal Buyer Model
class Personal(Buyer):
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(99)]
    )
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
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.gender})"
