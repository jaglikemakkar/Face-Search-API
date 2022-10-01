from fileinput import filename
from flask import Flask, render_template, url_for, request, redirect, jsonify
from flaskext.mysql import MySQL
import face_recognition
import os, zipfile, multiprocessing, shutil
import numpy as np
from SortedList import SortedList

# Class to store the HTML
class Frontend:

    # Form for add_face 
    def add_face(self):

        # Finding total number of images present in database
        conn = DbConnection(db)
        cnt_imgs = conn.execute_select("select count(*) from images")[0]

        # Returning the form
        return '''<!doctype html>
        <title>Add Face</title>
        <h1>Upload image.</h1>
        <h2>Total images in database = %s </h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
        ''' % (cnt_imgs)
    
    # Frontend for add_faces_in_bulk page
    def add_faces_in_bulk(self):

        # Finding number of images present in database
        conn = DbConnection(db)
        cnt_imgs = conn.execute_select("select count(*) from images")[0]

        # Returning the HTML form
        return '''<!doctype html>
        <title>Add Faces In Bulk</title>
        <h1>Upload Zip File.</h1>
        <h2>Total images in database = %s </h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
        ''' % (cnt_imgs)

    # HTML form for search_faces page
    def search_faces(self):

        # Finding the number of images present in db
        conn = DbConnection(db)
        cnt_imgs = conn.execute_select("select count(*) from images")[0]

        # Returning the HTML form
        return '''<!doctype html>
        <title>Add Face</title>
        <h1>Search Faces.</h1>
        <h2>Total images in database = %s </h2>
        <form method="POST" enctype="multipart/form-data">
            <input type = "text" name = "confidence" placeholder = "Confidence level"><br>
            <input type = "text" name = "num_images" placeholder = "Number of images"><br>
            <input type="file" name="file"><br>
            <input type="submit" value="Submit">
        </form>
        ''' % (cnt_imgs)

    # Frontend for get face info page
    def get_face_info(self):

        # Finding the number of images present in db
        conn = DbConnection(db)
        cnt_imgs = conn.execute_select("select count(*) from images")[0]

        # Returning the html form
        return '''<!doctype html>
        <title>Get Face Info</title>
        <h1>Enter Face Id.</h1>
        <h2>Total images in database = %s </h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="text" name="face_id">
            <input type="submit" value="Submit">
        </form>
        ''' % (cnt_imgs)

# Class to handle database queries
class DbConnection:
    conn = None
    def __init__(self, db):
        self.conn = db.connect()

    # Function to execute Select queries
    def execute_select(self, query):        
        cursor = self.conn.cursor()
        cursor.execute(query)

        # Fetching the select data
        data = cursor.fetchall()
        return data

    # Function to execute update, insert, delete queries
    def execute_update(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)

        # Commiting the update
        self.conn.commit()

# Classs to store Images
class Image1:

    # This class creates image object from id, name, version and encoding
    def __init__(self, id, name, version, encoding):
        self.id = id
        self.name = name
        self.version = version
        self.encoding = encoding

class Image:

    # This class creates image object from file
    def __init__(self, file, filename):
        self.file = file
        self.filename = filename

        # Extracting details of image
        self.name = self.get_name()
        self.version = self.get_version()
        self.encoding = self.get_encoding()
    
    # Function to extract name of image
    def get_name(self):
        filename = self.filename
        name = filename.split('.')[0]
        name = name.split('_')[:-1]
        name = '_'.join(name)
        return name
    
    # Function to extrace version of the image
    def get_version(self):
        filename = self.filename
        name = filename.split('.')[0]
        version = name.split('_')[-1]
        # version = int(version, 10)
        return version
    
    # Function to get encoding of the image
    def get_encoding(self):
        file = self.file

        # Loading the image
        img = face_recognition.load_image_file(file)

        # Encoding the image using face_recognition library
        encoding = face_recognition.face_encodings(img)

        # Selecting first fase
        encoding = encoding[0]

        # Converting encoding from array to string
        encoding = [str(i) for i in encoding]
        encoding = ','.join(encoding)
        return encoding
    
    # Function to store image in database
    def insert(self):
        query = "INSERT INTO images(name, version, encoding) VALUES('%s', '%s', '%s')" % (self.name, self.version, self.encoding)

        # Creating object of Dbconnection to execute query
        conn = DbConnection(db)
        conn.execute_update(query)

# Class for Zip File
class ZipFile:
    def __init__(self, file):
        self.file = file
    
    # Function to get images of zip file
    def get_images(self):
        imgs = []
        file = self.file

        # Storing the images in temporary folder
        temp_folder = "temp_folder"

        # Extracting the images
        with zipfile.ZipFile(file) as zip_ref:
            zip_ref.extractall(temp_folder)

        # Iterating over the extracted files
        for root, dirs, files in os.walk(temp_folder):
            for filename in files:
                img_path = root + '\\' + filename

                # Creating image object from file path
                img = Image(img_path, filename)
                imgs.append(img)
        self.empty_the_folder(temp_folder)
        return imgs

    def empty_the_folder(self,folder_path):
        folder = folder_path
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

# Class to validate files
class ValidateFile:

    # This will store the extensions allowed
    allowed_extensions = {}

    def __init__(self, dic):
        self.allowed_extensions = dic

    # Function to check if file is allowed
    def allowed_file(self, filename):
        allowed = True

        # Checking if dot is present in filename or not
        if '.' not in filename:
            allowed = False
        
        # Checking the filename extension
        if filename.rsplit('.', 1)[1].lower() in self.allowed_extensions:
            allowed = False

        return allowed

    # Function to check if file is valid or not
    def is_valid(self, file):
        if file and self.allowed_file(file.filename):
            return True
        else:
            return False

# Class to handle api queries
class FacialSearch:
    def __init__(self):
        pass
    
    # Function to convert encoding from string to np array
    def de_encode(self, encoding):

        # Splitting at ','
        encoding = encoding.split(',')

        # Converting strings to float
        for i in range  (len(encoding)):
            encoding[i] = float(encoding[i])
        
        # Converting list to nparray
        return np.array(encoding)

    # Function to get image by id
    def get_image_by_id(self, id):

        # Creating db connection
        conn = DbConnection(db)
        query = "Select id, name, version, encoding from images where id = %s" % str(id)

        # Selecting required image from database
        (id, name, version, encoding) = conn.execute_select(query)[0]
        encoding = self.de_encode(encoding)

        # Returning the image object
        return Image1(id, name, version, encoding)
    
    # Function to fetch all images from database
    def get_all_images(self):

        # Creating database object
        conn = DbConnection(db)
        query = "Select id, name, version, encoding from images"
        data = conn.execute_select(query)
        res = []

        # Iterating over the result data
        for i in data:
            id,name,version,encoding = i

            # Creating image object
            img = Image1(id, name, version, encoding)
            res.append(img)
        return res
    
    # Function to perform facial match
    def match_image(self, input_file, strictness, k):

        # Getting all images from database
        all_images = self.get_all_images()

        # De encoding the encodings
        all_image_encodngs = [self.de_encode(img.encoding) for img in all_images]

        # Getting encodings for input image
        input_img = face_recognition.load_image_file(input_file)
        encodings = face_recognition.face_encodings(input_img)

        a = SortedList()
        face_cnt = 1
        matches = {}

        # Iterating over all the faces in input image
        for face in encodings:

            # Finding the distance of current face
            distance = face_recognition.face_distance(all_image_encodngs, face)

            # Checking if distance <= strictnes
            for i in range (len(distance)):
                if distance[i] <= strictness:
                    if len(a) < k:
                        a.add([distance[i], i])
                    elif a[-1][0] > distance[i]:
                        a.pop()
                        a.add([distance[i], i])
                    
            matches[f'face_{face_cnt}'] = []
            for i in range (min(len(a), k)):
                img = all_images[a[i][1]]
                matches[f'face_{face_cnt}'].append({"id": img.id, "name": img.name, "version": img.version})

        return matches



# Configuring app app
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jaglike'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['TESTING'] = True

# Setting database
db = MySQL(app)
conn = DbConnection(db)

# Function to handle add_face
@app.route('/add_face/', methods = ['GET' , 'POST'])
def add_face():

    # If it is post request
    if request.method == 'POST':
        try:
            # Performing error handling
            if 'file' not in request.files:
                return redirect(request.url)
            file = request.files['file']

            # Validating the input file
            validator = ValidateFile({'.jpg', '.png', '.jpeg'})
            if not validator.is_valid(file):
                return "Invalid Image"
            
            # Creating image object and inserting it
            image = Image(file, file.filename)
            image.insert()
            return jsonify("Image inserted")

        except:
            return jsonify("Not able to insert")
    
    else:
        # If it was GET request
        # Returning the frontend of the page
        frontend = Frontend()
        return frontend.add_face()

# Function for multi-processing pool
def fun(img):
    conn = DbConnection(db)
    conn.execute_update("INSERT INTO images(name, version, encoding) VALUES('%s', '%s', '%s')" % (img.name, img.version, img.encoding))

# Function to handle add faces in bulk
@app.route('/add_faces_in_bulk/', methods = ['GET' , 'POST'])
def add_faces_in_bulk():
    if request.method == 'POST':
        try:

            # Pefroming error handling
            if 'file' not in request.files:
                return redirect(request.url)
            file = request.files['file']

            # Checking if input file is valid
            validator = ValidateFile({'.zip'})
            if not validator.is_valid(file):
                return jsonify("Invalid File")
            
            # Creating zip file object
            zip_file = ZipFile(file)

            # Extracting images from zip file
            imgs = zip_file.get_images()

            # Using multiprocessing to efficiently insert images
            pool = multiprocessing.Pool(4)
            pool.map(fun, imgs)
            pool.close()
            return jsonify("Inserted images")

        except:
            return jsonify("Not able to insert images")

    else:
        # If it was a get request, returning the frontend of the page
        frontend = Frontend()
        return frontend.add_faces_in_bulk()

# Function to handle search_faces 
@app.route('/search_faces/', methods = ['GET' , 'POST'])
def search_faces():
    if request.method == 'POST':
        try:
            # performing error handling
            if 'file' not in request.files:
                return redirect(request.url)
        
            # Validating the input file
            file = request.files['file']
            validator = ValidateFile({'.jpg', '.png', '.jpeg'})
            if not validator.is_valid(file):
                return jsonify("Invalid Image")
            
            # Extracting confidence and num_images
            try:
                confidence = float(request.form["confidence"])
                num_images = int(request.form["num_images"])
            except:
                # If parameters were incorrect, setting default parameters
                confidence = 0.7
                num_images = 3
            
            # Performing search using facialSearch class
            fs = FacialSearch()
            res = fs.match_image(file, 1-confidence, num_images)
            return jsonify(res)

        except:
            return jsonify("Could not search face")
        
    else:
        # If it was GET request, returning the frontend of the page
        frontend = Frontend()
        return frontend.search_faces()

# Function to handle get face info page
@app.route('/get_face_info/', methods = ['GET', 'POST'])
def get_face_info():
    if request.method == 'POST':
        # Performing error handling
        if 'face_id' not in request.form:
            return redirect(request.url)

        try:        
            # Fetching face_id of imagee
            face_id = request.form["face_id"]

            # Performing facial search on image by id
            fs = FacialSearch()
            img = fs.get_image_by_id(face_id)

            # Returning the json object
            out = {"id": img.id, "name": img.name, "version": img.version}
            return jsonify(out)
        except:
            return "Could not get face info"
    else:
        # If it was get request, returning the frontend of the page
        frontend = Frontend()
        return frontend.get_face_info()



if __name__ == '__main__':
    app.run(debug=True)