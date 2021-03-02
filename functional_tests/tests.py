from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import unittest
import time


class NewVisitorTest(LiveServerTestCase):
	'''new visitor test'''

	def setUp(self):
		'''instalation'''
		self.browser = webdriver.Firefox() # Включаем браузер

	def tearDown(self):
		'''dismantling'''
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		'''подвтерждение строки в таблице списка'''
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])
	

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
		time.sleep(1)

		self.check_for_row_in_list_table('1: Buy peacock feather')
		
		# Textarea is still invites her to add one more element
		# She enters "Make fly out of peacock fethers"
		# Edit is very methodical
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys("Make fly out of peacock fethers")
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)

		# The page is being updated again. And now it shows both elements of her list	
		self.check_for_row_in_list_table('1: Buy peacock feather')
		self.check_for_row_in_list_table('2: Make fly out of peacock fethers')
		

		# EDit wonders if the site remembers her list. Next she sees that
		# the site generated for her unique URL-address. A short text with explanations
		# is displayed about this
		self.fail('Finish the test!')

		# She visits this URL-address - her list is still there

		# She is satisfied and goes to sleep again
