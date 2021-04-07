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
		self.get_item_input_box().send_keys(Keys.ENTER)

		# browser interсepts the request and does not load the page with list
		self.wait_for(lambda: self.browser.find_elements_by_css_selector(
			'#id_text:invalid'
		))

		# She starts typing the text of the new item and error disappears
		self.get_item_input_box().send_keys('Buy Milk')
		self.wait_for(lambda: self.browser.find_elements_by_css_selector(
			'#id_text:valid'
		))

		# and she can send it successfully
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy Milk')

		# As strange as it may seem. Edit decides to send the second empty list item
		self.get_item_input_box().send_keys(Keys.ENTER)

		# and again the browser won't be obey
		self.wait_for_row_in_list_table('1: Buy Milk')
		self.wait_for(lambda: self.browser.find_elements_by_css_selector(
			'#id_text:invalid'
		))

		
		# And she can correct it by filling the fields with some text
		self.get_item_input_box().send_keys('Make tea')
		self.wait_for(lambda: self.browser.find_elements_by_css_selector(
			'#id_text:valid'
		))
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy Milk')
		self.wait_for_row_in_list_table('2: Make tea')

	def test_cannot_add_duplicate_items(self):
		'''тест: нельзя добавлять повторяющиеся элементы'''
		# Edit opens a home page and starts a new list
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys('Buy wellies')
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy wellies')

		# She accidentally tries input repeated element
		self.get_item_input_box().send_keys('Buy wellies')
		self.get_item_input_box().send_keys(Keys.ENTER)

		# She sees a helpful error message 
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You've already got this in your list"
		))