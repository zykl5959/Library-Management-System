how to compile, build, and install your application. It
should include any technical dependencies (language, frameworks, platform, OS,
software libraries, software versions, etc.).

This Instruction is for Mac OS

In this project, we use Python Web framework called Django,MySQL Databse;



Django:

1、Install Python 3.7.2
Get the latest version of Python at https://www.python.org/downloads/, and follow the guide line

2、Check the version of Python:
Open the Terminal and type:
python3 --version
## Python 3.7.2

3、Install Django 2.1.7
Open the Terminal and type:
pip3 install Django==2.1.7
## It will install the lastest version

4、Check the version of Django:
1、open a Python console by type :python3
>>> import django
>>> django.VERSION
(2, 1, 7, 'final', 0)


Database

1、Download the disk image (.dmg) file https://dev.mysql.com/downloads/mysql/ and install following the guideline
We should define a password for the root user, and also toggle whether MySQL Server should start after the configuration step is complete.

2、Import Database:
	a)Open the console and start the interactive MySQL mode: mysql -uroot -p, then type password
	b) create database using name "mydb";
	b)use mydb;
	c)source <path_of_your_.sql> //project.sql

Connect to Database:
1、you’ll need a DB API driver like mysqlclient. download: https://dev.mysql.com/downloads/connector/python/
2、open /Library/Library/settings.py：
3、We should do so setting 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',# engine, we use mysql
        'NAME':'mydb',			# database name
        'USER':'root',			# username
        'PASSWORD':'******',	# mysql Host ip, default :'localhost'
        'HOST': 'localhost',  # mysql Host ip, default :'localhost'
        'PORT': '3306',  # mysql sever port, default: '3306'
    }
}

Finally, we can start to run our app:
	1、In terminal type: python3 manage.py runserver;
	2、Starting development server at http://127.0.0.1:8000
	3、In browser, type http://127.0.0.1:8000







