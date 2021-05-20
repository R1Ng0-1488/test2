from selenium import webdriver
from .base import FunctionalTest


def quit_if_possible(browser):
	try: browser.quit()
	except: pass


class SharingTest(FunctionalTest):
	'''тест обмена данными'''

	def test_can_share_a_list_with_another_user(self):
		'''тест: можно обмениваться списком с еще одиним пользователем'''
		# Edit is registred user
		self.create_pre_authenticated_session('t1m.sadist@gmail.com')
		edith_browser = self.browser
		self.addCleanup(lambda: quit_if_possible(edith_browser))

		# her friend Onicefer also hangs on the list site
		oni_browser = webdriver.Firefox(options=self.firefox_options)
		self.addCleanup(lambda: quit_if_possible(oni_browser))
		self.browser = oni_browser
		self.create_pre_authenticated_session('temich.97@mail.ru')

		# Edit opens a home page and starts a new list
		self.browser = edith_browser
		self.browser.get(self.live_server_url)
		self.add_list_item('Get help')

		# She points out the option "Share this list"
		share_box = self.browser.find_element_by_css_selector(
			'input[name="sharee"]'
		)		
		self.asserEqual(
			share_box.get_attribute('placeholder'),
			'your-friend@example.com'
		)