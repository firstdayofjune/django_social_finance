from django.shortcuts import get_object_or_404
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


class BankUserAccountUpdate(generic.edit.UpdateView):
	model = bank_account_models.BankAccount
	success_url = '/'
	slug_field = 'holder_id'
	slug_url_kwarg = 'user_id'
	fields = ['iban']

	def get_queryset(self):
		self.holder = get_object_or_404(bank_account_models.BankUser, id=self.kwargs['user_id'])
		self.account = self.holder.accounts.all().filter(id=self.kwargs['pk'])
		return self.account

class BankUserAccountCreate(generic.edit.CreateView):
	model = bank_account_models.BankAccount
	success_url = '/'
	slug_field = 'holder_id'
	slug_url_kwarg = 'user_id'
	fields = ['iban']
