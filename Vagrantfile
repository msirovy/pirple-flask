Vagrant.configure("2") do |config|
  config.vm.box = "debian/buster64"
  config.vm.provider "virtualbox" do |v|
    v.name = "flask-pirple"
    v.memory = 1024
    v.cpus = 1
  end
  
  # Networking
  config.vm.hostname = "flask"
  config.vm.network "forwarded_port", guest: 80, host: 18080
	
	# shared folder 
	config.vm.synced_folder './app', '/tmp/app', type: 'rsync'

	# install VM and configure app
  config.vm.provision "shell", path: "install_vm.sh"
  config.vm.provision "shell", path: "install_uwsgi.sh"
  config.vm.provision "shell", path: "install_app.sh"


end
