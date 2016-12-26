from unittest import TestCase

import ffmpeg

import os


class test_ffmpeg(TestCase):
    def test_get_ss_arg_for_file_nonexisting(self):
        self.assertEqual(ffmpeg.ss_args('qwe'), [])

    def test_get_ss_arg_for_file_existing(self):
        filename = self.get_test_filename('2016-10-07 goswamimj.mp4')
        self.assertEqual(ffmpeg.ss_args(filename), ['-ss', '1:15'])

    # pyyaml somehow automatically leaves 0:07 as '0:07', but converts 1:07 to int 67 (seconds).
    # We have to deal with either.
    def test_get_ss_args_for_zero_minutes(self):
        filename = self.get_test_filename('2016-10-17 avadhutmj.mp4')
        self.assertEqual(ffmpeg.ss_args(filename), ['-ss', '0:07'])

    def test_get_to_args_for_file_nonexisting(self):
        self.assertEqual(ffmpeg.to_args('qwe'), [])

    def test_get_to_args_for_file_existing(self):
        filename = self.get_test_filename('2016-10-17 avadhutmj.mp4')
        self.assertEqual(ffmpeg.to_args(filename), ['-to', '1:02:03'])

    @staticmethod
    def get_test_filename(base_filename):
        directory = os.path.dirname(__file__)
        filename = os.path.join(directory, 'files', base_filename)
        return filename
