from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
import unittest
import time


MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
	'''new visitor test'''

	def setUp(self):
		'''instalation'''
		self.browser = webdriver.Firefox() # Включаем браузер

	def tearDown(self):
		'''dismantling'''
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		'''ожидание строки в таблице списка'''
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)
 	

	def test_can_start_a_list_and_retrieve_it_later(self):
		'''тест: может начать и список и получить его позже'''
		# Edit heard about a cool new online-application with
		# urgent lists. She decides to estimate it's home page
		self.browser.get(self.live_server_url) # Переходим по ссылке

		# She sees that title and header of the page say about urgent lists
		self.assertIn('To-Do', self.browser.title) #  проверяем наличие To-DO  в тайтле
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# She is immedeatly offered to enter list's element
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		# She types in the text area "Buy peacock feather"
		# her hobby is knitting fishing flies
		inputbox.send_keys('Buy peacock feather')

		# When she pushes enter, the page is being updated. And now the page
		# contains "1: Buy peacock feather"
		inputbox.send_keys(Keys.ENTER)
		
		self.wait_for_row_in_list_table('1: Buy peacock feather')
		
		# Textarea is still invites her to add one more element
		# She enters "Make fly out of peacock fethers"
		# Edit is very methodical
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys("Make fly out of peacock fethers")
		inputbox.send_keys(Keys.ENTER)
		
		# The page is being updated again. And now it shows both elements of her list	
		self.wait_for_row_in_list_table('1: Buy peacock feather')
		self.wait_for_row_in_list_table('2: Make fly out of peacock fethers')

		# EDit wonders if the site remembers her list. Next she sees that
		# the site generated for her unique URL-address. A short text with explanations
		# is displayed about this
		# self.fail('Finish the test!')

		# She visits this URL-address - her list is still there

		# She is satisfied and goes to sleep again
	
	def test_multiple_users_can_start_lists_at_different_urls(self):
		'''тест: многочисленные пользователи могут начать списки по разным url'''

		# Edit starts a new list
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		# She notices that her list has a unique URL-address
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		# Now a new user Francis is visiting the site

		## We use a new browser session so we provide that
		## no Edith information won't come through the data, cookie etc.
		self.browser.quit()
		self.browser = webdriver.Firefox()

		# Frencis visits a home page. There are no Edith list signs
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('Make a fly', page_text)

		# Francis starts a new list entering a new element. It is less interesting
		# than Edith list
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		# Francis gets a unique URL-address
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		# There are no signs from Edith list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)