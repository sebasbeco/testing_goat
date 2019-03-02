from .base import FunctionalTest


class LayoutAndStyling(FunctionalTest):

    def test_layout_and_styling(self):
        # Edith goes to the homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        self.verify_inputbox_is_centered()

        # She starts a new list and sees the input is nicely centered there too
        self.enter_new_todo('testing')
        self.wait_for_row_in_list_table('1: testing')
        self.verify_inputbox_is_centered()