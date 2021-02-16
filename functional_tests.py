from selenium import webdriver

browser = webdriver.Firefox() # Включаем браузер
browser.get('http://localhost:8000') # Переходим по ссылке

assert 'Django' in browser.title #  проверяем наличие Django  в тайтле