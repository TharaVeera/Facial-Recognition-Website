# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 08:51:41 2018

@author: 1023191
"""

import json
import requests
client_id= "" #depends on what your account/app config 
client_secret = "" #depends on what your account/app config 
redirect_uri = "https://localhost:5000"



parameters = {"response_type": "code", 
              "client_id": client_id,
              "redirect_uri": redirect_uri,
              "state": "DCEeFWf45A53sdfKef424", "scope": ["r_basicprofile", "r_emailaddress"] }
url = "https://www.linkedin.com/oauth/v2/authorization"
response = requests.get(url, params = parameters)
print(response.url)
#print(response.content)

#this is the code given by the response.url. It will be different for you
code = "AQRQoMWSlJ6RP6llxVg-1vXVsnO0mYzMLOAmaWXS2WhseaG1bjLQO-b1IOosac4M8gwI_fxQXOJx0YJ0dDYSx6pon7GrZsAn8nc2mFPMT70adxxxmYjPwOleCBFJWn3fXnbjmlnIrWUBAl0lPk4bx13AtvtoVrwQWaHVex8o"
state="DCEeFWf45A53sdfKef424"

parameters2 = {"grant_type": "authorization_code", "code": code, 
               "redirect_uri": redirect_uri, "client_id": client_id, 
               "client_secret": client_secret}
url2 = "https://www.linkedin.com/oauth/v2/accessToken"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
response2 = requests.post(url2, params = parameters2, headers = headers, allow_redirects = True).json()
print(response2)

access = response2["access_token"]
expires = response2["expires_in"]
print(access)
print(expires)

url3 = "https://api.linkedin.com/v1/people/~"
headers3 = {"Connection": "Keep-Alive", 
           "Authorization": "Bearer " + access}
parameters3= {"format":"json"}
response3 = requests.get(url3, params=parameters3, headers = headers3).json()
print(response3)
person_id = response3["id"]
print(person_id)

id = "IeCxPtCggJ"
url5 = "https://api.linkedin.com/v1/people/~"
parameters5= {"user-id": id, "format":"json"}
response5 = requests.get(url5, params=parameters5, headers = headers3).json()
print(response5)

#ANYTHING USING LINKEDIN V2 WILL NOT WORK UNLESS YOU HAVE LINKEDIN DEVELOPER ACCESS. Try this once you have approval
ip = "172.16.31.82"
url4 = "https://api.linkedin.com/v2/clientAwareMemberHandles"

parameters4 = {"q":"handleString", "handleString": "tveeramach@yahoo.com"}
headers4 = {"X-Forwarded-For": ip, 
           "Caller-Account-Age": "2", "Caller-Device-UUID": "" ,"Connection": "Keep-Alive", 
           "Authorization": "Bearer " + access}
response4 = requests.get(url4, params = parameters4, headers = headers4)
print(response4.content)
print(response4.status_code)
