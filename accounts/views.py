from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import auth, messages
from django.urls import reverse

from .models import Token

def send_login_email(request):
	'''отправить сообщение для входа в систему'''
	email = request.POST['email']
	token = Token.objects.create(email=email)
	url = request.build_absolute_uri(
		reverse('login') + '?token=' + str(token.uid))
	message_body = f'Use this link to log in:\n\n{url}'
	send_mail(
		'Your login link for Superlists',
		message_body,
		'admin@admin.com',
		[email],
	)
	messages.success(request, "Check your email we sent you a link, \
			which needs to be used for log in the website.")
	return redirect('/')

def login(request):
	user = auth.authenticate(request.GET.get('token'))
	if user:
		auth.login(request, user)
	return redirect('/')
