from django.test import TestCase
# from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlistAuthenticationBackend
from django.contrib import auth
from accounts.models import Token

User = auth.get_user_model()


class AuthenticationTest(TestCase):
	'''тест аунтификации'''

	def test_returns_None_if_no_such_token(self):
		'''тест: возвращает None, если нет такого токена'''
		result = auth.authenticate(
			'no-such-token'
		)
		self.assertIsNone(result)

	def test_returns_new_user_with_correct_email_if_token_exists(self):
		'''тест: возвращает новый пользователь с правильной электронной почтой
		если марке существует'''
		email = 't1m.sadist@gmail.com'
		token = Token.objects.create(email=email)
		user = auth.authenticate(token.uid)
		new_user = User.objects.get(email=email)
		self.assertEqual(user, new_user)

	def test_returns_existing_user_with_correct_email_if_token_exists(self):
		'''тест: возвращается существующий пользователь с правильной электронной почтой,
		если маркер существует'''
		email = 't1m.sadist@gmail.com'
		existing_user = User.objects.create(email=email)
		token = Token.objects.create(email=email)
		user = auth.authenticate(token.uid)
		self.assertEqual(user, existing_user)


class GetUserTest(TestCase):
	'''тест получения пользователя'''

	def test_gets_user_by_email(self):
		'''тест: получает пользователя по адресу электронной почты'''
		User.objects.create(email='t1m@gmail.com')
		desired_user = User.objects.create(email='t1m.sadist@gmail.com')
		found_user = PasswordlistAuthenticationBackend().get_user(
			't1m.sadist@gmail.com')
		self.assertEqual(found_user, desired_user)

	def test_returns_None_if_no_user_with_that_email(self):
		'''тест: возвращает None если нет пользователя с этим email'''
		self.assertIsNone(
			PasswordlistAuthenticationBackend().get_user('t1m.sadist@gmail.com')
		)