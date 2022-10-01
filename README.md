# Face-Search-API

This is an python implementation of API that can be used to add images
to database, and perform facial search on these images. The API provides
functions to add single image, add images in bulk (through zip file), 
perform facial search on images and get image by id.
I have used face_recognition library to perform facial search. To improve 
the efficiency of the program, I have used multi-processing. To improve
the algorithmic complexity of the program, I have used sorted list datastructure.


## A description of how this program works (i.e. its logic)

**Assumptions:**
1. The file name must be of the form name_version_extension. The allowed extensions for
images are - jpg, jpeg, png and for bulk images are zip.

2. Input images will contain only one face, else the first face will be considered.

**API Endpoints:**

**add_face:** This endpoint will take an image as input. It will perform error handling and validate if
the file is of the correct format. If everything is fine, it will insert the file into the database.

**add_faces_in_bulk:** This endpoint will take a zip folder as input perform validations on it. If
everything is fine, it will insert all the images in zip folder to the database.

**search_faces:** This function will take an image, confidence and K as input. It will return top K
matches having confidence >= given confidence. If there are multiple faces in input, it will return
top K matches for every face.

**get_face_info:** This function will take image id as input. It will return the corresponding image
from the database. If id is incorrect, it will report it.


## How to compile and run this program

Extract the folder and navigate to the main.py file.
Run the following command to start the server:

    python main.py

Now the server will start listening to the port - 5000
Visit the port to see the API live.

For testing the API, use the following commands:

    coverage run -m test_main

To see the coverage run:

    coverage report
