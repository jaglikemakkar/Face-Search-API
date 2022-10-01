import main, pytest, unittest
from flask import Flask
from main import app

class FlaskTest(unittest.TestCase):
    def test_add_face(self):
        tester = app.test_client(self)
        file_dic = {"file": open('C:\\Academics\\6th Sem\\CS305_Software_Engineering\\Assignments\\Assignment-2\\test_images\\Aaron_Eckhart_0001.jpg', 'rb')}
        resp = tester.post("http://localhost:5000/add_face/", data = file_dic)
        assert resp.json == "Image inserted"

    def test_add_faces_in_bulk(self):
        tester = app.test_client(self)
        file_dic = {"file": open('C:\\Academics\\6th Sem\\CS305_Software_Engineering\\Assignments\\Assignment-2\\test_images.zip', 'rb')}
        resp = tester.post("http://localhost:5000/add_faces_in_bulk/", data = file_dic)
        assert resp.json == "Inserted images"
    
    def test_search_faces(self):
        tester = app.test_client(self)
        file_dic = {"file": open('C:\\Academics\\6th Sem\\CS305_Software_Engineering\\Assignments\\Assignment-2\\test_images\\Aaron_Eckhart_0001.jpg', 'rb')}
        resp = tester.post("http://localhost:5000/search_faces/", data = file_dic)
        assert resp.status_code == 200
    
    def test_search_faces(self):
        tester = app.test_client(self)
        file_dic = {"file": open('C:\\Academics\\6th Sem\\CS305_Software_Engineering\\Assignments\\Assignment-2\\test_images\\Aaron_Eckhart_0001.jpg', 'rb')}
        json_dic = {"confidence" : 0.7, "num_images": 2}
        resp = tester.post("http://localhost:5000/search_faces/", data = file_dic)
        assert resp.status_code == 200
    
    def test_get_face_info(self):
        tester = app.test_client(self)
        json_dic = {"face_id": 1}
        resp = tester.post("http://localhost:5000/get_face_info/", json = json_dic)
        assert resp.status_code == 200

    def test_frontend_1(self):
        tester = app.test_client(self)
        resp = tester.get("http://localhost:5000/add_face/")
        assert resp.status_code == 200
    
    def test_frontend_2(self):
        tester = app.test_client(self)
        resp = tester.get("http://localhost:5000/add_faces_in_bulk/")
        assert resp.status_code == 200
    
    def test_frontend_3(self):
        tester = app.test_client(self)
        resp = tester.get("http://localhost:5000/search_faces/")
        assert resp.status_code == 200

    def test_frontend_4(self):
        tester = app.test_client(self)
        resp = tester.get("http://localhost:5000/get_face_info/")
        assert resp.status_code == 200
    
    def test_add_face_error_1(self):
        tester = app.test_client(self)
        file_dic = {"file": open('C:\\Academics\\6th Sem\\CS305_Software_Engineering\\Assignments\\Assignment-2\\test_images.zip', 'rb')}
        resp = tester.post("http://localhost:5000/add_face/", data = file_dic)
        assert resp.status_code == 200
    
    def test_add_face_error_2(self):
        tester = app.test_client(self)
        file_dic = {"file": open('C:\\Academics\\6th Sem\\CS305_Software_Engineering\\Assignments\\Assignment-2\\bad_images\\bad1.jpg', 'rb')}
        resp = tester.post("http://localhost:5000/add_face/", data = file_dic)
        assert resp.status_code == 200
    
    def test_add_faces_in_bulk_error_1(self):
        tester = app.test_client(self)
        file_dic = {"file": open('C:\\Academics\\6th Sem\\CS305_Software_Engineering\\Assignments\\Assignment-2\\bad_images.zip', 'rb')}
        resp = tester.post("http://localhost:5000/add_faces_in_bulk/", data = file_dic)
        assert resp.status_code == 200
    
    def test_search_faces_error_1(self):
        tester = app.test_client(self)
        file_dic = {"file": open('C:\\Academics\\6th Sem\\CS305_Software_Engineering\\Assignments\\Assignment-2\\test_images\\Aaron_Eckhart_0001.jpg', 'rb')}
        json_dic = {"confidence" : 0.7, "num_images": 2}
        resp = tester.post("http://localhost:5000/search_faces/")    

    def test_get_face_info_error_1(self):
        tester = app.test_client(self)
        json_dic = {"face_id": -1}
        resp = tester.post("http://localhost:5000/get_face_info/", json = json_dic)
        assert resp.status_code == 200


if __name__ == "__main__":
    unittest.main()


# class FlaskTest(unittest.TestCase):
        
#     def test_index(self):
#         tester = app.test_client(self)
#         response = tester.post( '/add_face', json = {'image_path':'.\\Abdel_Nasser_Assidi_0002.jpg' })
#         statuscode = response.status_code
#         print(response.json)
#         self.assertAlmostEquals(statuscode , 200)

#     def test_add_faces_in_bulk(self):
#         tester = app.test_client(self)
#         response = tester.post( '/add_faces_in_bulk', json = {'zip_path':'.\\sample_zip.zip' })
#         statuscode = response.status_code
#         print(response.json)
#         self.assertAlmostEquals(statuscode , 200)
    
#     def test_search_faces(self):
#         tester = app.test_client(self)
#         response = tester.post( '/search_faces', json = {'input_image':'.\\Abdel_Nasser_Assidi_0002.jpg' })
#         statuscode = response.status_code
#         print(response.json)
#         self.assertAlmostEquals(statuscode , 200)
    
#     def test_get_image_info(self):
#         tester = app.test_client(self)
#         response = tester.post( '/get_face_info', json = {'api_key':3, 'face_id': 3})
#         statuscode = response.status_code
#         print(response.json)
#         self.assertAlmostEquals(statuscode , 200)
        

# if _name_ == "_main_":
#     unittest.main()