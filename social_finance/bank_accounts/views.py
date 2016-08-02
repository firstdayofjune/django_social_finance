from django.shortcuts import render
from django.views import generic
from bank_accounts.models import BankUser

# Create your views here.
class AccountListing(generic.ListView):
	model = BankUser
	template_name = 'bank_accounts/account_listing.html'
	context_object_name = 'users'
	



