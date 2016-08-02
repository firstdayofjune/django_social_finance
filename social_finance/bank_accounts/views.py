from django.shortcuts import render
from bank_accounts.models import BankAccount

# Create your views here.
def account_listing(request):
	accounts = BankAccount.objects.all()
	return render(request, 'bank_accounts/account_listing.html', {'accounts': accounts})	