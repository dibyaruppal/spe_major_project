import unittest
from flask_testing import TestCase
from flask import url_for
from app import app 
import io

class MyTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_predict_no_file_part(self):
        response = self.client.post(url_for('predict'))
        self.assert400(response)
        self.assertEqual(response.json['error'], 'No file part')

    def test_predict_no_selected_file(self):
        data = {'image': (None, '')}
        response = self.client.post(url_for('predict'), data=data)
        self.assert400(response)
        self.assertEqual(response.json['error'], 'No selected file')

    def test_predict_invalid_file_extension(self):
        data = {'image': (io.BytesIO(b"abcdef"), 'test.txt')}
        response = self.client.post(url_for('predict'), data=data)
        self.assert400(response)
        self.assertEqual(response.json['error'], 'Allowed image types are: png, jpg, jpeg')

    def test_predict_valid_image(self):
        with open('test_image.jpg', 'rb') as image_file:
            data = {'image': (image_file, 'test_image.png')}
            response = self.client.post(url_for('predict'), data=data, content_type='multipart/form-data')
            self.assert200(response)
            self.assertIn('prediction_class', response.json)
            self.assertIn('predicted_probabilities', response.json)

if __name__ == '__main__':
    unittest.main()
