from django.shortcuts import render, redirect
from .models import *

def index(request):
	return render(request, "order/index.html")


# Create your views here.
