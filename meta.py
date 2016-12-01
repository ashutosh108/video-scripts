import os
import re
import yaml
import datetime
import string
import numbers
import babel.dates
import yamlupdater

_yaml_data_cache = {}


def _yaml_data(filename):
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


def get_ss_args(filename):
    skip_time = get_skip_time(filename)
    if skip_time:
        return ['-ss', skip_time]
    else:
        return []


def _yaml_get_time_length(filename: str, key: str) -> str:
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


def get_to_args(filename):
    cut_time = _yaml_get_time_length(filename, 'cut')
    if cut_time:
        return ['-to', cut_time]
    else:
        return []


def get_lang(filename):
    try:
        return _yaml_data(filename)['lang']
    except KeyError:
        return 'en'


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
    goswamimj=['Bhakti Sudhīr Goswāmī', 'Śrīla Bhakti Sudhīr Goswāmī Mahārāj'],
    bsgoswami=['Bhakti Sudhīr Goswāmī', 'Śrīla Bhakti Sudhīr Goswāmī Mahārāj'],
    janardanmj=['Bhakti Pāvan Janārdan', 'Śrīla Bhakti Pāvan Janārdan Mahārāj'],
    bpjanardan=['Bhakti Pāvan Janārdan', 'Śrīla Bhakti Pāvan Janārdan Mahārāj'],
    avadhutmj=['Bhakti Bimal Avadhūt', 'Śrīla Bhakti Bimal Avadhūt Mahārāj'],
    bbavadhut=['Bhakti Bimal Avadhūt', 'Śrīla Bhakti Bimal Avadhūt Mahārāj'],
    madhusudanmj=['Bhakti Rañjan Madhusūdan', 'Śrīla Bhakti Rañjan Madhusūdan Mahārāj'],
    brmadhusudan=['Bhakti Rañjan Madhusūdan', 'Śrīla Bhakti Rañjan Madhusūdan Mahārāj'],
    hasyapriya=['Hāsyapriya Prabhu', 'Hāsyapriya Prabhu'],
    taritkrishna = ['Tārit Kṛṣṇa Prabhu', 'Tārit Kṛṣṇa Prabhu']
)


def _artist_real_name_en(artist_code):
    if artist_code in _known_artists_en:
        return _known_artists_en[artist_code][0]
    return artist_code


def _artist_full_name_en(artist_code):
    if artist_code in _known_artists_en:
        return _known_artists_en[artist_code][1]
    return artist_code


_known_artists_ru = dict(
    goswamimj=['Бхакти Судхӣр Госва̄мӣ', 'Ш́рӣла Бхакти Судхӣр Госва̄мӣ Mаха̄ра̄дж'],
    bsgoswami=['Бхакти Судхӣр Госва̄мӣ', 'Ш́рӣла Бхакти Судхӣр Госва̄мӣ Mаха̄ра̄дж'],
    janardanmj=['Бхакти Па̄ван Джана̄рдан', 'Ш́рӣла Бхакти Па̄ван Джана̄рдан Mаха̄ра̄дж'],
    bpjanardan=['Бхакти Па̄ван Джана̄рдан', 'Ш́рӣла Бхакти Па̄ван Джана̄рдан Mаха̄ра̄дж'],
    avadhutmj=['Бхакти Бимал Авадхӯт', 'Ш́рӣла Бхакти Бимал Авадхӯт Mаха̄ра̄дж'],
    bbavadhut=['Бхакти Бимал Авадхӯт', 'Ш́рӣла Бхакти Бимал Авадхӯт Mаха̄ра̄дж'],
    madhusudanmj=['Бхакти Ран̃джан Мадхусӯдан', 'Ш́рӣла Бхакти Ран̃джан Мадхусӯдан Mаха̄ра̄дж'],
    brmadhusudan=['Бхакти Ран̃джан Мадхусӯдан', 'Ш́рӣла Бхакти Ран̃джан Мадхусӯдан Mаха̄ра̄дж'],
    hasyapriya=['Ха̄сьяприя Прабху', 'Ха̄сьяприя Прабху'],
    taritkrishna=['Та̄рит Кр̣ш̣н̣а Прабху', 'Та̄рит Кр̣ш̣н̣а Прабху'],
    unknown=['Автор неизвестен', 'Автор неизвестен']
)


def _artist_real_name_ru(artist):
    if artist in _known_artists_ru:
        return _known_artists_ru[artist][0]
    return artist


def _artist_full_name_ru(artist_code):
    if artist_code in _known_artists_ru:
        return _known_artists_ru[artist_code][1]
    return artist_code


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


def _get_artist_en(filename):
    codes = _get_artists_codes(filename)
    names = map(lambda code: _artist_real_name_en(code), codes)
    return ', '.join(names)


def _get_artist_ru(filename):
    codes = _get_artists_codes(filename)
    names = map(lambda code: _artist_real_name_ru(code), codes)
    return ', '.join(names)


def _get_year_month_day(filename):
    basename = os.path.basename(filename)
    match = re.match('^(\d\d\d\d)-?(\d\d)-?(\d\d)', basename)
    if match:
        return match.groups()
    return [None, None, None]


def ffmpeg_meta_args(filename, lang):
    if lang == 'ru':
        return ffmpeg_meta_args_ru_stereo(filename)
    else:
        return _ffmpeg_meta_args_en(filename)


def _ffmpeg_meta_args_en(filename):
    artist = _get_artist_en(filename)
    title = get_title_en(filename)
    return _ffmpeg_meta_args(filename, artist, title, album='Gupta Govardhan 2016')


def ffmpeg_meta_args_ru_mono(filename):
    artist = _get_artist_ru(filename)
    title = get_title_ru(filename) + ' (моно)'
    return _ffmpeg_meta_args(filename, artist, title, 'Гупта Говардхан 2016')


def ffmpeg_meta_args_ru_stereo(filename):
    artist = _get_artist_ru(filename)
    title = get_title_ru(filename)
    return _ffmpeg_meta_args(filename, artist, title, 'Гупта Говардхан 2016')


def _ffmpeg_meta_args(filename, artist, title, album):
    [year, month, day] = _get_year_month_day(filename)
    args = [
        '-id3v2_version', '3',
        '-write_id3v1', '1',
        '-metadata', 'artist=' + artist,
        '-metadata', 'title=' + title,
        '-metadata', 'album=' + album,
        '-metadata', 'genre=Speech']
    if year:
        args += ['-metadata', 'date=' + year + '-' + month + '-' + day]
        args += ['-metadata', 'comment=' + year + '-' + month + '-' + day]
    return args


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
    artist = _get_artist_en(filename)
    return title + ' ' + artist


def get_youtube_title_ru_stereo(filename):
    title = get_title_ru(filename)
    if title[-1] not in string.punctuation:
        title += '.'
    artist = _get_artist_ru(filename)
    return title + ' ' + artist


def get_youtube_title_ru_mono(filename):
    title = get_title_ru(filename)
    title_without_dot = title
    dot = '.'
    if title[-1] in string.punctuation and title[-1] != '.':
        dot = ''
    if title[-1] == '.':
        title_without_dot = title_without_dot[:-1]
    artist = _get_artist_ru(filename)
    return title_without_dot + ' (моно)' + dot + ' ' + artist


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


def get_youtube_description(filename, lang):
    if lang == 'ru':
        return _get_youtube_description_ru_orig(filename)
    else:
        return _get_youtube_description_en(filename)


def _get_youtube_description_en(filename):
    year, month, day = _get_year_month_day(filename)
    dt_obj = datetime.date(int(year), int(month), int(day))
    author_with_title = _get_author_with_title_en(filename)
    date = '{dt:%B} {dt.day}, {dt:%Y}'.format(dt=dt_obj)
    yt_descr = get_description_en(filename) + '\n'
    yt_descr += author_with_title + '\n'  # e.g. Srila Bhakti Rañjan Madhusudan Maharaj
    yt_descr += date + '\n'  # e.g. October 11, 2016
    yt_descr += 'Theistic Media Studios, Gupta Govardhan Ashram.\n'
    yt_descr += 'Downloaded from TMS_TV livestream.com/accounts/2645002\n\n'
    yt_descr += 'На русском: (ссылка скоро будет)'
    return yt_descr


def _get_author_with_title_ru(filename):
    authors_codes = _get_artists_codes(filename)
    authors_full_names = map(_artist_full_name_ru, authors_codes)
    return ', '.join(authors_full_names)


def _get_youtube_description_ru_orig(filename):
    year, month, day = _get_year_month_day(filename)
    dt_obj = datetime.date(int(year), int(month), int(day))
    author_with_title = _get_author_with_title_ru(filename)
    date = babel.dates.format_datetime(dt_obj, 'dd MMMM YYYY', locale='ru_RU')
    yt_descr = get_description_ru(filename) + '\n'
    yt_descr += author_with_title + '\n'  # e.g. Srila Bhakti Rañjan Madhusudan Maharaj
    yt_descr += date + '\n'  # e.g. October 11, 2016
    yt_descr += 'Студия "Теистик Медиа", Ашрам на Гупта Говардхане.\n'
    yt_descr += 'Загружено с TMS_TV livestream.com/accounts/2645002\n\n'
    return yt_descr


def get_youtube_description_ru_stereo(filename):
    year, month, day = _get_year_month_day(filename)
    dt_obj = datetime.date(int(year), int(month), int(day))
    author_with_title = _get_author_with_title_ru(filename)
    date = babel.dates.format_datetime(dt_obj, 'dd MMMM YYYY', locale='ru_RU')
    yt_descr = get_description_ru(filename) + '\n'
    yt_descr += author_with_title + '\n'  # e.g. Srila Bhakti Rañjan Madhusudan Maharaj
    yt_descr += date + '\n'  # e.g. October 11, 2016
    yt_descr += 'Студия "Теистик Медиа", Ашрам на Гупта Говардхане.\n'
    yt_descr += 'Загружено с TMS_TV livestream.com/accounts/2645002\n\n'
    yt_descr += 'English original: (link pending)\n'
    yt_descr += 'Моно перевод: (link pending)'
    return yt_descr


def get_youtube_description_ru_mono(filename):
    year, month, day = _get_year_month_day(filename)
    dt_obj = datetime.date(int(year), int(month), int(day))
    author_with_title = _get_author_with_title_ru(filename)
    date = babel.dates.format_datetime(dt_obj, 'dd MMMM YYYY', locale='ru_RU')
    yt_descr = get_description_ru(filename) + '\n'
    yt_descr += author_with_title + '\n'  # e.g. Srila Bhakti Rañjan Madhusudan Maharaj
    yt_descr += date + '\n'  # e.g. October 11, 2016
    yt_descr += 'Студия "Теистик Медиа", Ашрам на Гупта Говардхане.\n'
    yt_descr += 'Загружено с TMS_TV livestream.com/accounts/2645002\n\n'
    yt_descr += 'English original: (link pending)\n'
    yt_descr += 'Стерео перевод: (link pending)'
    return yt_descr


def update_yaml(orig_mp4_filename, key, value):
    yaml_filename = os.path.splitext(orig_mp4_filename)[0] + '.yml'
    yamlupdater.set(yaml_filename, key, value)
    global _yaml_data_cache
    if orig_mp4_filename in _yaml_data_cache:
        _yaml_data_cache[orig_mp4_filename][key] = value
