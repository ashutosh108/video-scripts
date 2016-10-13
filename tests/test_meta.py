from unittest import TestCase

import meta

import os


class test_meta(TestCase):
    def test_get_ss_arg_for_file_nonexisting(self):
        self.assertEqual(meta.get_skip_time('qwe'), None)

    def test_get_ss_arg_for_file_existing(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'files', '2016-10-07 goswamimj.mp4')
        self.assertEqual(meta.get_skip_time(filename), '1:15')

    def test_get_title_for_file(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'files', '2016-10-07 goswamimj.mp4')
        self.assertEqual('2016-10-07', meta.get_title_for_file(filename))


    def test_get_artist_eng(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'files', '2016-10-07 goswamimj.mp4')
        self.assertEqual('Bhakti Sudhir Goswami', meta.get_artist_eng(filename))

    def test_get_artist_eng_multiple(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'files', '2016-10-07 janardanmj_goswamimj.mp4')
        self.assertEqual('Bhakti Pavan Janardan, Bhakti Sudhir Goswami', meta.get_artist_eng(filename))

    def test_get_artist_eng_ranjan(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'files', '2016-10-07 brmadhusudan.mp4')
        self.assertEqual('Bhakti Rañjan Madhusudan', meta.get_artist_eng(filename))

    def test_get_year_month_day(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'files', '2016-10-07 brmadhusudan.mp4')
        [year, month, day] = meta.get_year_month_day(filename)
        self.assertEqual('2016', year)
        self.assertEqual('10', month)
        self.assertEqual('07', day)

    def test_get_title_eng(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'files', '2016-10-07 goswamimj.mp4')
        title_eng = meta.get_title_eng(filename)
        self.assertEqual('Have faith in Guru-Vaishnava, not in yourself', title_eng)

    def test_get_skip_time(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'files', '2016-10-07 goswamimj.mp4')
        skip_time = meta.get_skip_time(filename)
        self.assertEqual('1:15', skip_time)


    def test_get_skip_time_from_yml(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'files', '2016-10-12 brmadhusudan.mp4')
        skip_time = meta.get_skip_time(filename)
        self.assertEqual('0:07:56', skip_time)
