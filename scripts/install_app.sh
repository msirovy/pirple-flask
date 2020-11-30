#!/bin/bash -x

cat >/etc/uwsgi-apps/default.ini<<EOF
[uwsgi]
plugin = python
module = main:app
home = /home/flask/app
master = True
cheap = True
idle = 600

die-on-idle = True
manage-script-name = True

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

	cat >/home/flask/.my.cnf<<EOF
[mysql]
user = flask
password = ${DB_PWD}
host = localhost
EOF

fi


cat >/etc/nginx/sites-enabled/default<<EOF
# Default server configuration
#
server {
	listen 80 default_server;
	listen [::]:80 default_server;

	server_name _;

	location /static {
		root /home/flask/app/static/;
		gzip_static               on;
    expires                   1h;
    add_header                Cache-Control public;
    add_header                ETag '';
    break;
	}

	location / {
		#try_files $uri $uri/ =404;
		include uwsgi_params;
		uwsgi_pass 
		#uwsgi_pass 127.0.0.1:9091;
	}

	location /_stats/ {
		proxy_pass http://127.0.0.1:9092;
	}
}

EOF
