from django.test import TestCase

from .models import Item, List


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListAndItemModelsTest(TestCase):

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


class ListViewTest(TestCase):

    def test_display_all_items(self):
        todo_list = List.objects.create()
        Item.objects.create(text='item1', list=todo_list)
        Item.objects.create(text='item2', list=todo_list)

        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')