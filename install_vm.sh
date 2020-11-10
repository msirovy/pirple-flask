#!/bin/bash -x

# Keep it small
cat >/etc/apt/apt.conf.d/00_minimal<<EOF
APT::Install-Recommends "false";
APT::Install-Suggests "false";
EOF


# Run updates
apt -y update
#apt -y upgrade

# Install prerequisites
apt install -y nginx \
  mariadb-client \
	sqlite3 \
  python3-pip \
	python3-setuptools \
  virtualenv \
  vim-tiny \
	rsync \
  tree \
  git \
  htop 

cat >/etc/profile.d/00-aliases.sh<<EOF
alias ll="ls -al"
alias susu="sudo su -"
alias psa="ps aux"
alias nls="netstat -putna"
alias json="python -m json.tool"

EOF

cat >/etc/skel/.vimrc<<EOF
syntax on
set backspace=indent,eol,start
filetype plugin indent on
set ts=2
set sts=2
set sw=2


autocmd Filetype python setlocal ts=4 expandtab

EOF

# Install mysqldb (only testing purposes)
apt install -y mariadb-server



# Prepare application
if [ ! -f /home/flask/.my.cnf ]; then
	useradd -m flask -s /bin/bash
	DB_PWD=$(openssl rand -base64 16)
	mysql -e "create database flask;"
	mysql -e "grant all on flask.* to flask@'%' identified by '"${DB_PWD}"';"
	mysql -e "flush privileges;"

	mysql -u flask -p${DB_PWD} -e 'use flask;'

	echo "Connection to db is OK"

	# Configure my.cnf 
  cat >/home/flask/.my.cnf<<EOF
[mysql]
user = flask
password = ${DB_PWD}

EOF

fi


