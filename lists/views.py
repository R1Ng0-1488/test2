from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_page(request):
	'''home page'''
	return render(request, 'home.html')