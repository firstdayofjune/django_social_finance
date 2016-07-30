# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ogarcia/arch-net-x64"
  config.vm.box_url = "https://atlas.hashicorp.com/ogarcia/boxes/arch-net-x64"

  config.vm.host_name = "social-django"
  config.vm.synced_folder ".", "/home/vagrant"

  # Provider-specific configuration  
  config.vm.provider "virtualbox" do |vb|
    # Customize the amount of memory on the VM:
    vb.memory = "2048"
  end

  # Create a forwarded port mapping
  config.vm.network "forwarded_port", guest: 80, host: 8080
    auto_correct: true
  # Forward Django development-server port
  config.vm.network "forwarded_port", guest: 8000, host: 8000
    auto_correct: true
  # Forward PostgreSQL port
  config.vm.network "forwarded_port", guest: 5432, host: 15432
    auto_correct: true

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Enable provisioning with a shell script.
  config.vm.provision :shell, path: "bootstrap.sh"
end
