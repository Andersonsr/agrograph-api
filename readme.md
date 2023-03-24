# Agrograph API
API developed with Django to manage data from Agrograph, 
a platform that uses Neo4j to store geo-localized data from 
agriculture oriented applications, Agrograph is described 
in the following paper https://publicaciones.sadio.org.ar/index.php/JAIIO/article/view/418.


## Endpoints

* ### POST sing-in/ 

  The expected request for this endpoint is displayed bellow. 
All fields are required to create a new user.
  ```
    "email": "youremail@anything.com",
    "password": "supersecurepassword",
    "name": "John Doe",
    "institution": "uni"  
  ```

* ### POST login/

    This endpoint expects to receive a request body like this.
A new session will be initiated and a code 200 response will 
be returned if user exist and password is right.
    
  ```
  {
      "email": "youremail@anything.com",
      "password": "supersecurepassword"
  }
  ```

* ### POST logout/

    this endpoint will end your current session, that is all.

* ### POST edit-profile/ 

  In order to edit its own profile a user must log in first, then a
request like the following one must be sent to this end point. 
email, password, name, institution are required properties and 
must have a value even if not updated. 

  ```
  {
      "email": "youreNEWemail@anything.com",
      "password": "supersecureNEWpassword",
      "name": "John Doe",
      "institution": "uni"
  }
  ```

* ### POST insert/
  This endpoint is used to create new nodes, to do so the request 
sent to this endpoint must have a array of measurements 
identified by the key "data".

  Each measurement has these required properties, longitude (float), 
latitude (float), name (string), unit (string), value (float), 
category (string), date (string).   

  The time (string) property is optional, date must be in 
the '%d/%m/%Y' format, time must be in the format '%H:%M:%S'.

  The category property must have one of the following values:
"solo", "produção vegetal", "produção animal", "meteorologia".

  ```
  {
    "data": [
      {
        "longitude": 1.0, 
        "latitude": 0.0, 
        "name": "potassium",
        "unit": "mmol/dm³",
        "value": 2.1,
        "category": "solo",
        "date": "10/10/2023"
      },
      { 
        "longitude": 1.1, 
        "latitude": 0.1,
        "name": "potassium",
        "unit": "mmol/dm³",
        "value": 2.0,
        "category": "solo",
        "date": "10/10/2023",
        "time": "08:15:33"
      }
    ]
  }
  ```
* ### GET read/
  This endpoint receive a request as bellow, but every key is 
optional, if an empty request is sent to this endpoint it will 
return every measurement owned by the user.
  The polygon must be formed by at least 3 points.
  The name value can contain multiple variables in one string.  
  ```
  {
      "date-min": "10/01/2023",
      "date-max": "01/01/2023",
      "time-min": "12:00:00",
      "time-max": "07:00:00",
      "name": "potassium phosphorus",
      "value-min": 2.0,
      "value-max" 2.3,
      "category" "solo",
      "polygon": [
          {"longitude": 1.0, "latitude": 2.0}, 
          {"longitude": 2.0, "latitude": 2.0},
          {"longitude": 1.0, "latitude": 1.0},
          {"longitude": 2.0, "latitude": 1.0}
       ]
  }
  ```
The result is a json array containing multiple objects. 

## Reminder
to run all test cases the following command line must be executed,
Neo4j database need to be running.

```run tests
python manage.py test agroapi.testCases
```