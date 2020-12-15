Instructions to set up the livis project
-----------------------------------------

- Create a folder named 'LIVIS', where we will set up our Livis Project.
- Create a new virtual environment for the Livis Project through Command Prompt with python version 3.8.5.
- Install all the necessary packages in the environment using the requirements.txt file.
- Set the path directory to the 'LIVIS' folder we created. Start the Livis project using the command: 
	django-admin startproject livis
- Run the following commands:
	python manage.py makemigrations
	python manage.py migrations
	python manage.py createsuperuser


Instructions to set up a new sub-application in the Livis project.
-------------------------------------------------------------------

- Create an app using the following command:
	python manage.py startapp [app_name]
	Eg: python manage.py startapp accounts	
- Make sure to add the app in the 'INSTALLED_APPS' list inside the 'settings.py' file in the 'livis' folder.

