from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class BankUser(models.Model):
	no_special_characters_regex = r'^.*?[(!"#\$%\(\)\*\+\/\\:;<=>\?@\[\]\^_`\{\|\}~)]+.*?$'
	message = _('Special characters are forbidden')
	code = 'invalid'
	no_special_characters = RegexValidator(
		no_special_characters_regex,
		message,
		code,
		inverse_match=True,
	)

	admin = models.ForeignKey(settings.AUTH_USER_MODEL)
	firstname = models.CharField(max_length=255, validators=[no_special_characters])
	lastname = models.CharField(max_length=255, validators=[no_special_characters])

	def save(self, *args, **kwargs):
		self.clean_fields()
		super(BankUser, self).save(*args, **kwargs)


class BankAccount(models.Model):
	no_special_characters_regex = r'^.*?[(!"#\$%\(\)\*\+\/\\:;<=>\?@\[\]\^_`\{\|\}~)]+.*?$'
	message = _('Special characters are forbidden')
	code = 'invalid'
	no_special_characters = RegexValidator(
		no_special_characters_regex,
		message,
		code,
		inverse_match=True,
	)

	holder = models.ForeignKey(BankUser)
	iban = models.CharField(max_length=34, validators=[no_special_characters])

	def save(self, *args, **kwargs):
		self.clean_fields()
		super(BankAccount, self).save(*args, **kwargs)