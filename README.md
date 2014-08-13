# Tenon proxy

Very basic proxy for API calls to Tenon.io

## Environment variables

The app will need the following environment variables set to work:

- TENON_KEY (the key sent to the tenon api)
- USERNAME (username expected in the credentials of all requests)
- PASSWORD (password expected in the credentials of all requests)
- ORIGINS (domains allowed to make requests)

## Running locally

 Assuming you have pip and virtualenv installed:

 1. Clone this repo
 2. Create a virtualenv

```
     $ cd tenon-api
     $ virtualenv .
     $ source bin/activate
```

 3. Install requirements

 ```
     $ pip install -r requirements.txt
```
 4. Run

 ```
     $ TENON_KEY=*your key* USERNAME=*username* PASSWORD=*password* ORIGINS=*domains you want to allow access to* python app.py
```
