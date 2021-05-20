from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from selenium.webdriver.common.keys import Keys 

import re

from .test_login import SUBJECT
from .base import FunctionalTest

User = get_user_model()


class MyListsTest(FunctionalTest):
	'''тест приложения "Мои списки"'''

	def registred_instead_of_session(self, email):
		'''регистрация вместо куки'''
		self.browser.get(self.live_server_url)
		self.browser.find_element_by_name('email').send_keys(email)
		self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

		# Appears the message which says that she was sent
		# an letter to her email

		self.wait_for(lambda: self.assertIn(
			'Check your email',
			self.browser.find_element_by_tag_name('body').text
		))

		# Edit checks her email and finds a message
		body = self.wait_for_email(email, SUBJECT)

		# Is contains a link to url-address
		self.assertIn('Use this link to log in', body)
		url_search = re.search(r'http://.+/.+$', body)
		if not url_search:
			self.fail(f"Could not find url in email body:\n{body}")
		url = url_search.group(0)

		# Edit pushes the link
		self.browser.get(url)


	def test_logged_in_users_lists_are_saved_as_my_lists(self):
		'''тест: списки зарегистрированных пользователей сохраняются как мои списки'''
		email = 'ololoevo1488@gmail.com'
		self.browser.get(self.live_server_url)
		self.wait_to_be_logged_out(email)

		# Edit is a registred user
		if self.staging_server:
			self.registred_instead_of_session(email)

		else:
			self.create_pre_authenticated_session(email)
			self.browser.get(self.live_server_url)
		self.wait_to_be_logged_in(email)

		# Edit opens home page and starts a new list
		self.add_list_item('Reticulate splines')
		self.add_list_item('Immanentize eschaton')
		first_list_url = self.browser.current_url

		# She points out a link to 'My lists' for the first time
		self.browser.find_element_by_link_text('My lists').click()

		# She sees that her list is there and it is named
		# based on the first element
		self.wait_for(
			lambda: self.browser.find_element_by_link_text('Reticulate splines')
		)
		self.browser.find_element_by_link_text('Reticulate splines').click()
		self.wait_for(
			lambda: self.assertEqual(self.browser.current_url, first_list_url)
		)

		# She decides to start one more list only to be sure
		self.browser.get(self.live_server_url)
		self.add_list_item('Click cows')
		second_list_url = self.browser.current_url

		# Under the heading 'My lists' her new list appears
		self.browser.find_element_by_link_text('My lists').click()
		self.wait_for(
			lambda: self.browser.find_element_by_link_text('Click cows')
		)
		self.browser.find_element_by_link_text('Click cows').click()
		self.wait_for(
			lambda: self.assertEqual(self.browser.current_url, second_list_url)
		)