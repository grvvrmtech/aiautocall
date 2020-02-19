sudo apt-get install nginx uwsgi uwsgi uwsgi-plugin-python3  
sudo openssl genrsa -des3 -out nginx.key 1024  
sudo openssl req -new -key nginx.key -out nginx.csr  
sudo cp nginx.key nginx.key.org  
sudo openssl rsa -in nginx.key.org -out nginx.key  
sudo openssl x509 -req -days 365 -in nginx.csr -signkey nginx.key -out nginx.crt
sudo mkdir /etc/nginx/ssl  
sudo mv nginx.key /etc/nginx/ssl/nginx.key  
sudo mv nginx.crt /etc/nginx/ssl/nginx.crt  
cd /etc/nginx/sites-enabled/  
sudo ln -s /home/gaurav/aiautocall/autocall_nginx.conf autocall_nginx.conf  
cd -

pwd
autocall_nginx.conf    :   change all address to change directory
autocall/settings.py :  allow host 192.168.5.245
autocall_uwgsi_ini : change chdr and socket to current directory
autocall/wsgi.py  :    change path to current directory
