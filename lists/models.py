from django.db import models

# Create your models here.


class List(models.Model):
	'''Список'''

class Item(models.Model):
	'''Элемент списка'''
	text = models.TextField(default='')
	list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)