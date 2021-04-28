from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import time
import os


MAX_WAIT = 10

def wait(fn):
	def method_fn(*args, **kwargs):
		start_time = time.time()
		while True:
			try:
				return fn(*args, **kwargs)
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)
	return method_fn 


class FunctionalTest(StaticLiveServerTestCase):
	'''new visitor test'''

	def setUp(self):
		'''instalation'''
		self.firefox_options = webdriver.FirefoxOptions()
		self.firefox_options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'

		self.browser = webdriver.Firefox(options=self.firefox_options) # Включаем браузер
		staging_server = os.environ.get('STAGING_SERVER')
		if staging_server:
			self.live_server_url = 'http://' + staging_server

	def tearDown(self):
		'''dismantling'''
		self.browser.quit()

	@wait
	def wait_for(self, fn):
		'''ожидание'''
		return fn()
		
	@wait
	def wait_for_row_in_list_table(self, row_text):
		'''ожидание строки в таблице списка'''
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])
			
	def get_item_input_box(self):
		'''получить поле ввода для элемента'''
		return self.browser.find_element_by_id('id_text')

	@wait
	def wait_to_be_logged_in(self, email):
		'''ожидать входа в систему'''
		self.browser.find_element_by_link_text('Log Out')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertIn(email, navbar.text)

	@wait
	def wait_to_be_logged_out(self, email):
		'''ожидать выхода из систему'''
		self.browser.find_element_by_name('email')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertNotIn(email, navbar.text)