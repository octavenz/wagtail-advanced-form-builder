# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/bionic64"

  config.vm.network "forwarded_port", guest: 8000, host: 8019
  config.vm.network "forwarded_port", guest: 1080, host: 1080, auto_correct: true

  config.vm.network "private_network", ip: "192.168.20.20"

  config.vm.synced_folder ".", "/home/vagrant/waf", create: true

  # Provider-specific configuration so you can fine-tune various settings
  # config.vm.provider "virtualbox" do |vb|
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end

  config.vm.provision :ansible do |ansible|
    ansible.playbook = "provisioning/server.yml"
    ansible.inventory_path = "provisioning/inventory"
    ansible.limit = "development"
    ansible.verbose = true
  end

  config.vm.provider "virtualbox" do |v|
    v.linked_clone = true
  end
end
