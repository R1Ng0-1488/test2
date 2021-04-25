from .models import Token, User


class PasswordlistAuthenticationBackend:
	'''беспарольный серверный процесс аунтификации'''

	def authenticate(self, uid):
		'''аунтификация'''
		try:
			token = Token.objects.get(uid=uid)
			return User.objects.get(email=token.email)
		except User.DoesNotExist:
			return User.objects.create(email=token.email)
		except Token.DoesNotExist:
			return None

	def get_user(self, email):
		'''получить пользователя'''
		try:
			return User.objects.get(email=email)
		except User.DoesNotExist:
			return None

			