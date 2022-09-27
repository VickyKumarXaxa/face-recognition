from lib2to3.pgen2.literals import evalString
from flask import Flask, request, jsonify
import psycopg2
import face_recognition
import pickle
import zipfile
from io import StringIO
from PIL import Image
import imghdr

# the main program to add images in a database
# and do facial recognition on an unknown image using images
# available in the database

app = Flask(__name__)

# allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# dictionary to store details for connecting to the postgresql database
POSTGRES = {
    'user' : 'postgres',
    'pw' : 'password',
    'db' : 'face',
    'host' : 'localhost',
    'port' : '5432',
}

# psycopg2
# pillow

# function to connect to the postgresql database
def get_db_connection():
    # create connection using the details in the POSTGRES dictionary
    conn = psycopg2.connect(
        host=POSTGRES['host'],
        database=POSTGRES['db'],
        user=POSTGRES['user'],
        password=POSTGRES['pw']
    )
    # return the connection
    return conn

# function to verify the filename of uploaded file
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# test route to check if flask server is working or not
@app.route("/")
def hello_world():
    return "<p>Hello, World</p>"

# function for searching and matching faces in the database
@app.route("/search_faces/", methods=['POST'])
def search_faces():
    # if it is a post request
    if request.method == 'POST' :
        # get the uploaded image file
        file = request.files['file']
        # get the k value for "top k" matches
        k = int(request.form.get('k'))
        # list to store the return message
        data_to_return = []
        # get the confidence parameter and convert it to float
        confidence = float(request.form.get('confidence'))

        if file.filename == '':
            #no filename
            return {"status": "ERROR", "body": {"no file name" : data_to_return}}

        # if file is available and filename is in allowed types
        if file and allowed_file(file.filename) :
            # open a database connection by calling get_db_connection()
            con = get_db_connection()
            cur = con.cursor()
            # retrive the face encodings from the database
            cur.execute('SELECT face_encoding from face_image')
            rows = cur.fetchall()
            # append the retrived face encodings to the list known_face_data
            known_face_data = []
            for row in rows :
                data = pickle.loads(row[0])
                known_face_data.append(data)
            
            # load the uploaded image from file
            img = face_recognition.load_image_file(file)
            # get the encoding for the unknown image
            unknown_face_encodings = face_recognition.face_encodings(img)

            # if there is face available in the uploaded image
            if len(unknown_face_encodings) > 0 :
                # for every face in the uploaded image
                for face in range(len(unknown_face_encodings)):
                    # compare the image with each encoding available in the database 
                    match_results = face_recognition.compare_faces(known_face_data, unknown_face_encodings[face], confidence)
                    # get euclidian face distance from each image in the database
                    match_distance = face_recognition.face_distance(known_face_data, unknown_face_encodings[face])
                    # for each match push the distance in dictionary
                    match_data = {}
                    for i in range(len(match_results)) :
                        if match_results[i] == True:
                            match_data[i] = float(match_distance[i])
                            
                    j = 0
                    # retrive the best k matches best on face distance for the face
                    for m in sorted(match_data.items(), key=lambda x: x[1]):
                        row_id = m[0]
                        # get details from the database
                        cur.execute('SELECT * FROM image_data WHERE id = %s', str(row_id+1))
                        data_row = cur.fetchone()
                        id = data_row[0]
                        name = data_row[1]
                        # push the details into data_to_return
                        data_to_return.append({"id":id, "name": name})
                        j = j + 1
                        if j == k :
                            break
                # cleanup and return the details
                cur.close()
                con.close()
                return {"status": "OK", "body": {"matches": data_to_return}}
            else:
                # return no faces found
                cur.close()
                con.close()
                return {"status": "OK", "body": {"no faces" : data_to_return}}


# function for adding faces in the database
@app.route("/add_face/", methods=['POST'])
def add_face():
     if request.method == 'POST' :
        # get image
        file = request.files['file']
        if file.filename == '':
            # no filename
            return {"status": "ERROR", "body": {"no file name" : " "}}

        if file and allowed_file(file.filename) :
            # get name of the person from uploaded file
            fileName = file.filename
            fileNamePart = fileName.split('.')
            stringArray = fileNamePart[0].split('_')
            name = ''
            for i in stringArray :
                if not i.isnumeric():
                    name = name + ' ' + i
                else :
                    version = int(i)
            
            # open database connection
            conn = get_db_connection()
            curr = conn.cursor()
            # load and convert the image to face encoding
            img = face_recognition.load_image_file(file)
            img_encoding = face_recognition.face_encodings(img)[0]
            # convert the encoding to pickle for storage in database
            encodinglist = pickle.dumps(img_encoding)
            version = 1
            # push in the database
            curr.execute('INSERT INTO face_image (face_encoding) VALUES (%s)', (encodinglist,))
            curr.execute('INSERT INTO image_data (name, version) VALUES (%s, %s)', (name, version))
            # commit changes
            conn.commit()
            # close connection
            curr.close()
            conn.close()
            # return message
            return jsonify({"status": "OK", "body": "Image added to database"})


# function for adding images to the database from the zip file
@app.route("/add_faces_in_bulk/", methods=['POST'])
def add_faces_in_bulk():
    if request.method == 'POST' :
        # get the zipfile
        zip_file = request.files['file']
        zipped_images = zipfile.ZipFile(zip_file)
        # extract the images
        zipped_images.extractall()
        # open database connection
        con = get_db_connection()
        curr = con.cursor()
        # for each image in the zipfile
        for i in range(len(zipped_images.namelist())):
            # get the filename of the image
            file_in_zip = zipped_images.namelist()[i]
            if (".jpg" in file_in_zip or ".JPG" in file_in_zip):
                # load the image and encode it into face encoding
                img = face_recognition.load_image_file(file_in_zip)
                img_encoding = face_recognition.face_encodings(img)[0]
                # convert the encoding to pickle for database storage
                img_pickled_data = pickle.dumps(img_encoding)
                # get person name from the image filename
                fileName = file_in_zip
                fileNamePart = fileName.split('.')
                stringArray = fileNamePart[0].split('_')
                name = ''
                for j in stringArray :
                    if not j.isnumeric():
                        name = name + ' ' + j
                    else :
                        version = int(j)
                version = 1
                # add into the database
                curr.execute('INSERT INTO face_image (face_encoding) VALUES (%s)', (img_pickled_data,))
                curr.execute('INSERT INTO image_data (name, version) VALUES (%s, %s)', (name, version))
                # commit changes
                con.commit()
        # close the database connection and return message
        curr.close()
        con.close()
        return {"status": "OK", "body": "Images added to database"}

                
# function for getting the face info
@app.route("/get_face_info/", methods=['POST'])
def get_face_info():
    if request.method == 'POST':
        # get the face id
        id = int(request.get_data())
        # open database connection
        conn = get_db_connection()
        curr = conn.cursor()
        # get information from the database
        curr.execute('SELECT * FROM image_data WHERE id = %s', str(id))
        face_data = curr.fetchone()
        id = 0
        name = ''
        # if data is present in database, get the details 
        if face_data :
            id = face_data[0]
            name = face_data[1]
        # close connection and return
        curr.close()
        conn.close()
        return {"status": "OK", "body": {"id" : id, "name": name}}

if __name__ == '__main__':
    app.run(debug=True)