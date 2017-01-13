import datetime
import numbers
import os
import re
import string
from typing import Optional

import babel.dates
import yaml

import yamlupdater

_yaml_data_cache = {}


def _yaml_data(filename) -> dict:
    global _yaml_data_cache
    if filename not in _yaml_data_cache:
        try:
            yaml_filename = os.path.splitext(filename)[0] + '.yml'
            with open(yaml_filename, 'r', encoding='UTF-8') as f:
                _yaml_data_cache[filename] = yaml.load(f)
        except (IndexError, FileNotFoundError):
            _yaml_data_cache[filename] = dict()
    return _yaml_data_cache[filename]


def get_skip_time(filename: str) -> str:
    """
    get proper argument for -ss min:sec part of the ffmpeg command line
    e.g. '2:51' if that's what's written in filename_offset.txt
    or None if that _offset file is not found
    :param filename:
    :return: string or None
    """
    name_wo_ext = os.path.splitext(filename)[0]
    for offset_filename in ['%s_offset.txt' % name_wo_ext, '%s offset.txt' % name_wo_ext]:
        try:
            with open(offset_filename) as f:
                return f.readline().rstrip()
        except FileNotFoundError:
            pass
    return _yaml_get_time_length(filename, 'skip')


def _yaml_get_time_length(filename: str, key: str) -> Optional[str]:
    """
    get proper argument for -tt min:sec part of the ffmpeg command line
    :param filename:
    :return: string or None
    """
    y = _yaml_data(filename)
    try:
        skip = y[key]
        if isinstance(skip, numbers.Number):
            skip = str(datetime.timedelta(seconds=skip))
        return skip
    except KeyError:
        return None


def get_cut_time(filename):
    return _yaml_get_time_length(filename, 'cut')


def get(filename: str, key: str, default=None):
    return _yaml_data(filename).get(key, default)


def get_lang(filename):
    return get(filename, 'lang', 'en')


def get_title_en(filename):
    y = _yaml_data(filename)
    try:
        return y['title_en']
    except KeyError:
        try:
            return y['title_eng']
        except KeyError:
            return os.path.basename(os.path.splitext(filename)[0])


def get_title_ru(filename):
    y = _yaml_data(filename)
    try:
        return y['title_ru']
    except KeyError:
        try:
            return y['title_rus']
        except KeyError:
            return os.path.basename(os.path.splitext(filename)[0])


_known_artists_en = dict(
    goswamimj=['Bhakti Sudhīr Goswāmī', 'Śrīla Bhakti Sudhīr Goswāmī Mahārāj', 'B.S.Goswāmī'],
    bsgoswami=['Bhakti Sudhīr Goswāmī', 'Śrīla Bhakti Sudhīr Goswāmī Mahārāj', 'B.S.Goswāmī'],
    janardanmj=['Bhakti Pāvan Janārdan', 'Śrīla Bhakti Pāvan Janārdan Mahārāj', 'B.P.Janārdan'],
    bpjanardan=['Bhakti Pāvan Janārdan', 'Śrīla Bhakti Pāvan Janārdan Mahārāj', 'B.P.Janārdan'],
    avadhutmj=['Bhakti Bimal Avadhūt', 'Śrīla Bhakti Bimal Avadhūt Mahārāj', 'B.B.Avadhūt'],
    bbavadhut=['Bhakti Bimal Avadhūt', 'Śrīla Bhakti Bimal Avadhūt Mahārāj', 'B.B.Avadhūt'],
    madhusudanmj=['Bhakti Rañjan Madhusūdan', 'Śrīla Bhakti Rañjan Madhusūdan Mahārāj', 'B.R.Madhusūdan'],
    brmadhusudan=['Bhakti Rañjan Madhusūdan', 'Śrīla Bhakti Rañjan Madhusūdan Mahārāj', 'B.R.Madhusūdan'],
    hasyapriya=['Hāsyapriya Prabhu', 'Hāsyapriya Prabhu', 'Hāsyapriya Pr.'],
    taritkrishna=['Tārit Kṛṣṇa Prabhu', 'Tārit Kṛṣṇa Prabhu', 'Tārit Kṛṣṇa Pr.']
)


def _artist_real_name_en(artist_code):
    if artist_code in _known_artists_en:
        return _known_artists_en[artist_code][0]
    return artist_code


def _artist_full_name_en(artist_code):
    if artist_code in _known_artists_en:
        return _known_artists_en[artist_code][1]
    return artist_code


def _artist_short_name_en(artist_code):
    if artist_code in _known_artists_en:
        return _known_artists_en[artist_code][2]
    return artist_code


_known_artists_ru = dict(
    goswamimj=['Бхакти Судхӣр Госва̄мӣ', 'Ш́рӣла Бхакти Судхӣр Госва̄мӣ Mаха̄ра̄дж', 'Б.С.Госва̄мӣ'],
    bsgoswami=['Бхакти Судхӣр Госва̄мӣ', 'Ш́рӣла Бхакти Судхӣр Госва̄мӣ Mаха̄ра̄дж', 'Б.С.Госва̄мӣ'],
    janardanmj=['Бхакти Па̄ван Джана̄рдан', 'Ш́рӣла Бхакти Па̄ван Джана̄рдан Mаха̄ра̄дж', 'Б.П.Джана̄рдан'],
    bpjanardan=['Бхакти Па̄ван Джана̄рдан', 'Ш́рӣла Бхакти Па̄ван Джана̄рдан Mаха̄ра̄дж', 'Б.П.Джана̄рдан'],
    avadhutmj=['Бхакти Бимал Авадхӯт', 'Ш́рӣла Бхакти Бимал Авадхӯт Mаха̄ра̄дж', 'Б.Б.Авадхӯт'],
    bbavadhut=['Бхакти Бимал Авадхӯт', 'Ш́рӣла Бхакти Бимал Авадхӯт Mаха̄ра̄дж', 'Б.Б.Авадхӯт'],
    madhusudanmj=['Бхакти Ран̃джан Мадхусӯдан', 'Ш́рӣла Бхакти Ран̃джан Мадхусӯдан Mаха̄ра̄дж', 'Б.Р.Мадхусӯдан'],
    brmadhusudan=['Бхакти Ран̃джан Мадхусӯдан', 'Ш́рӣла Бхакти Ран̃джан Мадхусӯдан Mаха̄ра̄дж', 'Б.Р.Мадхусӯдан'],
    hasyapriya=['Ха̄сьяприя Прабху', 'Ха̄сьяприя Прабху', 'Ха̄сьяприя Пр.'],
    taritkrishna=['Та̄рит Кр̣ш̣н̣а Прабху', 'Та̄рит Кр̣ш̣н̣а Прабху', 'Та̄рит Кр̣ш̣н̣а Пр.'],
    unknown=['Автор неизвестен', 'Автор неизвестен', 'Автор неизвестен']
)


def _artist_real_name_ru(artist):
    if artist in _known_artists_ru:
        return _known_artists_ru[artist][0]
    return artist


def _artist_full_name_ru(artist_code):
    if artist_code in _known_artists_ru:
        return _known_artists_ru[artist_code][1]
    return artist_code


def _artist_short_name_ru(artist):
    if artist in _known_artists_ru:
        return _known_artists_ru[artist][2]
    return artist


def _get_artists_codes(filename):
    basename = os.path.basename(filename)
    match = re.match('^(\d\d\d\d)-?(\d\d)-?(\d\d)\s+(.*)\.', basename)
    if match is not None:
        artists_str = match.group(4)
        artists = []
        for artist in re.split('[_-]', artists_str):
            artists.append(artist)
        return artists
    else:
        return ['unknown']


def get_artist_en(filename):
    codes = _get_artists_codes(filename)
    names = map(lambda code: _artist_real_name_en(code), codes)
    return ', '.join(names)


def _get_artist_short_en(filename):
    codes = _get_artists_codes(filename)
    names = map(lambda code: _artist_short_name_en(code), codes)
    return ', '.join(names)


def get_artist_ru(filename):
    codes = _get_artists_codes(filename)
    names = map(lambda code: _artist_real_name_ru(code), codes)
    return ', '.join(names)


def _get_artist_short_ru(filename):
    codes = _get_artists_codes(filename)
    names = map(lambda code: _artist_short_name_ru(code), codes)
    return ', '.join(names)


def get_year_month_day(filename):
    basename = os.path.basename(filename)
    match = re.match('^(\d\d\d\d)-?(\d\d)-?(\d\d)', basename)
    if match:
        return match.groups()
    return [None, None, None]


def get_work_filename(filename, add):
    dir_name = os.path.dirname(filename)
    basename = os.path.basename(filename)
    basename_wo_ext = os.path.splitext(basename)[0]
    return os.path.join(dir_name, 'temp', basename_wo_ext + add)


def get_youtube_title(filename, lang):
    if lang == 'ru':
        return get_youtube_title_ru_stereo(filename)
    else:
        return get_youtube_title_en(filename)


def get_youtube_title_en(filename):
    title = get_title_en(filename)
    if title[-1] not in string.punctuation:
        title += '.'
    artist = get_artist_en(filename)
    new_title = title + ' ' + artist
    if len(new_title) > 100:
        artist_short = _get_artist_short_en(filename)
        new_title = title + ' ' + artist_short
    return new_title[:100]


def get_youtube_title_ru_stereo(filename):
    title = get_title_ru(filename)
    if title[-1] not in string.punctuation:
        title += '.'
    artist = get_artist_ru(filename)
    new_title = title + ' ' + artist
    if len(new_title) > 100:
        artist_short = _get_artist_short_ru(filename)
        new_title = title + ' ' + artist_short
    return new_title[:100]


def get_youtube_title_ru_mono(filename):
    title = get_title_ru(filename)
    title_without_dot = title
    dot = '.'
    if title[-1] in string.punctuation and title[-1] != '.':
        dot = ''
    if title[-1] == '.':
        title_without_dot = title_without_dot[:-1]
    artist = get_artist_ru(filename)
    new_title = title_without_dot + ' (моно)' + dot + ' ' + artist
    if len(new_title) > 100:
        artist_short = _get_artist_short_ru(filename)
        new_title = title_without_dot + ' (моно)' + dot + ' ' + artist_short
    return new_title[:100]


def get_description_en(filename):
    try:
        return _yaml_data(filename)['descr_en']
    except KeyError:
        try:
            return _yaml_data(filename)['descr_eng']
        except KeyError:
            return ''


def get_description_ru(filename):
    try:
        return _yaml_data(filename)['descr_ru']
    except KeyError:
        try:
            return _yaml_data(filename)['descr_rus']
        except KeyError:
            return ''


def _get_author_with_title_en(filename):
    authors_codes = _get_artists_codes(filename)
    authors_full_names = map(_artist_full_name_en, authors_codes)
    return ', '.join(authors_full_names)


def get_youtube_description_orig(filename, lang):
    if lang == 'ru':
        return _get_youtube_description_ru(filename)
    else:
        return _get_youtube_description_en(filename)


def _youtube_playlists_en():
    return """More Goswāmī Mahārāj: 2016 — https://www.youtube.com/playlist?list=PL6tEPx3Dy5-UTBh4hYonpv3HIeoRI8Hii
2017 — https://www.youtube.com/playlist?list=PL6tEPx3Dy5-WwqFLQIhM3Hu7cBh60Y2VZ
More Madhusūdan Mahārāj: https://www.youtube.com/playlist?list=PL6tEPx3Dy5-X13nA4LgtKgujEvCI_77NY
More Avadhūt Mahārāj: 2016 — https://www.youtube.com/playlist?list=PL6tEPx3Dy5-XnC79_zqlekdFl0nFNpvjJ
2017 — https://www.youtube.com/playlist?list=PL6tEPx3Dy5-XZkgmpnWfenoggfZOVOaPS"""


def _youtube_playlists_ru():
    return """Ещё Госва̄мӣ Mаха̄ра̄джа: 2016 — https://www.youtube.com/playlist?list=PL6tEPx3Dy5-Ugkm4jTb3VGdVChoCm3J8X
2017 — https://www.youtube.com/playlist?list=PL6tEPx3Dy5-X8O8R9jP-TDJPbmgN0kIOD
Ещё Мадхусӯдана Mаха̄ра̄джа: https://www.youtube.com/playlist?list=PL6tEPx3Dy5-VzEoAeaEliOm-iQUGmY-lz
Ещё Авадхӯта Mаха̄ра̄джа: 2016 — https://www.youtube.com/playlist?list=PL6tEPx3Dy5-X3u6WgQtMTjhfErxKk1tkK
2017 — https://www.youtube.com/playlist?list=PL6tEPx3Dy5-VheQwXw_fFnDft_AX4JqYo"""


def _get_youtube_description_en(filename):
    year, month, day = get_year_month_day(filename)
    dt_obj = datetime.date(int(year), int(month), int(day))
    author_with_title = _get_author_with_title_en(filename)
    date = '{dt:%B} {dt.day}, {dt:%Y}'.format(dt=dt_obj)
    yt_descr = get_description_en(filename) + '\n'
    yt_descr += author_with_title + '\n'  # e.g. Srila Bhakti Rañjan Madhusudan Maharaj
    yt_descr += date + '\n'  # e.g. October 11, 2016
    yt_descr += 'Theistic Media Studios, Gupta Govardhan Āśram.\n'
    yt_descr += 'Downloaded from TMS_TV livestream.com/accounts/2645002\n\n'
    yt_descr += 'На русском: ' + _get_youtube_link(filename, 'rus_stereo', '(ссылка скоро будет)')
    return yt_descr + '\n\n' + _youtube_playlists_en()


def _get_author_with_title_ru(filename):
    authors_codes = _get_artists_codes(filename)
    authors_full_names = map(_artist_full_name_ru, authors_codes)
    return ', '.join(authors_full_names)


def _get_youtube_description_ru(filename):
    year, month, day = get_year_month_day(filename)
    dt_obj = datetime.date(int(year), int(month), int(day))
    author_with_title = _get_author_with_title_ru(filename)
    date = babel.dates.format_datetime(dt_obj, 'dd MMMM YYYY', locale='ru_RU')
    yt_descr = get_description_ru(filename) + '\n'
    yt_descr += author_with_title + '\n'  # e.g. Srila Bhakti Rañjan Madhusudan Maharaj
    yt_descr += date + '\n'  # e.g. October 11, 2016
    yt_descr += 'Студия «Теистик Медиа», А̄ш́рам на Гупта Говардхане.\n'
    yt_descr += 'Загружено с TMS_TV livestream.com/accounts/2645002'
    return yt_descr + '\n\n' + _youtube_playlists_ru()


def _get_youtube_link(filename, key, default='(link pending)'):
    youtube_id = get(filename, 'youtube_id_'+key)
    if youtube_id:
        return 'https://youtu.be/' + youtube_id
    else:
        return default


def get_youtube_description_ru_stereo(filename):
    yt_descr = _get_youtube_description_ru(filename)
    yt_descr += 'English original: ' + _get_youtube_link(filename, 'orig') + '\n'
    yt_descr += 'Моно перевод: ' + _get_youtube_link(filename, 'rus_mono')
    return yt_descr


def get_youtube_description_ru_mono(filename):
    yt_descr = _get_youtube_description_ru(filename)
    yt_descr += 'English original: ' + _get_youtube_link(filename, 'orig') + '\n'
    yt_descr += 'Стерео перевод: ' + _get_youtube_link(filename, 'rus_stereo')
    return yt_descr


def update_yaml(orig_mp4_filename, key, value):
    yaml_filename = os.path.splitext(orig_mp4_filename)[0] + '.yml'
    yamlupdater.set(yaml_filename, key, value)
    global _yaml_data_cache
    if orig_mp4_filename in _yaml_data_cache:
        _yaml_data_cache[orig_mp4_filename][key] = value
