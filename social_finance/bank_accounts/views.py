from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from bank_accounts import models as bank_account_models

#############################
##### BankUser and BankAccount R
#############################
class AccountListing(generic.ListView):
	"""View listing all BankUsers (and the BankAccounts they have)."""
	model = bank_account_models.BankUser
	template_name = 'bank_accounts/account_listing.html'
	context_object_name = 'customers'
	queryset = bank_account_models.BankUser.objects.order_by('id')
	


#############################
##### BankUser CUD
#############################
class BankUserCreate(generic.edit.CreateView):
	"""View to create a BankUser."""
	model = bank_account_models.BankUser
	success_url = reverse_lazy('home')
	fields = ['firstname', 'lastname']

	def form_valid(self, form):
		"""The user who creates the BankUser automatically becomes the BankUsers admin."""
		form.instance.admin = self.request.user
		return super(BankUserCreate, self).form_valid(form)


class BankUserUpdate(generic.edit.UpdateView):
	"""View to Update a BankUser information."""
	model = bank_account_models.BankUser
	success_url = reverse_lazy('home')
	fields = ['firstname', 'lastname']

	def form_valid(self, form):
		"""Validates that only the BankUsers admin can update the BankUser."""
		if form.instance.admin != self.request.user:
			return HttpResponse('Unauthorized - Only the Users admin can update the User', status=401)
		else:
			return super(BankUserUpdate, self).form_valid(form)



class BankUserDelete(generic.edit.DeleteView):
	"""View to Delete the BankUser."""
	model = bank_account_models.BankUser
	success_url = reverse_lazy('home')

	def delete(self, request, *args, **kwargs):
		"""Validates that only the BankUsers admin can delete the BankUser."""
		bank_user = self.get_object()
		if bank_user.admin != request.user:
			return HttpResponse('Unauthorized - Only the Users admin can delete the User', status=401)
		else:
			return super(BankUserDelete, self).delete(request, *args, **kwargs)


#############################
##### BankAccount CUD
#############################
class BankUserAccountCreate(generic.edit.CreateView):
	"""View to create a new BankAccount (belonging to a BankUser)."""
	model = bank_account_models.BankAccount
	success_url = reverse_lazy('home')
	slug_field = 'holder_id'
	slug_url_kwarg = 'user_id'
	fields = ['iban']

	def form_valid(self, form):
		"""The Holder will be set and a permission chek is performed (only a BankUsers admin is allowed to add an account to the BankUser)."""
		self.holder = get_object_or_404(bank_account_models.BankUser, id=self.kwargs['user_id'])

		if self.holder.admin != self.request.user:
			return HttpResponse('Unauthorized - Only the Account-Holders admin can update the Account', status=401)
		else:
			form.instance.holder = self.holder
			return super(BankUserAccountCreate, self).form_valid(form)



class BankUserAccountUpdate(generic.edit.UpdateView):
	"""View to update a BankAccount (belonging to a BankUser)."""	
	model = bank_account_models.BankAccount
	success_url = reverse_lazy('home')
	slug_field = 'holder_id'
	slug_url_kwarg = 'user_id'
	fields = ['iban']

	def get_queryset(self):
		"""The account for a given holder will be fetched."""
		self.holder = get_object_or_404(bank_account_models.BankUser, id=self.kwargs['user_id'])
		self.account = self.holder.accounts.all().filter(id=self.kwargs['pk'])
		return self.account

	def form_valid(self, form):
		"""Validates that only the account-holders (BankUser) admin can update the account info."""
		if form.instance.holder.admin != self.request.user:
			return HttpResponse('Unauthorized - Only the Account-Holders admin can update the Account', status=401)
		else:
			return super(BankUserAccountUpdate, self).form_valid(form)


class BankUserAccountDelete(generic.edit.DeleteView):
	"""View to delete a BankUser's BankAccount."""
	model = bank_account_models.BankAccount
	success_url = reverse_lazy('home')
	slug_field = 'holder_id'
	slug_url_kwarg = 'user_id'

	def get_queryset(self):
		"""The account for a given holder will be fetched."""
		self.holder = get_object_or_404(bank_account_models.BankUser, id=self.kwargs['user_id'])
		self.account = self.holder.accounts.all().filter(id=self.kwargs['pk'])
		return self.account

	def delete(self, request, *args, **kwargs):
		"""Validates that only the account-holders (BankUser) admin can delete the holders account."""
		bank_account = self.get_object()
		if bank_account.holder.admin != request.user:
			return HttpResponse('Unauthorized - Only the Account-Holders admin can delete the Account', status=401)
		else:
			return super(BankUserAccountDelete, self).delete(request, *args, **kwargs)