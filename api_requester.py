import requests
import json

# this program is used for sending search face requests to flask server
my_img = {'file': open('aron_test.jpeg', 'rb')}
my_data = {'k':'1', 'confidence':'0.6'}
r = requests.post('http://127.0.0.1:5000/search_faces/', data=my_data, files=my_img)
data = r.json()
print(data)