from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .models import Item, List
from .forms import ItemForm, ExistingListItemForm, NewListForm
# Create your views here.


User = get_user_model()


def home_page(request):
	'''home page'''
	return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
	'''представление списка'''
	list_ = List.objects.get(id=list_id)
	form = ExistingListItemForm(for_list=list_)

	if request.method == 'POST':
		form = ExistingListItemForm(for_list=list_, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect(list_)
	return render(request, 'list.html', {'list': list_,
										 'form': form})

# def new_list(request):
# 	'''новый список'''
# 	form = ItemForm(data=request.POST)
# 	if form.is_valid():
# 		list_ = List()
# 		if request.user.is_authenticated:
# 			list_.owner = request.user
# 		list_.save()
# 		form.save(for_list=list_)
# 		return redirect(str(list_.get_absolute_url()))
# 	else:
# 		return render(request, 'home.html', {'form': form})

def new_list(request):
	'''новый список 2'''
	form = NewListForm(data=request.POST)
	if form.is_valid():
		list_ = form.save(owner=request.user)
		return redirect(str(list_.get_absolute_url()))
	return render(request, 'home.html', {'form': form})

def my_lists(request, email):
	'''мои списки'''
	owner = User.objects.get(email=email)
	return render(request, 'my_lists.html', {'owner': owner})

def share_list(request, list_id):
	'''поделиться списком'''
	list_ = List.objects.get(id=list_id)
	if request.method == 'POST':
		user = User.objects.get(email=request.POST.get('sharee'))
		list_.shared_with.add(user)
	return redirect(list_)