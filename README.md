# Points Boost

## Backend

### Setup

Setup virtualenv
```
    $ sudo easy_install virtualenv
    $ mkvirtualenv pointsboost
    $ cd backend
    $ pip install -r requirements.txt
```

Run server

```
$ python backend/app/routes.py 
```

Examples
```
$ curl -X POST http://localhost:5000/users?fitbit_token=tokenblah
$ curl -X GET http://localhost:5000/users/68efdace-5511-11e6-a1cc-02426236196d/challenges/_new
```

## Frontend

* Install NodeJS 4.4.1
* `cd` in to the `frontend/` directory
* `npm install -g bower gulp`
* `npm install`
* `bower install`
* `gulp serve`
