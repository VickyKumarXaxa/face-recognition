import pytest
import psycopg2
import requests
import json
from main import app
from main import search_faces
from main import add_face
from main import add_faces_in_bulk
from main import get_face_info
from main import get_db_connection
from main import allowed_file

# test function for main.py

# test for add_face()
def test_add_face():
    # load image file to upload
    my_img = {'file': open('Aaron_Eckhart_0001.jpg', 'rb')}
    # r = requests.post('http://127.0.0.1:5000/add_face/', files=my_img)
    # send post request to the flask server
    r = app.test_client().post('/add_face/', data=my_img)
    # get the returned data
    data = r.json  
    assert data['status'] == 'OK'

# test for add_faces_in_bulk()
def test_add_faces_in_bulk():
    # load zip file to upload
    my_zip = {'file': open('zip_images.zip', 'rb')}
    # r = requests.post('http://127.0.0.1:5000/add_faces_in_bulk/', files=my_zip)
    # send the post request to flask server
    r = app.test_client().post('/add_faces_in_bulk/', data=my_zip)
    # get the returned data
    data = r.json
    assert data['status'] == 'OK'

# test for search_faces()
def test_search_faces():
    # get the data to send
     my_img = {'file': open('Aaron_Eckhart_0001.jpg', 'rb'), 'k':'1', 'confidence':'0.6'}
     # r = requests.post('http://127.0.0.1:5000/search_faces/', files=my_img)
     # send post request to the flask server
     r = app.test_client().post('/search_faces/', data=my_img)
     # get return the data
     data = r.json
     assert data['status'] == "OK"

# test for get_face_info()
def test_get_face_info():
    # r = requests.post('http://127.0.0.1:5000/get_face_info/', data='1',)
    # send post request to the flask server
    r = app.test_client().post('/get_face_info/', data='1')
    # get the returned data
    data = r.json
    assert data['status'] == "OK"

# test for allowed_file()
def test_allowed_file():
    # send string to the function
    res = allowed_file('abc.jpg')
    # assert
    assert res == True
