import os, shutil, pickle
from flask import Flask, jsonify, request, redirect
from flaskext.mysql import MySQL
import face_recognition
from threading import Thread
import multiprocessing

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jaglike'
app.config['MYSQL_DATABASE_DB'] = 'se_2'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
db = MySQL(app)

# Start = 1369
def fun(file):
    try:
        path = "C:\\Academics\\6th Sem\\CS305_Software_Engineering\\Assignments\\Assignment-2\\images\\" + file
        version = int(file.split('.')[0].split('_')[-1], 10)
        name = file.split('.')[0].split('_')[:-1]
        name = '_'.join(name)
        img = face_recognition.load_image_file(path)
        # Get face encodings for any faces in the uploaded image
        encoding = face_recognition.face_encodings(img)[0]
        encoding = [str(i) for i in encoding]
        encoding = ','.join(encoding)

        connect = db.connect()
        cursor = connect.cursor()
        query = "INSERT INTO images(name, version, encoding) VALUES('%s', '%s', '%s')" % (name, version, encoding)
        cursor.execute(query)
        connect.commit()
        cursor.close()
    except:
        print("Failed to insert image: ", file)
if __name__ == "__main__":
    cnt = 0
    threads = []
    pool = multiprocessing.Pool(4)
    all_files = []
    for root, dirs, files in os.walk('images'):
        for file in files:
            # shutil.copyfile(original, target)
            all_files.append(file)
            cnt+=1
    pool.map(fun, all_files)
    # print("Done: ", cnt)