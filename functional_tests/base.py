import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

chromedriver = r'/home/sebastian/chromedriver/chromedriver'
MAX_WAIT = 1


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(chromedriver)
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    @property
    def inputbox(self):
        return self.browser.find_element_by_id('id_new_item')

    def enter_new_todo(self, text):
        self.inputbox.send_keys(text + Keys.ENTER)

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def verify_inputbox_is_centered(self):
        self.assertAlmostEqual(
            self.inputbox.location['x'] + self.inputbox.size['width'] / 2,
            512,
            delta=10
        )
