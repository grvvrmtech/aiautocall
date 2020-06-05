#!/bin/bash
CURRENT_PATH=`pwd`
LOCAL_IP=192.168.5.27
WS_IP=192.168.5.27
WS_PORT=2700

sudo apt-get install nginx uwsgi uwsgi uwsgi-plugin-python3
sudo openssl genrsa -des3 -out nginx.key 1024
sudo openssl req -new -key nginx.key -out nginx.csr
sudo cp nginx.key nginx.key.org
sudo openssl rsa -in nginx.key.org -out nginx.key
sudo openssl x509 -req -days 365 -in nginx.csr -signkey nginx.key -out nginx.crt
sudo mkdir -p /etc/nginx/ssl
sudo mv nginx.key /etc/nginx/ssl/nginx.key
sudo mv nginx.crt /etc/nginx/ssl/nginx.crt

sudo rm nginx.csr
sudo rm nginx.key.org

cp ${CURRENT_PATH}/base_nginx.conf ${CURRENT_PATH}/autocall_nginx.conf
sed -i 's:CURRENT_PATH:'${CURRENT_PATH}':g' autocall_nginx.conf
sed -i 's:LOCAL_IP:'${LOCAL_IP}':g' autocall_nginx.conf
sed -i 's:WS_IP:'${WS_IP}':g' autocall_nginx.conf
sed -i 's:WS_PORT:'${WS_PORT}':g' autocall_nginx.conf

cd /etc/nginx/sites-enabled/
sudo rm autocall_nginx.conf
sudo ln -s ${CURRENT_PATH}/autocall_nginx.conf autocall_nginx.conf
cd -



cp autocall/base_settings.py autocall/settings.py
cp base_uwgsi.ini autocall_uwgsi.ini
cp autocall/base_wsgi.py autocall/wsgi.py
sed -i 's:LOCAL_IP:'${LOCAL_IP}':g' autocall/settings.py
sed -i 's:CURRENT_PATH:'${CURRENT_PATH}':g' autocall_uwgsi.ini
sed -i 's:CURRENT_PATH:'${CURRENT_PATH}':g' autocall/wsgi.py

python3.5 -m venv env
source env/bin/activate
python3.5 -m pip install -r requirements.txt


