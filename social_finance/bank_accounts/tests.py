import os
import pytest

from bank_accounts import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase


@pytest.mark.django_db
class UserValidationTest(TestCase):
	fixtures = [
		os.path.join('bank_accounts', 'fixtures', 'test_admins.json'),
	]

	@classmethod
	def setUpClass(cls):
		super(UserValidationTest, cls).setUpClass()

		cls.User = get_user_model()
		cls.admin = cls.User.objects.filter(username='Peter')[0]


	def test_firstname_does_not_allow_special_characters(self):
		# [^(!"#\$%\(\)\*\+\/\\:;<=>\?@\[\]\^_`\{\|\}~)]
		with pytest.raises(ValidationError):
			user_args = {
				'admin': self.admin,
				'firstname': 'Inval|d name',
				'lastname': 'Valid Name',
			}
			new_user = models.BankUser(**user_args)
			new_user.save()

	def test_lastname_does_not_allow_special_characters(self):
		pass

	def test_iban_does_not_allow_special_characters(self):
		pass

	def test_iban_starts_with_country_code(self):
		pass

	def test_iban_has_check_digits_after_country_code(self):
		pass

	def test_bban_cannot_exceed_thirty_characters(self):
		pass

	def test_bban_cannot_contain_special_characters(self):
		pass


@pytest.mark.django_db
class UserManipulationTest(TestCase):
	fixtures = [
		os.path.join('bank_accounts', 'fixtures', 'test_admins.json'),
	]

	@classmethod
	def setUpClass(cls):
		super(UserManipulationTest, cls).setUpClass()
		cls.User = get_user_model()

		# Fix the clear-text passwords of fixtures
		for user in cls.User.objects.all():
			user.set_password(user.password)
			user.save()


	def test_user_cannot_be_updated_by_foreign_admin(self):
		pass

	def test_user_cannot_be_deleted_by_foreign_admin(self):
		pass