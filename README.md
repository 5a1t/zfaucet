zcash faucet 

Set up instructions (WiP):

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install libpq-dev python-dev
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install nginx

modify settings.py to configure settings.

export proper ENV variables:

	export DJANGO_ENVIRONMENT=prod

	export DJANGO_SECRET_KEY=xxx

	export DJANGO_POSTGRESQL_PASSWORD=xxx



pip install -r requirements.txt
pip install -r requirements-prod.txt
sudo su - postgres
createdb django
createuser -P django
psql
GRANT ALL PRIVILEGES ON DATABASE django TO django;
python manage.py syncdb
gunicorn --workers=2 zfaucet.wsgi
sudo service nginx start
vim /etc/nginx/sites-available/zfaucet

    server {
        server_name faucet.yoursite.com;

        access_log off;

        location /static/ {
            alias /home/ansible/static/;
        }

        location / {
                proxy_pass http://127.0.0.1:8000;
                proxy_set_header X-Forwarded-Host $server_name;
                proxy_set_header X-Real-IP $remote_addr;
                add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
        }
    }

cd /etc/nginx/sites-enabled
sudo ln -s ../sites-available/zfaucet
sudo rm default
python manage.py collectstatic


(assuming user is ansible and has created a virtualenv called zfaucet)

crontab -e 
*/5 * * * * /home/ansible/run_health.sh
*/5 * * * * /home/ansible/.virtualenvs/zfaucet/bin/python /home/ansible/zfaucet/manage.py healthcheck


run_health.sh:
#!/bin/bash
su ansible
source /home/ansible/set_prod.sh
cd /home/ansible/zfaucet
/home/ansible/.virtualenvs/zfaucet/bin/python ./manage.py healthcheck


run_sweep.sh
#!/bin/bash
su ansible
source /home/ansible/set_prod.sh
cd /home/ansible/zfaucet/pyzfaucet

/home/ansible/.virtualenvs/zfaucet/bin/python -m pyzcash.examples.sweep_all mfu8LbjAq15zmCDLCwUuay9cVc2FcGuY4d

