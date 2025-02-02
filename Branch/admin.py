from django.contrib import admin
from .models import Farmer, Buyer, Market, Personal

admin.site.register(Farmer)
admin.site.register(Buyer)
admin.site.register(Market)
admin.site.register(Personal)