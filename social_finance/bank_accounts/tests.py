from bank_accounts import models
from django.test import TestCase


class UserValidationTest(TestCase):

	def test_firstname_does_not_allow_special_characters(self):
		# [^(!"#\$%'\(\)\*\+\/\\:;<=>\?@\[\]\^_`\{\|\}~)]
		pass

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


class UserManipulationTest(TestCase):

	def test_user_cannot_be_updated_by_foreign_admin(self):
		pass

	def test_user_cannot_be_deleted_by_foreign_admin(self):
		pass