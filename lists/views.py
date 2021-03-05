from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Item
# Create your views here.

def home_page(request):
	'''home page'''
	return render(request, 'home.html')

def view_list(request):
	'''представление списка'''
	items = Item.objects.all()
	return render(request, 'list.html', {'items': items})

def new_list(request):
	'''новый список'''
	Item.objects.create(text=request.POST['item_text'])
	return redirect('/lists/only_one_list_in_the_world/')