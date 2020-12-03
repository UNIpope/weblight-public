# Weblights 
This is a website/api to interact with kasa smart devices.

*The Ids and Secrets have been removed from this application for the public repo.*

The website uses Flask, OAuth and bootstrap to secure, run and style the application.
python-kasa is utilised to address lights and plugs on the network.(strip.py)
This can then accessed through a flask api/site allowing other application to 
access this functionality.

## Auth0
The Flask website is secured using the Auth0 platform.
Steps takes by Flask:
1. authlib.integrations.flask_client import OAuth
2. oauth setup 
3. login page
4. callback
	- auth0.authorize_access_token()
	- get user info
	- flask session
	- ['jwt_payload'] ['profile']
5. redirect to wherever
6. logout
	- clear session
	- auth0 rederect client id 