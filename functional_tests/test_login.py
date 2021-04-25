from django.core import mail
from selenium.webdriver.common.keys import Keys 
import re

from .base import FunctionalTest


TEST_EMAIL = 't1m.sadist@gmail.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
	'''тест регистрации в системе'''

	def test_can_get_email_link_to_log_in(self):
		'''тест: можно получить ссылку по почте для регистрации'''
		# Edit enters the official superlist website and for the first time
		# points out log in section in navbar
		# It tells her to input her email what she does
		self.browser.get(self.live_server_url)
		self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
		self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

		# Appears the message which says that she was sent
		# an letter to her email
		self.wait_for(lambda: self.assertIn(
			'Check your email',
			self.browser.find_element_by_tag_name('body').text
		))

		# Edit checks her email and finds a message
		email = mail.outbox[0]
		self.assertIn('Use this link to log in', email.body)
		url_search = re.search(r'http://.+/.+$', email.body)
		if not url_search:
			self.fail(f"Could not find url in email body:\n{email.body}")
		url = url_search.group(0)
		self.assertIn(self.live_server_url, url)

		# Edit pushes the link
		self.browser.get(url)

		# She is registred in system
		self.wait_for(
			lambda: self.browser.find_element_by_link_text('Log Out')
		)
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertIn(TEST_EMAIL, navbar.text)

		# She is leaving the system
		self.browser.find_element_by_link_text('Log Out').click()

		# She left the system
		self.wait_for(
			lambda: self.browser.find_element_by_name('email')
		)
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertNotIn(TEST_EMAIL, navbar.text)