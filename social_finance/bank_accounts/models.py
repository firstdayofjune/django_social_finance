from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class NoSpecialCharacters(RegexValidator):
	"""Validator checks for special characters. """

	def __init__(self, **kwargs):
		special_characters_regex = r'^.*?[(!"#\$%\(\)\*\+\/\\:;<=>\?@\[\]\^_`\{\|\}~)]+.*?$'
		message = _('Special characters are forbidden')
		code = 'invalid'

		kwargs = { 
			'regex': special_characters_regex,
			'message': message,
			'code': code,
			'inverse_match': True
		}
		
		super(NoSpecialCharacters, self).__init__(**kwargs)


class BankUser(models.Model):
	"""A person using the Bank, is defined by his/her first- and lastname and the bank clerk who created the User."""
	admin = models.ForeignKey(settings.AUTH_USER_MODEL)
	firstname = models.CharField(max_length=255, validators=[NoSpecialCharacters()])
	lastname = models.CharField(max_length=255, validators=[NoSpecialCharacters()])

	def save(self, *args, **kwargs):
		self.clean_fields()
		super(BankUser, self).save(*args, **kwargs)


class BankAccount(models.Model):
	"""A bank-users account which stores the IBAN."""
	iban_regex = r'^[A-Z]{2}\d\d([A-Z]|\d){1,30}$'
	message = _('Not a valid IBAN-format.')
	code = 'invalid'
	iban_format_validator = RegexValidator(iban_regex, message, code)

	holder = models.ForeignKey(BankUser, related_name='accounts')
	iban = models.CharField(max_length=34, validators=[NoSpecialCharacters(), iban_format_validator])

	def save(self, *args, **kwargs):
		self.clean_fields()
		super(BankAccount, self).save(*args, **kwargs)
