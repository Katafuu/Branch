from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("""<meta http-equiv="refresh" content="0; url=./home"/>""")
