from django.shortcuts import render
from bank_accounts.models import BankUser

# Create your views here.
def account_listing(request):
	users = BankUser.objects.all()
	return render(request, 'bank_accounts/account_listing.html', {'users': users})	