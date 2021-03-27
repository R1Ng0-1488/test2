from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
	'''тест: валидации элемента списка'''

	def test_cannot_add_empty_list_items(self):
		'''тест: нельзя добавлять пустые элементы списка'''
		# Edit opens home page and accidentally tries ti send
		# an empty list element. She pushe Enter on the empty input field
		self.browser.get(self.live_server_url)
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

		# Home page is updating and error message appears
		# that says that the list items should not be empty
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You can't have an empty list item"
		))
		# She tries again. Now with some text for item and now is working
		self.browser.find_element_by_id('id_new_item').send_keys('Buy Milk')
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy Milk')

		# As strange as it may seem. Edit decides to send the second empty list item
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

		# She gets a similar warning on the list page
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You can't have an empty list item"
		))
		# And she can correct it by filling the fields with some text
		self.browser.find_element_by_id('id_new_item').send_keys('Make tea')
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy Milk')
		self.wait_for_row_in_list_table('2: Make tea')