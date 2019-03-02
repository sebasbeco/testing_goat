from selenium import webdriver

from .base import FunctionalTest, chromedriver


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        self.assertEqual(
            self.inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures). When she hits enter, the page updates,
        # and now the page lists "1: Buy peacock feathers" as an item in a to-do list
        self.enter_new_todo('Buy peacock feathers')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        self.enter_new_todo('Use peacock feathers to make a fly')

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # Satisfied, she goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        self.enter_new_todo('Buy peacock feathers')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now a new user, Francis, comes along to the site
        ## start a new browser to make sure no info from edith is coming
        ## through cookies
        self.browser.quit()
        self.browser = webdriver.Chrome(chromedriver)

        # Francis visits the homepage. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        pagetext = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', pagetext)
        self.assertNotIn('Make a fly', pagetext)

        # Francis starts a new list by entering a new item
        self.enter_new_todo('Buy milk')
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        pagetext = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', pagetext)
        self.assertIn('Buy milk', pagetext)