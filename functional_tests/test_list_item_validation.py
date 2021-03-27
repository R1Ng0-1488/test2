from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
	'''тест: валидации элемента списка'''

	def test_cannot_add_empty_list_items(self):
		'''тест: нельзя добавлять пустые элементы списка'''
		# Edit opens home page and accidentally tries ti send
		# an empty list element. She pushe Enter on the empty input field

		# Home page is updating and error message appears
		# that says that the list items should not be empty

		# She tries again. Now with some text for item and now is working

		# As strange as it may seem. Edit decides to send the second empty list item

		# She gets a similar warning on the list page

		# And she can correct it by filling the fields with some text
		self.fail('write me')