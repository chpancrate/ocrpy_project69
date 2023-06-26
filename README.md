# Project 9 of the OpenClassrooms Python developper training

## Develop a web application using the Django Framework

This project is a website using the Django Framework for python and the bootstrap framework for the CSS.
It also uses SQLite to store data.

Beware : a demo database is included in the repository, if you do not want the data you will need to erase it with the following command after the setup of the project.
'''
django-admin flush
''' 

## Installation

### Sources retrival

In order to run the application, clone the following repository in the directory where you want the application to be stored : https://github.com/chpancrate/ocrpy_project9


### Environment setup 

The application runs with Python 3.11.4.

To install python you can download it here : https://www.python.org/downloads/

If you are new to Python you can find information here : https://www.python.org/about/gettingstarted/ 

It is better to run the application in a virtual environment. You can find information on virtual envrionments here : https://docs.python.org/3/library/venv.html 

Once in your virtual environment, the following modules are mandatory :
- Django : 4.2.1
- Pillow : 9.5.0

All the useful modules are in requirements.txt. A quick way to install them is to run the command below in a python terminal:
```
pip install -r requirements.txt
```

## How to run the application

In order to run the application once the setup is complete go in the directory where the application is installed and then use the command : 
```
python manage.py runserver
```

The application will then be accessible at the url : http://127.0.0.1:8000/

## Users and passwords

Some users are setup, they can be found in the file users.txt at the root of the project.
