from django.test import TestCase
from django.urls import resolve
from django.template.loader import render_to_string
from django.http import HttpRequest

from lists.views import home_page
# Create your tests here.


class HomePageTest(TestCase):
	'''Тест домашней страницы'''

	def test_uses_home_template(self):
		'''тест: используется домашний шаблон'''
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')