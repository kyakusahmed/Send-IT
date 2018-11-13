

[![Build Status](https://travis-ci.org/kyakusahmed/Send-IT.svg?branch=challenge-2%2Fapiv1)](https://travis-ci.org/kyakusahmed/Send-IT)
[![Coverage Status](https://coveralls.io/repos/github/kyakusahmed/Send-IT/badge.svg?branch=challenge-2%2Fapiv1)](https://coveralls.io/github/kyakusahmed/Send-IT?branch=challenge-2%2Fapiv1)


# sendIT
SendIT is a courier service that helps users deliver parcels to different destinations. SendIT provides courier quotes based on weight categories.

[GH-PAGES](https://kyakusahmed.github.io/Send-IT/UI)


 Features
 User side:

- Signup page using personal information.
- Login page .
- make orders page.
- User product details 
- User view and edit profile with map location view
- User signout


As an Admin:

- admin can login or create an account first
- admin view orders page
- admin can change status or location of the parcel delivery
- admin can mark delivered orders
- admin can logout




### How to run the app


Make sure that python 3.4/3.5/3.6/3.7 is installed on your computer

Clone the repo
```
git clone https://github.com/kyakusahmed/sendIT.git
```
Change to the app directory
```
$ cd sendIT
```
Create a virtual enviroment
```
virtualenv (name)
```
Activate the virtualenv
```
For Windows:
	$ (virtualenv name)\scripts\activate, and  	
For Linux: 
 	$source(virtualenv name)/bin/activate
```
Install the required modules from the requirements.txt file 
```
$ pip install -r requirements.txt
```
Run the app
```
$ python run.py
```





| tasks               |    URLS                |  METHOD  |         PARAMS              | 
| ------------------- | -----------------------|----------|-----------------------------|
| get all parcels     | api/v1/parcels         |  GET     |   ---------------           |
|                     |                        |          |                             |
| get a specific      | api/v1/parcels/id      |  GET     |  id                         |
| parcel order        |                        |          |                             |
|                     |                        |          |                             |
| user posts a parcel | api/v1/parcels         |  POST    | sender_id, location, name,  | 
|                     |                        |          | phone, country, destination,| 
|	                    |			                     |	         | weight, price               | 
|                     |                        |          |                             |
| user updates parcel | api/v1/parcels/id      |  PUT     | status                      |
|                     |                        |          |                             |
| Fetch all parcel    | api/v1/users/user_id/  | GET      | user_id                     |
| delivery orders     | parcels                |          |                             |
| by a specific user  |                        |          |                             |
                                        
	
### How to run the Tests:

 open the terminal,activate virtual enviroment in the sendIT directory  and enter:
 ```
 $ pytest
```
 using nosetest  in open the terminal,activate virtual enviroment in the sendIT directory and enter:
 ```
 $ nosetests --with-coverage --cover-tests
 ```


