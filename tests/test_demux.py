from unittest import TestCase

from demux import get_ss_arg_for_file
from demux import get_title_for_file

import os


class test_demux(TestCase):
    def test_get_ss_arg_for_file_nonexisting(self):
        self.assertEqual(get_ss_arg_for_file('qwe'), None)

    def test_get_ss_arg_for_file_existing(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'files', '2016-10-07 goswamimj.mp4')
        self.assertEqual(get_ss_arg_for_file(filename), '1:15')

    def test_get_title_for_file(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'files', '2016-10-07 goswamimj.mp4')
        self.assertEqual('2016-10-07', get_title_for_file(filename))
