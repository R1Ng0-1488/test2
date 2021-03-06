from django.test import TestCase
import unittest
from unittest.mock import Mock, patch

from ..forms import (
	ItemForm, EMPTY_ITEM_ERROR,
	DUPLICATION_ITEM_ERROR, ExistingListItemForm,
	NewListForm
)
from ..models import List, Item


class ItemFormTest(TestCase):
	'''Тест формы для элемента списка'''

	def test_form_item_input_has_placeholder_and_css_classes(self):
		'''тест: поле ввода имеет атрибут placeholder и css-классы'''
		form = ItemForm()
		self.assertIn('placeholder="Enter a to-do item"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())

	def test_form_validation_for_blank_items(self):
		'''тест: валидации формы для пустых элементов'''
		form = ItemForm(data={'text': ''})
		self.assertFalse(form.is_valid())
		self.assertEqual(
			form.errors['text'],
			[EMPTY_ITEM_ERROR]
		)

	# def test_form_save_handles_saving_to_a_list(self):
	# 	'''тест: метод save формы обрабатывает сохранение в список'''
	# 	list_ = List.objects.create()
	# 	form = ItemForm(data={'text': 'do me'})
	# 	new_item = form.save(for_list=list_)
	# 	self.assertEqual(new_item, Item.objects.first())
	# 	self.assertEqual(new_item.text, 'do me')
	# 	self.assertEqual(new_item.list, list_)


class ExistingListItemFormTest(TestCase):
	'''Тест формы элементов существующего списка'''

	def test_form_renders_item_text_input(self):
		'''тест: форма отображает текстовый ввод элемента'''
		list_ = List.objects.create()
		form = ExistingListItemForm(for_list=list_)
		self.assertIn('placeholder="Enter a to-do item"', form.as_p())

	def test_form_validation_for_blank_item(self):
		'''тест: валидация формы для пустых элементов'''
		list_ = List.objects.create()
		form = ExistingListItemForm(for_list=list_, data={'text': ''})
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

	def test_form_validation_for_duplicate_items(self):
		'''тест: валидация формы для повторных элементов'''
		list_ = List.objects.create()
		Item.objects.create(list=list_, text='no twins!')
		form = ExistingListItemForm(for_list=list_, data={'text': 'no twins!'})
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['text'], [DUPLICATION_ITEM_ERROR])

	def test_form_save(self):
		'''тест: сохранение формы'''
		list_ = List.objects.create()
		form = ExistingListItemForm(for_list=list_, data={'text': 'hi'})
		new_item = form.save()
		self.assertEqual(new_item, Item.objects.all()[0])
		

class NewListFormTest(unittest.TestCase):
	'''тест формы для нового списка'''

	@patch('lists.forms.List.create_new')
	def test_save_creates_new_list_from_post_data_if_user_not_authenticated(
		self, mock_list_create_new):
		'''тест: save создает новый списко из POST-данных
		если пользователь не аунтифицирован'''
		user = Mock(is_authenticated=False)
		form = NewListForm(data={'text': 'new item text'})
		form.is_valid()
		form.save(owner=user)
		mock_list_create_new.assert_called_once_with(
			first_item_text='new item text'
		)

	@patch('lists.forms.List.create_new')
	def test_save_creates_new_list_owner_if_user_authenticated(
		self, mock_list_create_new):
		'''тест: save создает новый список с владельцем,
		если пользователь аунтифицирован'''
		user = Mock(is_authenticated=True)
		form = NewListForm(data={'text': 'new item text'})
		form.is_valid()
		form.save(owner=user)
		mock_list_create_new.assert_called_once_with(
			first_item_text='new item text', owner=user)

	@patch('lists.forms.List.create_new')
	def test_save_returns_new_list_object(self, mock_List_create_new):
		'''тест: save возвращает новый объект списка'''
		user = Mock(is_authenticated=True)
		form = NewListForm(data={'text': 'new item text'})
		form.is_valid()
		response = form.save(owner=user)
		self.assertEqual(response, mock_List_create_new.return_value)