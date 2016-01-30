# Item catalog - [ajay]

### Pre-requisites
1) Python
2) Sqlite
3) flask
```sh
    $ apt-get install python-flask
```
4) pip
```sh
    $ apt-get install python-pip
```
5) Sql alchemy
```sh
    $ apt-get install python-sqlalchemy
```
6) oauth2client
```sh
    $ pip install oauth2client 
```
7) httplib2
```sh
    $ pip install httplib2
```
8) dicttoxml (python library)
```sh
    $ pip install dicttoxml
```
### Required Libraries and dependencies
1) Git (optional)
2) A gmail or facebook id 
### Installation

download zip	

Unzip the file 
```sh
$ cd item-catalog
```
or
    
Clone github repository
	
Open the shell in mac/linux or command prompt in windows and navigate to the folder you wnat to clone the repository
	
Make sure you have installed git
	
```sh
	$ git clone https://github.com/ajack13/item-catalog.git
```
this should clone the repository to the folder

# Folders and files 
-------------------------------------------------------------------------------------------
### templates
This folder contains all the html templates of the app 
### static
This folder contsins css,js,images and cover-art of the items
### core.py
Contains python defenitions for the following operations
* Setting up server and run flask
* Add/Delete/Edit category 
* Add/Delete/Edit items
* JSON and XML endpoints
* Oauth autherization and authentication for facebook and gmail

### Other files
* database_setup.py ( code to setup database )
* sampleData.py ( code to add sample data to database)

# Setup project
--------------------------------------------------------------------------------------------
1) Navigate to the project and create the database by running database_setup.py
```sh
    $ python database_setup.py
```
2) Import sample data(optional)
```sh
    $ python sampleData.py 
```
3) Start project by running core.py
```sh
    $ python core.py
```
4) The app is configured to run on port 8000 on your browser
```sh
    http://localhost:8000/
```


### Version
1.1

