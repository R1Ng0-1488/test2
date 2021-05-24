from selenium import webdriver

from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage


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
		list_page = ListPage(self).add_list_item('Get help')
		

		# She points out the option "Share this list"
		share_box = list_page.get_share_box() 
		self.assertEqual(
			share_box.get_attribute('placeholder'),
			'your-friend@example.com'
		)

		# She shares her list
		# The page refreshed and reports that
		# now the page is used with Onicefer
		list_page.share_list_with('temich.97@mail.ru')

		# Onicefer goes to the lists page in his browser
		self.browser = oni_browser
		MyListsPage(self).go_to_my_lists_page()

		# He sees Edit's list on it!
		self.browser.find_element_by_link_text('Get help').click()

		# On the page which Onicefer sees it says that this list is Edith's
		self.wait_for(lambda: self.assertEqual(
			list_page.get_list_owner(),
			't1m.sadist@gmail.com'
		))

		# He adds an element to the list
		list_page.add_list_item('Hi Edith!')

		# When Edit refreshes the list she sees Onicefer's additional
		self.browser = edith_browser
		self.browser.refresh()
		list_page.wait_for_row_in_list_table('Hi Edith!', 2)
