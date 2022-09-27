Submitter name : Vicky Kumar Xaxa
Roll No. : 2019CSB1131
Course : CS305
----------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------
1. What does this program do
    The program is a Flask server which can be invoked by sending and HTTP post request.
    The program provides an api for adding images of faces of persons in the Postgresql database
    and perform face recognition on an unknown image by using the images available in the database.
    The program also allows addition of images into the database in bulk through zip files and accessing
    the information through the face ids.

----------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------
2. How this program works
    The program starts by initializing the database using init_db if not done once.
    In main.py for doing the face recognition first unknown image is recieved through http post
    request along with "k" for top k matches and confidence for confidence level for matching. Then
    the encodings of the known images are retrived from the database and encoding of the unknown image
    is created. Then using the face_recognition library matches is performed between known encodings and
    the unknown encoding and face distance is calulated. For every matched face according to the
    provided confidence level, the face distance is stored in a dictionary. The dictionary is sorted
    and first k elements are taken if available and their information is received from the database.
    The received information is then sent to the client.

    For adding images, the image is received from the http post request and checked for proper file
    format. After that the name of the person is extracted from filename and metadata from the image.
    The image is then converted into face_recognition encoding and then to pickle and the data is 
    added in the database.

    For adding images in bulk, first the zip file is received from the http post request and the 
    images in the zip file are extracted. Each image is then opened and converted into face_recognition
    encoding and pushed into the Postgresql database.

    For getting the information, sql query is performed using the provided id and data  is returned
    to the request client.

----------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------
3. How to compile and run this program

* Requirements :
    1. Flask
    2. Postgresql
    3. psycopg2
    4. python face_recognition
    5. Pillow
    6. zipfile
    7. Pickle
    8. io
    9. Pytest
    10. Coverage

* Make changes in "POSTGRES" in main.py with details of the Postgresql database if required 

Note : run init_db.py using "python3 init_db.py" to initialize the database once before performing
        any tasks.
        for performing Unit tests all the default files should be available in the directory 

* Unit Test :
    for running the tests visit the directory and use the following commands in the linux terminal :
        pytest test_main.py

* Compile and Run :
    for running the flask server, open the directory in the terminal and write the following command :
        python3 main.py

* Coverage :
    for checking the code coverage open the directory in the terminal and write the following command :
        coverage run --source ./ -m pytest test_main.py
        coverage report -m