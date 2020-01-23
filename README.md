## FLASK API project

```javascript
cd YOUR_PROJECT_DIRECTORY_PATH/

virtualenv --no-site-packages env
(sometimes, you need to specify python version depending on the os..as --python=python3) 

source env/bin/activate

pip install -r requirements.txt

export FLASK_APP=app

export FLASK_ENV=development # enables debug mode

python3 app.py 
```

#### You can create an event or events.
#### Managers can see all events, users can see only the events that belong to them (or the ones shared to them -- TODO after capstone project) 



API's (You need user_id, and Token to use this APIs)
```python
Role: Public
/create/user - creates users to interact with the event APIs.
params required: name

response: {
  "status": 200,
  "user": [
    {
      "name": "sage",
      "user_id": 1
    }
  ]
}
```
```python
Role: Public
/get/user

response: {
  "status": 200,
  "user": [
    {
      "name": "sage",
      "user_id": 1
    }
  ]
}
```

```python
Role: user, Permission: get:events
/get/events
required params: {id} ID of a user whose events are desired.
{
  "events": [
    {
      "data": "Feb 5th",
      "event": "TED",
      "event_id": 6,
      "location": "Los Angeles",
      "user_id": 1,
      "website": "https://www.onedayu.com/"
    },
    {
      "data": "Feb 5th",
      "event": "aya",
      "event_id": 7,
      "location": "Los Angeles",
      "user_id": 1,
      "website": "https://www.onedayu.com/"
    }
  ],
  "success": true
}

```
```python
Role: user, Permission: post:events
/post/event
required params: {   
	"user_id": 1,
	"event": "Oneday University",
	"date": "Feb 5th",
	"location": "Los Angeles",
	"website": "https://www.onedayu.com/"
}
response:
{
  "events": "event created",
  "status": 200
}
```
```python
Role: Manager, Permission: get:allevents
required params: None. 
/get/allevents
reponse: {
  "events": [
    {
      "data": "Feb 5th",
      "event": "TED",
      "event_id": 6,
      "location": "Los Angeles",
      "user_id": 1,
      "website": "https://www.onedayu.com/"
    },
    {
      "data": "Feb 5th",
      "event": "aya",
      "event_id": 7,
      "location": "Los Angeles",
      "user_id": 1,
      "website": "https://www.onedayu.com/"
    },
    {
      "data": "Feb 5th",
      "event": "Oneday University",
      "event_id": 8,
      "location": "Los Angeles",
      "user_id": 1,
      "website": "https://www.onedayu.com/"
    }
```
```python
Role: Manager, Permission: patch:events
/patch/event
required params: id
optional params: event, date, location, website
response:
{
  "success": true
}

```
```python
Role: Manager, Permission: delete:events
/delete/event
required params: id 
response: {
  "success": true
}
```

## TESTING 
```javascript
curl --request GET \
  --url http://localhost:5000/get/events \
  --header 'authorization: Bearer <TOKEN>'
  ```
