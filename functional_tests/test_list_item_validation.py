from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item
        self.browser.get(self.live_server_url)
        self.newitem_inputbox.send_keys(Keys.ENTER)

        # The homepage refreshes, and there is an error message saying
        # that list items cannot be blank
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))

        # She tries again with some text for the item, which now works
        self.enter_new_todo('Buy milk')
        self.verify_todo_in_list('1: Buy milk')

        # Perversely, she now decides to submit a second blank list item
        self.newitem_inputbox.send_keys(Keys.ENTER)

        # She receives a similar warning
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))

        # And she can correct it by filling some text
        self.enter_new_todo('Make tea')
        self.verify_todo_in_list('1: Buy milk')
        self.verify_todo_in_list('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # Edith goes to the homepage and starts a new list
        self.browser.get(self.live_server_url)
        self.enter_new_todo('Buy wellies')
        self.verify_todo_in_list('1: Buy wellies')

        # She accidentally tries to enter a duplicate item
        self.enter_new_todo('Buy wellies')

        # She sees a helpful error message
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You've already got this in your list"
        ))