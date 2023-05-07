sudo service postgresql status
sudo service postgresql start
sudo service postgresql stop
sudo -u postgres psql
sudo -u postgres psql password
sudo passwd postgres
ALTER USER postgres WITH PASSWORD 'siyamak1981';
psql -h 127.0.0.1 -p 5432 -U postgres


##remove postgres
sudo apt-get --purge remove postgresql postgresql-*

##Docker

docker container rm 2d8519db063d
sudo service docker start
sudo service --status-all | grep '+'
sudo docker login
docker run -it ubuntu /bin/bash
sudo docker-compose run --rm app sh -c "python mana....."
or
docker-compose exec app or web  bash
##Docker postgres database
docker-compose exec db psql --username=hello_django --dbname=hello_django_dev
sudo lsof -i :5432 #kill use posrt 5432
kill -9 pid
\c hello_django_dev
\dt     ####list of relations
   

#redis
sudo systemctl status redis-server
sudo systemctl start redis-server
sudo systemctl stop redis-server
sudo service redis-server stop




#elasticsearch
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable kibana.service
sudo systemctl start elasticsearch.service


sudo systemctl start kibana.service
sudo systemctl stop kibana.service
sudo systemctl start kibana



#icone bx
https://coderthemes.com/minton/layouts/default/icons-boxicons.html


#unittest
docker-compose run app sh -c "python manage.py test -r --debug-mode blog"



## After Run Your Celery Worker
docker-compose run app sh -c "celery -A channels_celery_project beat -l INFO"
celery -A channels_celery_project worker -l INFO
## After Run Your Celery Beat
celery -A channels_celery_project beat -l INFO



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