import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from selenium import webdriver

from bank_accounts.models import BankUser


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

	def test_if_admin_sees_a_list_of_all_users(self):
		self.browser.get(self.live_server_url)

		user_panels = self.browser.find_elements_by_class_name('panel-group')
		
		assert len(user_panels) == len(BankUser.objects.all())

	def test_if_users_accounts_are_listed(self):
		self.browser.get(self.live_server_url)

		user_panels = self.browser.find_elements_by_class_name('panel-group')
		account_table = user_panels[0].find_element_by_class_name('table')
		account_list = account_table.find_element_by_tag_name('tbody')
		accounts = account_list.find_elements_by_tag_name('tr')
		
		assert len(accounts) == len(BankUser.objects.first().accounts.all())

	def test_if_edit_link_redirects_to_correct_edit_site(self):
		self.browser.get(self.live_server_url)

		user_panels = self.browser.find_elements_by_class_name('panel-group')
		edit_button = user_panels[0].find_element_by_class_name('glyphicon-pencil')
		edit_button_target = edit_button.get_attribute('href')

		edit_slug = reverse('bank-user-update', kwargs={'pk': BankUser.objects.first().id})
		assert edit_button_target.endswith(edit_slug)