# forms.py

from django import forms
from .models import Farmer, Market, Personal, Product

class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['first_name', 'last_name', 'region', 'latitude', 'longitude', 'min_quantity_order', 'delivery_region', 'offers_delivery', 'payment_terms', 'buyer_choice', 'supply_frequency', 'products']

class MarketForm(forms.ModelForm):
    class Meta:
        model = Market
        fields = ['name', 'latitude', 'longitude', 'payment_terms', 'preferred_products', 'preferred_order_quantity', 'order_frequency', 'can_arrange_transport', 'siege_number', 'market_name']

class PersonalForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = ['name', 'latitude', 'longitude', 'payment_terms', 'preferred_products', 'preferred_order_quantity', 'order_frequency', 'can_arrange_transport', 'age', 'gender']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name']