import os
import requests

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.test import Client
from selenium import webdriver

from bank_accounts.models import BankUser

def visit_login(driver, login_url):
	driver.get(login_url)
	username = driver.find_element_by_id('id_login')
	password = driver.find_element_by_id('id_password')
	username.send_keys('Peter')
	password.send_keys('peters_password')

	login_btn = driver.find_element_by_class_name('primaryAction')
	login_btn.click()		


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
		login_url = self.live_server_url + '/accounts/login'
		visit_login(self.browser, login_url)

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


class UserCRUDTest(StaticLiveServerTestCase):
	fixtures = [
		os.path.join('bank_accounts', 'fixtures', 'test_admins.json'),
		os.path.join('bank_accounts', 'fixtures', 'test_users.json'),
		os.path.join('bank_accounts', 'fixtures', 'test_accounts.json'),
	]	

	def setUp(self):
		self.browser = webdriver.PhantomJS()
		self.browser.set_window_size(1024, 768)
		self.browser.implicitly_wait(3)
		login_url = self.live_server_url + '/accounts/login'
		visit_login(self.browser, login_url)

	def tearDown(self):
		self.browser.quit()

	def test_if_edit_link_redirects_to_correct_edit_site(self):
		self.browser.get(self.live_server_url)

		user_panels = self.browser.find_elements_by_class_name('panel-group')
		edit_button = user_panels[0].find_element_by_class_name('glyphicon-pencil')
		edit_button_target = edit_button.get_attribute('href')

		edit_slug = reverse('bank-user-update', kwargs={'pk': BankUser.objects.first().id})
		assert edit_button_target.endswith(edit_slug)

	def test_if_edit_link_site_shows_prefilled_form(self):
		self.browser.get(self.live_server_url)

		user_panels = self.browser.find_elements_by_class_name('panel-group')
		edit_button = user_panels[0].find_element_by_class_name('glyphicon-pencil')
		edit_button.click()

		firstname_field = self.browser.find_element_by_id('id_firstname')
		lastname_field = self.browser.find_element_by_id('id_lastname')

		assert firstname_field.get_attribute('value') == BankUser.objects.first().firstname
		assert lastname_field.get_attribute('value') == BankUser.objects.first().lastname

	def test_if_add_link_redirects_to_correct_edit_site(self):
		self.browser.get(self.live_server_url)

		add_buttons = self.browser.find_elements_by_class_name('btn-success')
		add_user = add_buttons[0]
		add_user_target = add_user.get_attribute('href')

		add_slug = reverse('bank-user-create')
		assert add_user_target.endswith(add_slug)

	def test_if_add_link_site_shows_empty_form(self):
		self.browser.get(self.live_server_url)

		add_buttons = self.browser.find_elements_by_class_name('btn-success')
		add_user = add_buttons[0]
		add_user.click()

		firstname_field = self.browser.find_element_by_id('id_firstname')
		lastname_field = self.browser.find_element_by_id('id_lastname')

		assert firstname_field.get_attribute('value') == ''
		assert lastname_field.get_attribute('value') == ''

	def test_if_delete_link_redirects_to_correct_site(self):
		self.browser.get(self.live_server_url)

		user_panels = self.browser.find_elements_by_class_name('panel-group')
		remove_button = user_panels[0].find_element_by_class_name('glyphicon-remove')
		remove_button_target = remove_button.get_attribute('href')

		remove_slug = reverse('bank-user-delete', kwargs={'pk': BankUser.objects.first().id})
		assert remove_button_target.endswith(remove_slug)

	def test_if_delete_link_site_shows_submit_button(self):
		self.browser.get(self.live_server_url)

		user_panels = self.browser.find_elements_by_class_name('panel-group')
		remove_button = user_panels[0].find_element_by_class_name('glyphicon-remove')
		remove_button.click()

		confirm_button = self.browser.find_elements_by_tag_name('input')[1]
		assert confirm_button.get_attribute('type') == 'submit'


class AccountCRUDTest(StaticLiveServerTestCase):
	fixtures = [
		os.path.join('bank_accounts', 'fixtures', 'test_admins.json'),
		os.path.join('bank_accounts', 'fixtures', 'test_users.json'),
		os.path.join('bank_accounts', 'fixtures', 'test_accounts.json'),
	]	

	def setUp(self):
		self.browser = webdriver.PhantomJS()
		self.browser.set_window_size(1024, 768)
		self.browser.implicitly_wait(3)
		login_url = self.live_server_url + '/accounts/login'
		visit_login(self.browser, login_url)

	def tearDown(self):
		self.browser.quit()

	def test_if_edit_link_redirects_to_correct_edit_site(self):
		self.browser.get(self.live_server_url)

		user_panels = self.browser.find_elements_by_class_name('panel-group')
		account_table = user_panels[0].find_element_by_class_name('table')
		account_list = account_table.find_element_by_tag_name('tbody')
		accounts = account_list.find_elements_by_tag_name('tr')

		edit_button = accounts[0].find_element_by_class_name('glyphicon-pencil')
		edit_button_target = edit_button.get_attribute('href')

		url_args = {
			'user_id': BankUser.objects.first().id,
			'pk': BankUser.objects.first().accounts.first().id,
		}
		edit_slug = reverse('bank-account-update', kwargs=url_args)
		assert edit_button_target.endswith(edit_slug)

	def test_if_edit_link_site_shows_prefilled_form(self):
		self.browser.get(self.live_server_url)

		user_panels = self.browser.find_elements_by_class_name('panel-group')
		
		account_table = user_panels[0].find_element_by_class_name('table')
		account_list = account_table.find_element_by_tag_name('tbody')
		accounts = account_list.find_elements_by_tag_name('tr')

		edit_button = accounts[0].find_element_by_class_name('glyphicon-pencil')
		edit_button_target = edit_button.get_attribute('href')

		self.browser.get(edit_button_target)

		iban_field = self.browser.find_element_by_id('id_iban')
		
		assert iban_field.get_attribute('value') == BankUser.objects.first().accounts.first().iban

	def test_if_delete_link_redirects_to_correct_site(self):
		self.browser.get(self.live_server_url)

		user_panels = self.browser.find_elements_by_class_name('panel-group')
		account_table = user_panels[0].find_element_by_class_name('table')
		account_list = account_table.find_element_by_tag_name('tbody')
		accounts = account_list.find_elements_by_tag_name('tr')

		remove_button = accounts[0].find_element_by_class_name('glyphicon-remove')
		remove_button_target = remove_button.get_attribute('href')

		url_args = {
			'user_id': BankUser.objects.first().id,
			'pk': BankUser.objects.first().accounts.first().id,
		}
		remove_slug = reverse('bank-account-delete', kwargs=url_args)
		assert remove_button_target.endswith(remove_slug)

	def test_if_delete_link_site_shows_submit_button(self):
		self.browser.get(self.live_server_url)

		user_panels = self.browser.find_elements_by_class_name('panel-group')
		account_table = user_panels[0].find_element_by_class_name('table')
		account_list = account_table.find_element_by_tag_name('tbody')
		accounts = account_list.find_elements_by_tag_name('tr')

		remove_button = accounts[0].find_element_by_class_name('glyphicon-remove')
		remove_button_target = remove_button.get_attribute('href')

		self.browser.get(remove_button_target)

		confirm_button = self.browser.find_elements_by_tag_name('input')[1]
		assert confirm_button.get_attribute('type') == 'submit'

	def test_if_add_link_redirects_to_correct_edit_site(self):
		self.browser.get(self.live_server_url)

		user_panels = self.browser.find_elements_by_class_name('panel-group')
		
		account_table = user_panels[0].find_element_by_class_name('table')
		add_button = account_table.find_element_by_class_name('glyphicon-plus')
		add_account_target = add_button.get_attribute('href')

		add_slug = reverse('bank-account-create', kwargs={'user_id': BankUser.objects.first().id,})
		assert add_account_target.endswith(add_slug)

	def test_if_add_link_site_shows_empty_form(self):
		self.browser.get(self.live_server_url)

		user_panels = self.browser.find_elements_by_class_name('panel-group')
		
		account_table = user_panels[0].find_element_by_class_name('table')
		add_button = account_table.find_element_by_class_name('glyphicon-plus')
		add_account_target = add_button.get_attribute('href')

		self.browser.get(add_account_target)

		iban_field = self.browser.find_element_by_id('id_iban')
		
		assert iban_field.get_attribute('value') == ''

	def test_if_invalid_edit_user_returns_404(self):
		url_args = {
			'user_id': len(BankUser.objects.all()) + 1,
			'pk': BankUser.objects.first().accounts.first().id,
		}
		invalid_edit_slug = reverse('bank-account-update', kwargs=url_args)
		invalid_edit_url = self.live_server_url + invalid_edit_slug

		self.browser.get(invalid_edit_url)
		assert 'Not Found' in self.browser.page_source

	def test_if_invalid_user_account_combination_returns_404(self):
		url_args = {
			'user_id': BankUser.objects.last().id,
			'pk': BankUser.objects.first().accounts.first().id,
		}
		invalid_edit_slug = reverse('bank-account-update', kwargs=url_args)
		invalid_edit_url = self.live_server_url + invalid_edit_slug

		self.browser.get(invalid_edit_url)
		assert 'Not Found' in self.browser.page_source


class AuthorizationTest(StaticLiveServerTestCase):
	
	def setUp(self):
		self.browser = webdriver.PhantomJS()
		self.browser.set_window_size(1024, 768)
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_if_google_login_form_works(self):
		self.browser.get(self.live_server_url)

		assert 'google' in self.browser.page_source

