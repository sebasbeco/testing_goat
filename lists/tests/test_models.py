from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import Item, List


class ListAndItemModelsTest(TestCase):

    def test_cannot_save_empty_list_items(self):
        todolist = List.objects.create()
        item = Item(list=todolist, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_saving_and_retrieving_items(self):
        todo_list = List()
        todo_list.save()

        item1 = Item()
        item1.text = 'The first (ever) list item'
        item1.list = todo_list
        item1.save()

        item2 = Item()
        item2.text = 'Item the second'
        item2.list = todo_list
        item2.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, todo_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, 'The first (ever) list item')
        self.assertEqual(saved_items[0].list, todo_list)
        self.assertEqual(saved_items[1].text, 'Item the second')
        self.assertEqual(saved_items[1].list, todo_list)

    def test_get_absolute_url(self):
        todolist = List.objects.create()
        self.assertEqual(todolist.get_absolute_url(), f'/lists/{todolist.id}/')