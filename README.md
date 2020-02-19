sudo apt-get install ngnix uwsgi uwsgi uwsgi-plugin-python3  
sudo openssl genrsa -des3 -out nginx.key 1024  
sudo openssl req -new -key nginx.key -out nginx.csr  
sudo cp nginx.key nginx.key.org  
sudo openssl rsa -in nginx.key.org -out nginx.key  
sudo openssl x509 -req -days 365 -in nginx.csr -signkey nginx.key -out nginx.crt  
sudo mv nginx.key /etc/nginx/ssl/nginx.key  
sudo mv nginx.crt /etc/nginx/ssl/nginx.crt  
cd /etc/nginx/sites-enabled/  
sudo ln -s /home/gaurav/aiautocall/autocall_nginx.conf autocall_nginx.conf  
cd -  

