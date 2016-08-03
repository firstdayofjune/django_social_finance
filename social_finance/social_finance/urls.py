"""social_finance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from bank_accounts import views as bank_account_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', bank_account_views.AccountListing.as_view(), name='home'),
    url('accounts/', include('allauth.urls')),
    # BankUser CUD
    url(r'^bank-user-create/$', bank_account_views.BankUserCreate.as_view(), name='bank-user-create'),
    url(r'^bank-user-update/(?P<pk>[0-9]+)/$', bank_account_views.BankUserUpdate.as_view(), name='bank-user-update'),
    url(r'^bank-user-delete/(?P<pk>[0-9]+)/$', bank_account_views.BankUserDelete.as_view(), name='bank-user-delete'),
    # BankAccount CUD
    url(r'^bank-user/(?P<user_id>[0-9]+)/account-create/$', bank_account_views.BankUserAccountCreate.as_view(), name='bank-account-create'),
    url(r'^bank-user/(?P<user_id>[0-9]+)/account-update/(?P<pk>[0-9]+)/$', bank_account_views.BankUserAccountUpdate.as_view(), name='bank-account-update'),
    url(r'^bank-user/(?P<user_id>[0-9]+)/account-delete/(?P<pk>[0-9]+)/$', bank_account_views.BankUserAccountDelete.as_view(), name='bank-account-delete'),
    
]
