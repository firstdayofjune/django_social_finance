from django import template

register = template.Library()

@register.simple_tag
def format_iban(iban_string):
	formatted_iban = ''

	for pos, char in enumerate(iban_string):
		if pos % 4 == 0:
			formatted_iban += ' '
		formatted_iban += char

	return formatted_iban