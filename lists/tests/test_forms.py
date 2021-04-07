from django.test import TestCase

from ..forms import ItemForm, EMPTY_ITEM_ERROR
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

	def test_form_save_handles_saving_to_a_list(self):
		'''тест: метод save формы обрабатывает сохранение в список'''
		list_ = List.objects.create()
		form = ItemForm(data={'text': 'do me'})
		new_item = form.save(for_list=list_)
		self.assertEqual(new_item, Item.objects.first())
		self.assertEqual(new_item.text, 'do me')
		self.assertEqual(new_item.list, list_)