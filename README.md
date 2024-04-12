# Run Project

1. [run project](#Run Project)
    * [requirements](#Requirements)
    * [mysql](#setup-mysql)
    * [celery](#RUN CELERY)

## Run Project
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py runserver
* ###### Requirements:
  I use `pip freeze ` library for create requirements.txt
     ```text
      pip install -r requirement.txt
     ```

* ###### RUN CELERY:
  for run celery go to the directory of celery.py and run this:
     ```
      celery -A report_exchange worker -l info
     ```
  for run celery go to the directory of celery.py and run this:
     ```
      celery -A report_exchange beat -l info
    ```

* ###### SETUP MYSQL
  for see the status of mysql
    ```
       systemctl status mysql.service
    ```
  for start the mysql server
    ```
       systemctl start mysql.server 
    ```
  for stop the mysql server
    ```
       systemctl stop mysql.server 
    ```
