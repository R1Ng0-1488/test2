from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings

import time
import os
import poplib


User = get_user_model()

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
		self.staging_server = os.environ.get('STAGING_SERVER')
		if self.staging_server:
			self.live_server_url = 'http://' + self.staging_server

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

	def wait_for_email(self, test_email, subject):
		'''ожидать электронное сообщение'''
		if not self.staging_server:
			email = mail.outbox[0]
			self.assertIn(test_email, email.to)
			self.assertEqual(email.subject, subject)
			return email.body

		email_id = None
		start = time.time()
		inbox = poplib.POP3_SSL('pop.gmail.com')
		try:
			inbox.user(test_email)
			inbox.pass_(os.environ['GMAIL_PASSWORD'])
			while time.time() - start < 60:
				# get 10 the newest messages
				count, _ = inbox.stat()
				for i in reversed(range(max(1, count-10), count + 1)):
					print('getting msg', i)
					_, lines, __ = inbox.retr(i)
					lines = [l.decode('utf8') for l in lines]
					
					if f'Subject: {subject}' in lines:
						email_id = i
						body = '\n'.join(lines)
						return body
				time.sleep(5)
		finally:
			if email_id:
				inbox.dele(email_id)
			inbox.quit()

	def add_list_item(self, item_text):
		'''добавить элемент списка'''
		num_rows = len(self.browser.find_elements_by_css_selector('#id_list_table tr'))
		self.get_item_input_box().send_keys(item_text)
		self.get_item_input_box().send_keys(Keys.ENTER)
		item_number = num_rows + 1
		self.wait_for_row_in_list_table(f'{item_number}: {item_text}')

	def create_pre_authenticated_session(self, email):
		'''создать предварительно аунтифицированный сеанс'''
		user = User.objects.create(email=email)
		session = SessionStore()
		session[SESSION_KEY] = user.pk
		session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
		session.save()

		## set cookie, which needs for the first domen visit
		## 404 page is uploaded the fastes
		self.browser.get(self.live_server_url + "/404_no_such_url/")
		self.browser.add_cookie(dict(
			name=settings.SESSION_COOKIE_NAME,
			value=session.session_key,
			path='/',
		))