# Django Social Finance
A small django application for storing users (BankUser) and IBAN-accounts (BankAccounts) belonging to them.

## SetUp
The package comes with a preconfigured vagrant VM. To use the machine, vagrant has to be installed on your system (get vagrant [here](https://www.vagrantup.com/downloads.html)). Furthermore a VirtualBox installation is required, to run the VagrantVM (https://www.virtualbox.org).

Clone the project and cd into the directory

`$ git clone https://github.com/firstdayofjune/django_social_finance.git && cd django_social_finance`

Now setup the vagrant Virtual Machine.

`$ vagrant up`

The machine image will now be downloaded and the machine will be provisioned. (Depending on your internet connection, this may take some time as the VirtualBox-image has to be downloaded and fully updated first).

After provisioning, you will be prompted to login to your machine using ssh. You can do so running:

`$ vagrant ssh` (the password is "*vagrant*")

## Run
You may now start the Django application from `social_finance` directory typing:

`cd social_finance`

`python manage.py runserver 0.0.0.0:8000`

Now, if you visit [localhost:8000](http://localhost:8000/) in your local browser, you should be greeted by a nice pink pony with magical powers and a login-mask.


**Attention:** To check if the installation was successfull upfront, refer to the Test-Section and run the tests beforehand.

### First Login
You could either login using your google account or by hijacking one of the three preexisting admins (Peter, Paul and Mary).

Password of the existing accounts is `<account_name>s_password` (e.g. account-name: *Mary*, password: *marys_password*).


### Test
Some unit- and integration-tests are provided, and can be run using the `py.test` command:

#### Unittests:
`cd social_finance`

`py.test bank_accounts/tests.py`

#### Integration tests:
`cd social_finance`

`py.test functional_tests/`


## Issues
Unfortunately, when provisioning the VM in a Windows environment, the mounting of shared folders is leading to errors and the application can therefore not be run directly. If on Windows, you could still follow the abovementioned progress, but you would have to clone the repository again from within the vm (so after connecting to the machine using `vagrant ssh`).
Furthermore, git has to be installed to do so (`sudo pacman -S git`) and the fixtures have to be loaded, if you want the application to contain initial data (refer to bootstrap.sh [93:96] to see how the loading of fixtures can be done).
