# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "debian/stretch64"
  vmname = "basil"

  config.vm.hostname = "#{vmname}"
  config.vm.network "private_network", ip: "192.168.58.111"
  config.vm.synced_folder "./", "/opt/basil/"

  config.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = 1
      vb.name = "#{vmname}"
  end

  $script = <<-SCRIPT
  sudo apt-get update
  sudo apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common
  curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
  sudo apt-get update
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io
  sudo curl -L https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  SCRIPT

  config.vm.provision "shell", preserve_order: true,
    inline: $script
end
