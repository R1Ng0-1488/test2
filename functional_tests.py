from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):
	'''new visitor test'''

	def setUp(self):
		'''instalation'''
		self.browser = webdriver.Firefox() # Включаем браузер

	def tearDown(self):
		'''dismantling'''
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		'''тест: может начать и список и получить его позже'''
		# Edit heard about a cool new online-application with
		# urgent lists. She decides to estimate it's home page
		self.browser.get('http://localhost:8000') # Переходим по ссылке

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

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1: Buy peacock fether')
		)
		# Textarea is still invites her to add one more element
		# She enters "Make fly out of peacock fethers"
		# Edit is very methodical
		self.fail('Finish the test!')
		# The page is being updated again. And now it shows both elements of her list

		# EDit wonders if the site remembers her list. Next she sees that
		# the site generated for her unique YRL-address. A short text with explanations
		# is displayed about this

		# She visits this URL-address - her list is still there

		# She is satisfied goes to sleep again
		

if __name__ == '__main__':
	unittest.main(warnings='ignore')