sudo /etc/init.d/nginx restart
uwsgi --ini autocall_uwgsi.ini --plugin python3
