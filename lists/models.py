from django.db import models
from django.urls import reverse
# Create your models here.


class List(models.Model):
	'''Список'''

	def get_absolute_url(self):
		'''получить абсолютный url'''
		return reverse('view_list', args=[self.id])


class Item(models.Model):
	'''Элемент списка'''
	text = models.TextField(default='')
	list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)

	class Meta:
		ordering = ('id',)
		unique_together = ('list', 'text')

	def __str__(self):
		return self.text