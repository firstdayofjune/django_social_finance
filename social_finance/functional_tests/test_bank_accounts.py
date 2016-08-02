import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from bank_accounts.models import BankAccount
from selenium import webdriver


class AccountListingTest(StaticLiveServerTestCase):
	fixtures = [
		os.path.join('bank_accounts', 'fixtures', 'test_admins.json'),
		os.path.join('bank_accounts', 'fixtures', 'test_users.json'),
		os.path.join('bank_accounts', 'fixtures', 'test_accounts.json'),
	]	

	def setUp(self):
		self.browser = webdriver.PhantomJS()
		self.browser.set_window_size(1024, 768)
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_if_admin_sees_a_list_of_all_accounts(self):
		self.browser.get(self.live_server_url)

		account_table = self.browser.find_element_by_class_name('table')
		table_data = account_table.find_element_by_tag_name('tbody')
		accounts_listed = table_data.find_elements_by_tag_name('tr')

		assert len(accounts_listed) == len(BankAccount.objects.all())