import os
import pytest

from bank_accounts import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import TestCase


@pytest.mark.django_db
class UserValidationTest(TestCase):
	fixtures = [
		os.path.join('bank_accounts', 'fixtures', 'test_admins.json'),
		os.path.join('bank_accounts', 'fixtures', 'test_users.json'),
	]

	@classmethod
	def setUpClass(cls):
		super(UserValidationTest, cls).setUpClass()

		cls.User = get_user_model()
		cls.admin = cls.User.objects.filter(username='Peter')[0]
		cls.bank_user = models.BankUser.objects.filter(firstname='Peters', lastname='Client')[0]

		cls.invalid_chars = ['!', '"', '#', '$', '%',
			'(', ')', '[', ']', '{', '}', '|',
			 '*', '+', '/', '\\', ':', '<', '=', '>',
			 ';', '?', '@', '^', '_', '`', '~',
			 ]

	def test_firstname_does_not_allow_special_characters(self):
		with pytest.raises(ValidationError):
			user_args = {
				'admin': self.admin,
				'lastname': 'Valid Name',
			}

			for invalid_char in self.invalid_chars:
				user_args['firstname'] = 'Inval{}d Name'.format(invalid_char)
				new_user = models.BankUser(**user_args)
				new_user.save()

	def test_lastname_does_not_allow_special_characters(self):
		with pytest.raises(ValidationError):
			user_args = {
				'admin': self.admin,
				'firstname': 'Valid Name',
			}

			for invalid_char in self.invalid_chars:
				user_args['lastname'] = 'Inval{}d Name'.format(invalid_char)
				new_user = models.BankUser(**user_args)
				new_user.save()

	def test_iban_does_not_allow_special_characters(self):
		with pytest.raises(ValidationError):
			account_args = {
				'holder': self.bank_user,
			}

			for invalid_char in self.invalid_chars:
				account_args['iban'] = 'DE1212345678012345678{}'.format(invalid_char)
				new_account = models.BankAccount(**account_args)
				new_account.save()

	def test_iban_starts_with_country_code(self):
		with pytest.raises(ValidationError):
			account_args = {
				'holder': self.bank_user,
				'iban': '991212345678012345678',
			}

			new_account = models.BankAccount(**account_args)
			new_account.save()

	def test_iban_has_check_digits_after_country_code(self):
		with pytest.raises(ValidationError):
			account_args = {
				'holder': self.bank_user,
				'iban': '99WW12345678012345678',
			}

			new_account = models.BankAccount(**account_args)
			new_account.save()

	def test_bban_cannot_exceed_thirty_characters(self):
		with pytest.raises(ValidationError):
			account_args = {
				'holder': self.bank_user,
				'iban': 'DE55{0}{0}{0}1'.format('0123456789'),
			}

			new_account = models.BankAccount(**account_args)
			new_account.save()

	def test_well_formated_iban_is_accepted(self):
		accounts_len = len(models.BankAccount.objects.all())
		account_args = {
				'holder': self.bank_user,
				'iban': 'DE1212345678012345678',
			}

		new_account = models.BankAccount(**account_args)
		new_account.save()
		assert len(models.BankAccount.objects.all()) == accounts_len + 1


@pytest.mark.django_db
class UserManipulationTest(TestCase):
	fixtures = [
		os.path.join('bank_accounts', 'fixtures', 'test_admins.json'),
		os.path.join('bank_accounts', 'fixtures', 'test_users.json'),
	]

	def test_user_cannot_be_updated_by_foreign_admin(self):
		username_before = models.BankUser.objects.first().firstname
		self.client.login(username='Paul', password='pauls_password')
		update_user_url = reverse('bank-user-update', kwargs={'pk': 1})
		user_args = {
			'firstname': 'Pauls',
			'lastname': 'Client',
		}
		self.client.post(update_user_url, user_args)

		assert models.BankUser.objects.first().firstname == username_before

	def test_user_cannot_be_deleted_by_foreign_admin(self):
		users_before = len(models.BankUser.objects.all())

		self.client.login(username='Paul', password='pauls_password')
		delete_user_url = reverse('bank-user-delete', kwargs={'pk': 1})
		self.client.delete(delete_user_url)

		assert len(models.BankUser.objects.all()) == users_before

	def test_user_admin_is_set_automatically(self):
		users_before = len(models.BankUser.objects.all())

		self.client.login(username='Peter', password='peters_password')
		create_user_url = reverse('bank-user-create')
		user_args = {
			'firstname': 'Peter',
			'lastname': 'Gabriel',
		}
		self.client.post(create_user_url, user_args)
		
		assert len(models.BankUser.objects.all()) == users_before + 1

		last_users_admin = models.BankUser.objects.last().admin
		assert last_users_admin.username == 'Peter'