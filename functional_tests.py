from selenium import webdriver
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

		# SHe sees that title and header of the page say about urgent lists
		self.assertIn('To-Do', self.browser.title) #  проверяем наличие To-DO  в тайтле
		self.fail('Finish the test!')
		
		# She is immedeatly offered to enter list's element

		# She types in the text area "Buy peacock feather"
		# her hobby is knitting fishing flies

		# When she pushes enter, the page is being updated. And now the page
		# contains "1: Buy peacock feather"
		# Edit is very methodical

		# THe page is being updated again. And now it shows both elements of her list

		# EDit wonders if the site remembers her list. Next she sees that
		# the site generated for her unique YRL-address. A short text with explanations
		# is displayed about this

		# She visits this URL-address - her list is still there

		# She is satisfied goes to sleep again
		

if __name__ == '__main__':
	unittest.main(warnings='ignore')