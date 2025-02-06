from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(Farmer)
admin.site.register(Buyer)
admin.site.register(Market)
admin.site.register(Personal)