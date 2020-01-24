## FLASK API project. This project is deployed in AWS.

```javascript
cd YOUR_PROJECT_DIRECTORY_PATH/

virtualenv --no-site-packages env
(sometimes, you need to specify python version depending on the os..as --python=python3) 

source env/bin/activate

pip install -r requirements.txt

export FLASK_APP=app

export FLASK_ENV=development # enables debug mode

python3 app.py 

To run in Gunicorn, gunicorn -b:8080 app:app --log-level debug

You can use the POSTMAN collection to run all the tests, or use a CURL example at the bottom of this document.
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
# Please Run the Postman collection for running tests. Please look at the event_id that is currently returned if you want to delete that in the test. 

#### To get all the events, just copy and paste the following snippet,or put your own token. The permission required for this is get:allevents or a role of a manager.

```
curl -X GET \
  http://ec2-13-52-247-232.us-west-1.compute.amazonaws.com:8080/get/all/events \
  -H 'Accept: */*' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5EaERNamhDTlRCRE1qWXlOVGhDTXpBM1JqWXdSRGxFTjBZME1ETkdOVEE1TkVFeE0wRkdOQSJ9.eyJpc3MiOiJodHRwczovL2Rldi0tYzl5OWNhOS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTQ5MjE3MjU3NTE4MTA0MzA1MTIiLCJhdWQiOlsiZXZlbnQiLCJodHRwczovL2Rldi0tYzl5OWNhOS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTc5ODIwNTk3LCJleHAiOjE1Nzk5MDY5OTcsImF6cCI6IlhsZ1V0bVgxSDQ4dm1LZXlSTjdnMFNTaWluMTdGUWtpIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpldmVudHMiLCJnZXQ6YWxsZXZlbnRzIiwiZ2V0OmV2ZW50cyIsInBhdGNoOmV2ZW50cyIsInBvc3Q6ZXZlbnRzIl19.I8VNNBTQ63Z0lDTFpIjKy009p_M7CXSOhrV_34tw1nMFMRcaypqRTx1c4WLiFp2LEf0a6-zoS_02Q8Z0_yF6xSLit5J-kQXWgZ_3XTdyTgieS_AqAKkwg7Dx7BzBKRsqSZaygq2ejDStoXaWmfNoqV6wxgvfbBKieXl-zEYWYj3eNIGzlfm02fWZ23xEZQhmbKhD-2mCMIIwZXDoJVta5D3bjFHa-_n0mYdMYX0FXv8QSkzXVIOxRm1wtpt9WUFggHLwvsYgOnJQRePhedqbJqxsKhWA6cihRd4HiXTQYtOzhLs7ff6_g13A22L2HwcdBXhMEbLerzRVJuLJ_Sqjpw' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Length: 14' \
  -H 'Content-Type: application/json' \
  -H 'Host: ec2-13-52-247-232.us-west-1.compute.amazonaws.com:8080' 
  ```
  
