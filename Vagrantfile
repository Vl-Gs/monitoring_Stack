# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.hostname = "monitoring-dev"

  # Network configuration
  config.vm.network "private_network", ip: "192.168.56.10"

  # Port forwarding
  config.vm.network "forwarded_port", guest: 3000, host: 3000  # Grafana
  config.vm.network "forwarded_port", guest: 9090, host: 9090  # Prometheus
  config.vm.network "forwarded_port", guest: 8086, host: 8086  # InfluxDB
  config.vm.network "forwarded_port", guest: 27017, host: 27017  # MongoDB
  config.vm.network "forwarded_port", guest: 1883, host: 1883  # Mosquitto MQTT
  config.vm.network "forwarded_port", guest: 9100, host: 9100  # Node Exporter
  config.vm.network "forwarded_port", guest: 9216, host: 9216  # MongoDB Exporter
  config.vm.network "forwarded_port", guest: 9234, host: 9234  # Mosquitto Exporter

  # VirtualBox specific configuration
  config.vm.provider "virtualbox" do |vb|
    vb.name = "monitoring-dev"
    vb.memory = 4096
    vb.cpus = 2
    
    # Disable audio to prevent CPU spikes
    vb.customize ["modifyvm", :id, "--audio", "none"]
    
    # Enable larger disk space
    unless File.exist?('./monitoring-dev-disk.vdi')
      vb.customize ['createhd', '--filename', './monitoring-dev-disk.vdi', '--size', 50 * 1024]
    end
    vb.customize ['storageattach', :id, '--storagectl', 'SCSI', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', './monitoring-dev-disk.vdi']
  end

  # Sync the project directory
  config.vm.synced_folder ".", "/vagrant", type: "virtualbox"

  # Provision with Ansible
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbooks/main.yml"
    ansible.inventory_path = "inventories/vagrant/hosts"
    ansible.limit = "all"
    ansible.extra_vars = {
      ansible_python_interpreter: "/usr/bin/python3",
      env: "vagrant"
    }
    ansible.groups = {
      "monitoring_servers" => ["default"],
      "database_servers" => ["default"]
    }
    ansible.verbose = "v"
  end

  # Shell provisioning for initial setup
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y python3 python3-pip
    pip3 install ansible
  SHELL
end
