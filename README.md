## FLASK API project

``` 
cd YOUR_PROJECT_DIRECTORY_PATH/

virtualenv --no-site-packages env

source env/bin/activate

pip install -r requirements.txt

export FLASK_APP=app

export FLASK_ENV=development # enables debug mode

python3 app.py 
```

### You can create an event or events, you can share your events with others.
## Managers can see all events, users can see only the events that belong to them or the ones shared to them.
## These events have APIs so that can be shared for Alexa or something similar 


API's (You need user_id, and Token to use this APIs)
```
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
```
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

```
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
```
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
```
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
```
Role: Manager, Permission: patch:events
/patch/event
required params: id
optional params: event, date, location, website
response:
{
  "success": true
}

```
```
Role: Manager, Permission: delete:events
/delete/event
required params: id 
response: {
  "success": true
}
```

##TESTING 
```
curl --request GET \
  --url http://localhost:5000/get/events \
  --header 'authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5EaERNamhDTlRCRE1qWXlOVGhDTXpBM1JqWXdSRGxFTjBZME1ETkdOVEE1TkVFeE0wRkdOQSJ9.eyJpc3MiOiJodHRwczovL2Rldi0tYzl5OWNhOS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTQ5MjE3MjU3NTE4MTA0MzA1MTIiLCJhdWQiOlsiZXZlbnQiLCJodHRwczovL2Rldi0tYzl5OWNhOS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTc5MzAxNTY1LCJleHAiOjE1NzkzODc5NjUsImF6cCI6IlhsZ1V0bVgxSDQ4dm1LZXlSTjdnMFNTaWluMTdGUWtpIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDpldmVudHMiXX0.S3_rV9LJ0jhMPuwGme7_PBct-bqbuPciYN00kzTG-59BLHyhbFptPxm8tT4KIbK-BXr2n9b19yoGrK4JeQspYEthSc3ijSdQQY7jhNzWwOq4JjPCv2btfbb2bWb9qx6rsiQosPro2Wv5zFJYjiCyEcLCM1x8YN0WyqsoFDwAppVABs6GLmkEbIpchqkYcuQNtSX-sfql3NIX-o0D87LevTswMEE0DoQkEK2mcuwgm2uiEd23PzMHobAv3vWLWGVz6keE4MvDC_4_8XBzBqQuWt9I4nL6moB3gsnDx8F1q43Ief7yVtR0_DHmvUPU95r8tH4ZRqCEkIJhtkqcRTiXog'
  ```
