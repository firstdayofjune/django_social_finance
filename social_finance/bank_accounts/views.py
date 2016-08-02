from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views import generic
from bank_accounts import models as bank_account_models

# Create your views here.
class AccountListing(generic.ListView):
	model = bank_account_models.BankUser
	template_name = 'bank_accounts/account_listing.html'
	context_object_name = 'users'
	

class BankUserUpdate(generic.edit.UpdateView):
	model = bank_account_models.BankUser
	success_url = '/'
	fields = ['firstname', 'lastname']

class BankUserCreate(generic.edit.CreateView):
	model = bank_account_models.BankUser
	success_url = '/'
	fields = ['firstname', 'lastname']