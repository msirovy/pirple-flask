#!/bin/bash -x
pip3 install uwsgi

cat >/etc/systemd/system/uwsgi@.socket<<EOF
Description=Socket for uWSGI app %i

[Socket]
ListenStream=/var/run/uwsgi/%i.socket
SocketUser=www-%i
SocketGroup=www-data
SocketMode=0660

[Install]
WantedBy=sockets.target
EOF

cat >/etc/systemd/system/uwsgi-app@.service<<EOF
[Unit]
Description=%i uWSGI app
After=syslog.target

[Service]
ExecStart=/usr/bin/uwsgi \
        --ini /etc/uwsgi-apps/%i.ini \
        --socket /var/run/uwsgi/%i.socket
User=www-%i
Group=www-data
Restart=on-failure
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all
EOF


mkdir -p /etc/uwsgi-apps





