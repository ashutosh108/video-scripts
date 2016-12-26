from unittest import TestCase

import meta

import os


class test_meta(TestCase):
    def test_get_skip_time_for_file_nonexisting(self):
        self.assertEqual(meta.get_skip_time('qwe'), None)

    def test_get_skip_time_for_file_existing(self):
        filename = self.get_test_filename('2016-10-07 goswamimj.mp4')
        self.assertEqual(meta.get_skip_time(filename), '1:15')

    # pyyaml somehow automatically leaves 0:07 as '0:07', but converts 1:07 to int 67 (seconds).
    # We have to deal with either.
    def test_get_skip_time_for_zero_minutes(self):
        filename = self.get_test_filename('2016-10-17 avadhutmj.mp4')
        self.assertEqual(meta.get_skip_time(filename), '0:07')

    def test_get_artist_en(self):
        filename = self.get_test_filename('2016-10-07 goswamimj.mp4')
        self.assertEqual('Bhakti Sudhīr Goswāmī', meta.get_artist_en(filename))

    def test_get_artist_en_multiple(self):
        filename = self.get_test_filename('2016-10-07 janardanmj_goswamimj.mp4')
        self.assertEqual('Bhakti Pāvan Janārdan, Bhakti Sudhīr Goswāmī', meta.get_artist_en(filename))

    def test_get_artist_en_ranjan(self):
        filename = self.get_test_filename('2016-10-07 brmadhusudan.mp4')
        self.assertEqual('Bhakti Rañjan Madhusūdan', meta.get_artist_en(filename))

    def test_get_year_month_day(self):
        filename = self.get_test_filename('2016-10-07 brmadhusudan.mp4')
        [year, month, day] = meta.get_year_month_day(filename)
        self.assertEqual('2016', year)
        self.assertEqual('10', month)
        self.assertEqual('07', day)

    def test_get_title_en(self):
        filename = self.get_test_filename('2016-10-07 goswamimj.mp4')
        title_en = meta.get_title_en(filename)
        self.assertEqual('Have faith in Guru-Vaishnava, not in yourself', title_en)

    def test_get_skip_time(self):
        filename = self.get_test_filename('2016-10-07 goswamimj.mp4')
        skip_time = meta.get_skip_time(filename)
        self.assertEqual('1:15', skip_time)

    def test_get_skip_time_from_yml(self):
        filename = self.get_test_filename('2016-10-12 brmadhusudan.mp4')
        skip_time = meta.get_skip_time(filename)
        self.assertEqual('0:07:56', skip_time)

    def test_get_youtube_description_en(self):
        filename = self.get_test_filename('2016-10-12 brmadhusudan.mp4')
        expected = """- The story of Chiangmai ashram
- Good fortune of those who have facilities for practicing devotional life
- How Srila Govinda Maharaj appreciated Thai culture
- The original purpose of the building of Chiangmai ashram: sanskrit school

Śrīla Bhakti Rañjan Madhusūdan Mahārāj
October 12, 2016
Theistic Media Studios, Gupta Govardhan Ashram.
Downloaded from TMS_TV livestream.com/accounts/2645002

На русском: (ссылка скоро будет)"""
        self.assertEqual(expected, meta.get_youtube_description_orig(filename, 'en'))

    def test_get_youtube_title_ru_stereo(self):
        filename = self.get_test_filename('2016-10-12 brmadhusudan.mp4')
        expected = 'Удача Чиангмайского ашрама. Бхакти Ран̃джан Мадхусӯдан'
        self.assertEqual(expected, meta.get_youtube_title_ru_stereo(filename))

    def test_get_youtube_title_ru_mono(self):
        filename = self.get_test_filename('2016-10-12 brmadhusudan.mp4')
        expected = 'Удача Чиангмайского ашрама (моно). Бхакти Ран̃джан Мадхусӯдан'
        self.assertEqual(expected, meta.get_youtube_title_ru_mono(filename))

    def test_get_youtube_title_ru_mono_dot(self):
        filename = self.get_test_filename('2016-01-01 goswamimj.mp4')
        expected = 'Проверка точки (моно). Бхакти Судхӣр Госва̄мӣ'
        self.assertEqual(expected, meta.get_youtube_title_ru_mono(filename))

    def test_get_youtube_title_ru_stereo_question_mark(self):
        filename = self.get_test_filename('2016-10-05 goswamimj.mp4')
        expected = 'Настроение или сердце? Бхакти Судхӣр Госва̄мӣ'
        self.assertEqual(expected, meta.get_youtube_title_ru_stereo(filename))

    def test_get_youtube_title_ru_mono_question_mark(self):
        filename = self.get_test_filename('2016-10-05 goswamimj.mp4')
        expected = 'Настроение или сердце? (моно) Бхакти Судхӣр Госва̄мӣ'
        self.assertEqual(expected, meta.get_youtube_title_ru_mono(filename))

    def test_get_youtube_descr_ru_stereo(self):
        filename = self.get_test_filename('2016-10-12 brmadhusudan.mp4')
        expected = """- История Чиангмайсколго ашрама
- Удача тех, кто имеет возможность практиковать преданное служение
- Как Шрила Говинда Махарадж ценил Тайскую культуру
- Здание Чиангмайского ашрама строилось для санскритской школы

Ш́рӣла Бхакти Ран̃джан Мадхусӯдан Mаха̄ра̄дж
12 октября 2016
Студия "Теистик Медиа", Ашрам на Гупта Говардхане.
Загружено с TMS_TV livestream.com/accounts/2645002

English original: (link pending)
Моно перевод: (link pending)"""
        self.assertEqual(expected, meta.get_youtube_description_ru_stereo(filename))

    def test_get_youtube_descr_ru_mono(self):
        filename = self.get_test_filename('2016-10-12 brmadhusudan.mp4')
        expected = """- История Чиангмайсколго ашрама
- Удача тех, кто имеет возможность практиковать преданное служение
- Как Шрила Говинда Махарадж ценил Тайскую культуру
- Здание Чиангмайского ашрама строилось для санскритской школы

Ш́рӣла Бхакти Ран̃джан Мадхусӯдан Mаха̄ра̄дж
12 октября 2016
Студия "Теистик Медиа", Ашрам на Гупта Говардхане.
Загружено с TMS_TV livestream.com/accounts/2645002

English original: (link pending)
Стерео перевод: (link pending)"""
        self.assertEqual(expected, meta.get_youtube_description_ru_mono(filename))

    @staticmethod
    def get_test_filename(base_filename):
        directory = os.path.dirname(__file__)
        filename = os.path.join(directory, 'files', base_filename)
        return filename

    def test_get_lang(self):
        filename = self.get_test_filename('2016-10-17 avadhutmj.mp4')
        expected = 'ru'
        self.assertEqual(expected, meta.get_lang(filename))

    def test_get_lang_en_default(self):
        filename = self.get_test_filename('2016-10-12 brmadhusudan.mp4')
        expected = 'en'
        self.assertEqual(expected, meta.get_lang(filename))

    def test_get(self):
        filename = self.get_test_filename('2016-10-17 avadhutmj.mp4')
        self.assertEqual('ru', meta.get(filename, 'lang'))

    def test_youtube_links_from_orig(self):
        filename = self.get_test_filename('2016-01-02 goswamimj.mp4')
        expected = """
Śrīla Bhakti Sudhīr Goswāmī Mahārāj
January 2, 2016
Theistic Media Studios, Gupta Govardhan Ashram.
Downloaded from TMS_TV livestream.com/accounts/2645002\n
На русском: https://youtu.be/sssssssssss"""
        self.assertEqual(expected, meta.get_youtube_description_orig(filename, 'en'))

    def test_youtube_links_from_mono(self):
        filename = self.get_test_filename('2016-01-02 goswamimj.mp4')
        expected = """
Ш́рӣла Бхакти Судхӣр Госва̄мӣ Mаха̄ра̄дж
02 января 2016
Студия "Теистик Медиа", Ашрам на Гупта Говардхане.
Загружено с TMS_TV livestream.com/accounts/2645002

English original: https://youtu.be/ooooooooooo
Стерео перевод: https://youtu.be/sssssssssss"""
        self.assertEqual(expected, meta.get_youtube_description_ru_mono(filename))

    def test_youtube_links_from_stereo(self):
        filename = self.get_test_filename('2016-01-02 goswamimj.mp4')
        expected = """
Ш́рӣла Бхакти Судхӣр Госва̄мӣ Mаха̄ра̄дж
02 января 2016
Студия "Теистик Медиа", Ашрам на Гупта Говардхане.
Загружено с TMS_TV livestream.com/accounts/2645002

English original: https://youtu.be/ooooooooooo
Моно перевод: https://youtu.be/mmmmmmmmmmm"""
        self.assertEqual(expected, meta.get_youtube_description_ru_stereo(filename))
