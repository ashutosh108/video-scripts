from unittest import TestCase

import meta

import os


class test_meta(TestCase):
    def test_get_ss_arg_for_file_nonexisting(self):
        self.assertEqual(meta._get_skip_time('qwe'), None)

    def test_get_ss_arg_for_file_existing(self):
        filename = self.get_test_filename('2016-10-07 goswamimj.mp4')
        self.assertEqual(meta._get_skip_time(filename), '1:15')

    # pyyaml somehow automatically leaves 0:07 as '0:07', but converts 1:07 to int 67 (seconds).
    # We have to deal with either.
    def test_get_ss_args_for_zero_minutes(self):
        filename = self.get_test_filename('2016-10-17 avadhutmj.mp4')
        self.assertEqual(meta._get_skip_time(filename), '0:07')

    def test_get_artist_eng(self):
        filename = self.get_test_filename('2016-10-07 goswamimj.mp4')
        self.assertEqual('Bhakti Sudhir Goswami', meta._get_artist_eng(filename))

    def test_get_artist_eng_multiple(self):
        filename = self.get_test_filename('2016-10-07 janardanmj_goswamimj.mp4')
        self.assertEqual('Bhakti Pavan Janardan, Bhakti Sudhir Goswami', meta._get_artist_eng(filename))

    def test_get_artist_eng_ranjan(self):
        filename = self.get_test_filename('2016-10-07 brmadhusudan.mp4')
        self.assertEqual('Bhakti Rañjan Madhusudan', meta._get_artist_eng(filename))

    def test_get_year_month_day(self):
        filename = self.get_test_filename('2016-10-07 brmadhusudan.mp4')
        [year, month, day] = meta._get_year_month_day(filename)
        self.assertEqual('2016', year)
        self.assertEqual('10', month)
        self.assertEqual('07', day)

    def test_get_title_eng(self):
        filename = self.get_test_filename('2016-10-07 goswamimj.mp4')
        title_eng = meta._get_title_eng(filename)
        self.assertEqual('Have faith in Guru-Vaishnava, not in yourself', title_eng)

    def test_get_skip_time(self):
        filename = self.get_test_filename('2016-10-07 goswamimj.mp4')
        skip_time = meta._get_skip_time(filename)
        self.assertEqual('1:15', skip_time)

    def test_get_skip_time_from_yml(self):
        filename = self.get_test_filename('2016-10-12 brmadhusudan.mp4')
        skip_time = meta._get_skip_time(filename)
        self.assertEqual('0:07:56', skip_time)

    def test_get_youtube_description_eng(self):
        filename = self.get_test_filename('2016-10-12 brmadhusudan.mp4')
        expected = """- The story of Chiangmai ashram
- Good fortune of those who have facilities for practicing devotional life
- How Srila Govinda Maharaj appreciated Thai culture
- The original purpose of the building of Chiangmai ashram: sanskrit school

Srila Bhakti Rañjan Madhusudan Maharaj
October 12, 2016
Theistic Media Studios, Gupta Govardhan Ashram.
Downloaded from TMS_TV livestream.com/accounts/2645002

На русском: (ссылка скоро будет)"""
        self.assertEqual(expected, meta.get_youtube_description_eng(filename))

    def test_get_youtube_title_rus_stereo(self):
        filename = self.get_test_filename('2016-10-12 brmadhusudan.mp4')
        expected = 'Удача Чиангмайского ашрама. Бхакти Ранджан Мадхусудан'
        self.assertEqual(expected, meta.get_youtube_title_rus_stereo(filename))

    def test_get_youtube_title_rus_mono(self):
        filename = self.get_test_filename('2016-10-12 brmadhusudan.mp4')
        expected = 'Удача Чиангмайского ашрама (моно). Бхакти Ранджан Мадхусудан'
        self.assertEqual(expected, meta.get_youtube_title_rus_mono(filename))

    def test_get_youtube_title_rus_mono_dot(self):
        filename = self.get_test_filename('2016-01-01 goswamimj.mp4')
        expected = 'Проверка точки (моно). Бхакти Судхир Госвами'
        self.assertEqual(expected, meta.get_youtube_title_rus_mono(filename))

    def test_get_youtube_title_rus_stereo_question_mark(self):
        filename = self.get_test_filename('2016-10-05 goswamimj.mp4')
        expected = 'Настроение или сердце? Бхакти Судхир Госвами'
        self.assertEqual(expected, meta.get_youtube_title_rus_stereo(filename))

    def test_get_youtube_title_rus_mono_question_mark(self):
        filename = self.get_test_filename('2016-10-05 goswamimj.mp4')
        expected = 'Настроение или сердце? (моно) Бхакти Судхир Госвами'
        self.assertEqual(expected, meta.get_youtube_title_rus_mono(filename))

    def test_get_youtube_descr_rus_stereo(self):
        filename = self.get_test_filename('2016-10-12 brmadhusudan.mp4')
        expected = """- История Чиангмайсколго ашрама
- Удача тех, кто имеет возможность практиковать преданное служение
- Как Шрила Говинда Махарадж ценил Тайскую культуру
- Здание Чиангмайского ашрама строилось для санскритской школы

Шрила Бхакти Ранджан Мадхусудан Махарадж
12 октября 2016
Студия "Теистик Медиа", Ашрам на Гупта Говардхане.
Загружено с TMS_TV livestream.com/accounts/2645002

English original: (link pending)
Моно перевод: (link pending)"""
        self.assertEqual(expected, meta.get_youtube_description_rus_stereo(filename))

    def test_get_youtube_descr_rus_mono(self):
        filename = self.get_test_filename('2016-10-12 brmadhusudan.mp4')
        expected = """- История Чиангмайсколго ашрама
- Удача тех, кто имеет возможность практиковать преданное служение
- Как Шрила Говинда Махарадж ценил Тайскую культуру
- Здание Чиангмайского ашрама строилось для санскритской школы

Шрила Бхакти Ранджан Мадхусудан Махарадж
12 октября 2016
Студия "Теистик Медиа", Ашрам на Гупта Говардхане.
Загружено с TMS_TV livestream.com/accounts/2645002

English original: (link pending)
Стерео перевод: (link pending)"""
        self.assertEqual(expected, meta.get_youtube_description_rus_mono(filename))

    @staticmethod
    def get_test_filename(base_filename):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'files', base_filename)
        return filename
