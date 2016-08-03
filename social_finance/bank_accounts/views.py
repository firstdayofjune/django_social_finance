from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from bank_accounts import models as bank_account_models

#############################
##### BankUser and BankAccount R
#############################
class AccountListing(generic.ListView):
	model = bank_account_models.BankUser
	template_name = 'bank_accounts/account_listing.html'
	context_object_name = 'users'
	

#############################
##### BankUser CUD
#############################
class BankUserCreate(generic.edit.CreateView):
	model = bank_account_models.BankUser
	success_url = reverse_lazy('home')
	fields = ['firstname', 'lastname']

	def form_valid(self, form):
		form.instance.admin = self.request.user
		return super(BankUserCreate, self).form_valid(form)


class BankUserUpdate(generic.edit.UpdateView):
	model = bank_account_models.BankUser
	success_url = reverse_lazy('home')
	fields = ['firstname', 'lastname']

	def form_valid(self, form):
		if form.instance.admin != self.request.user:
			return HttpResponse('Unauthorized - Only the Users admin can update the User', status=401)
		else:
			return super(BankUserUpdate, self).form_valid(form)



class BankUserDelete(generic.edit.DeleteView):
	model = bank_account_models.BankUser
	success_url = reverse_lazy('home')

	def delete(self, request, *args, **kwargs):
		bank_user = self.get_object()
		if bank_user.admin != request.user:
			return HttpResponse('Unauthorized - Only the Users admin can delete the User', status=401)
		else:
			return super(BankUserDelete, self).delete(request, *args, **kwargs)


#############################
##### BankAccount CUD
#############################
class BankUserAccountCreate(generic.edit.CreateView):
	model = bank_account_models.BankAccount
	success_url = reverse_lazy('home')
	slug_field = 'holder_id'
	slug_url_kwarg = 'user_id'
	fields = ['iban']

	def form_valid(self, form):
		self.holder = get_object_or_404(bank_account_models.BankUser, id=self.kwargs['user_id'])

		if self.holder.admin != self.request.user:
			return HttpResponse('Unauthorized - Only the Account-Holders admin can update the Account', status=401)
		else:
			form.instance.holder = self.holder
			return super(BankUserAccountCreate, self).form_valid(form)



class BankUserAccountUpdate(generic.edit.UpdateView):
	model = bank_account_models.BankAccount
	success_url = reverse_lazy('home')
	slug_field = 'holder_id'
	slug_url_kwarg = 'user_id'
	fields = ['iban']

	def get_queryset(self):
		self.holder = get_object_or_404(bank_account_models.BankUser, id=self.kwargs['user_id'])
		self.account = self.holder.accounts.all().filter(id=self.kwargs['pk'])
		return self.account

	def form_valid(self, form):
		if form.instance.holder.admin != self.request.user:
			return HttpResponse('Unauthorized - Only the Account-Holders admin can update the Account', status=401)
		else:
			return super(BankUserAccountUpdate, self).form_valid(form)


class BankUserAccountDelete(generic.edit.DeleteView):
	model = bank_account_models.BankAccount
	success_url = reverse_lazy('home')
	slug_field = 'holder_id'
	slug_url_kwarg = 'user_id'

	def get_queryset(self):
		self.holder = get_object_or_404(bank_account_models.BankUser, id=self.kwargs['user_id'])
		self.account = self.holder.accounts.all().filter(id=self.kwargs['pk'])
		return self.account

	def delete(self, request, *args, **kwargs):
		bank_account = self.get_object()
		if bank_account.holder.admin != request.user:
			return HttpResponse('Unauthorized - Only the Account-Holders admin can delete the Account', status=401)
		else:
			return super(BankUserAccountDelete, self).delete(request, *args, **kwargs)