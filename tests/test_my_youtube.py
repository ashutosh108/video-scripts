from unittest import TestCase

import my_youtube


class Test_my_youtube(TestCase):
    def test_compose_upload_body(self):
        body = my_youtube._compose_upload_body(filename='2016-07-05.mp4', title='qwe', lang='en', description='desc')
        self.assertEqual('qwe', body['snippet']['title'])
        self.assertEqual('desc', body['snippet']['description'])
        self.assertEqual('en', body['snippet']['defaultLanguage'])
        self.assertTrue(body['recordingDetails']['recordingDate'].startswith('2016-07-05'))

    def test_compose_upload_body_empty(self):
        body = my_youtube._compose_upload_body(filename='q')
        self.assertEqual('q', body['snippet']['title'])
        self.assertNotIn('description', body['snippet'])
        self.assertNotIn('recordingDetails', body)

    def test_compose_upload_body_ru_lang_from_filename(self):
        body = my_youtube._compose_upload_body(filename='2016-07-05 goswamimj ru.mp4')
        self.assertEqual('ru', body['snippet']['defaultLanguage'])
