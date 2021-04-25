from django.test import TestCase
from unittest.mock import patch, call
import accounts.views

from accounts.models import Token


class SendLoginEmailViewTest(TestCase):
	'''тест представления, которое отправляет сообщение
	для входа в систему'''

	def test_redirects_to_home_page(self):
		'''тест: переадресует на домашнюю страницу'''
		response = self.client.post('/accounts/send_login_email', data={
			'email': 't1m.sadist@gmail.com'
		})
		self.assertRedirects(response, '/')

	@patch('accounts.views.send_mail')
	def test_sends_mail_to_address_from_post(self, mock_send_mail):
		'''тест: отправляется сообщение на адресс из метода post'''

		self.client.post('/accounts/send_login_email', data={
			'email': 't1m.sadist@gmail.com'
		})
		self.assertTrue(mock_send_mail.called)
		(subject, body, from_email, to_list), keargs = mock_send_mail.call_args
		self.assertEqual(subject, 'Your login link for Superlists')
		self.assertEqual(from_email, 'admin@admin.com')
		self.assertEqual(to_list, ['t1m.sadist@gmail.com'])

	def test_adds_success_message(self):
		'''тест: добавить сообщение об успехе'''
		response = self.client.post('/accounts/send_login_email', data={
			'email': 't1m.sadist@gmail.com'
			}, follow=True)
		message = list(response.context['messages'])[0]
		self.assertEqual(
			message.message,
			"Check your email we sent you a link, \
			which needs to be used for log in the website.")

		self.assertEqual(message.tags, "success")

	def test_creates_token_associated_with_email(self):
		'''тест: создание маркер, связанный с электронной почтой'''
		self.client.post('/accounts/send_login_email', data={
			'email': 't1m.sadist@gmail.com'
		})
		token = Token.objects.first()
		self.assertEqual(token.email, 't1m.sadist@gmail.com')

	@patch('accounts.views.send_mail')
	def test_sends_link_to_login_usings_token_uid(self, mock_send_mail):
		'''тест: отсылается ссылка на вход в систему, используя uid маркера'''
		self.client.post('/accounts/send_login_email', data={
			'email': 't1m.sadist@gmail.com'
		})
		token = Token.objects.first()
		expected_url = f"http://testserver/accounts/login?token={token.uid}"
		(subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
		self.assertIn(expected_url, body)


@patch('accounts.views.auth')
class LoginViewTest(TestCase):
	'''Тест представления входа в систему'''

	def test_redirects_to_home_page(self, mock_auth):
		'''тест: переадресуется на домашнюю страницу'''
		response = self.client.get('/accounts/login?token=abcd123')
		self.assertRedirects(response, '/')

	
	def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
		'''тест: вызывается authenticate с uid из GET-запроса'''
		self.client.get('/accounts/login?token=abcd123')
		self.assertEqual(
			mock_auth.authenticate.call_args,
			call(uid='abcd123')
		)

	def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
		'''тест: вызывает auth_login с пользователеме, если такой есть'''
		response = self.client.get('/accounts/login?token=abcd123')
		self.assertEqual(
			mock_auth.login.call_args,
			call(response.wsgi_request, mock_auth.authenticate.return_value)
		)

	def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
		'''тест: не регистрируется в системе, если пользователь не аунтифицирован'''
		mock_auth.authenticate.return_value = None
		self.client.get('/accounts/login?token=abcd123')
		self.assertFalse(mock_auth.login.called)