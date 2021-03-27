from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
	'''тест: макета и стилевого оформления'''

	def test_layout_and_styling(self):
		'''тест макета и стилевого оформления'''
		# Edit opens home page
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		# She pointes out that the input field is neatly centred
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		) 
		# She begins a new list and sees that input field there
		# is neasty centred too
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: testing')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)
