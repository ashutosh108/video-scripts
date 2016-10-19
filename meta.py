import os
import re
import yaml
import datetime
import string
import numbers
import babel.dates

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


def _get_skip_time(filename: str) -> str:
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
    y = _yaml_data(filename)
    try:
        skip = y['skip']
        if isinstance(skip, numbers.Number):
            skip = str(datetime.timedelta(seconds=y['skip']))
        return skip
    except KeyError:
        return None


def get_ss_args(filename):
    skip_time = _get_skip_time(filename)
    if skip_time:
        return ['-ss', skip_time]
    else:
        return []


def _get_title_en(filename):
    y = _yaml_data(filename)
    try:
        return y['title_en']
    except KeyError:
        try:
            return y['title_eng']
        except KeyError:
            return os.path.basename(os.path.splitext(filename)[0])


def _get_title_ru(filename):
    y = _yaml_data(filename)
    try:
        return y['title_ru']
    except KeyError:
        try:
            return y['title_rus']
        except KeyError:
            return os.path.basename(os.path.splitext(filename)[0])


def _artist_real_name_en(artist):
    known_artists = dict(
        goswamimj='Bhakti Sudhir Goswami',
        bsgoswami='Bhakti Sudhir Goswami',
        janardanmj='Bhakti Pavan Janardan',
        bpjanardan='Bhakti Pavan Janardan',
        avadhutmj='Bhakti Bimal Avadhut',
        bbavadhut='Bhakti Bimal Avadhut',
        madhusudanmj='Bhakti Rañjan Madhusudan',
        brmadhusudan='Bhakti Rañjan Madhusudan'
    )
    if artist in known_artists:
        return known_artists[artist]
    return artist


def _artist_real_name_ru(artist):
    known_artists = dict(
        goswamimj='Бхакти Судхир Госвами',
        bsgoswami='Бхакти Судхир Госвами',
        janardanmj='Бхакти Паван Джанардан',
        bpjanardan='Бхакти Паван Джанардан',
        avadhutmj='Бхакти Бимал Авадхут',
        bbavadhut='Бхакти Бимал Авадхут',
        madhusudanmj='Бхакти Ранджан Мадхусудан',
        brmadhusudan='Бхакти Ранджан Мадхусудан'
    )
    if artist in known_artists:
        return known_artists[artist]
    return artist


def _get_artist_en(filename):
    basename = os.path.basename(filename)
    match = re.match('^(\d\d\d\d)-?(\d\d)-?(\d\d)\s+(.*)\.', basename)
    if match is not None:
        artists_str = match.group(4)
        artists = []
        for artist in artists_str.split('_'):
            artists.append(_artist_real_name_en(artist))
        return ', '.join(artists)
    else:
        return 'Unknown'


def _get_artist_ru(filename):
    basename = os.path.basename(filename)
    match = re.match('^(\d\d\d\d)-?(\d\d)-?(\d\d)\s+(.*)\.', basename)
    if match is not None:
        artists_str = match.group(4)
        artists = []
        for artist in artists_str.split('_'):
            artists.append(_artist_real_name_ru(artist))
        return ', '.join(artists)
    else:
        return 'Автор неизвестен'


def _get_year_month_day(filename):
    basename = os.path.basename(filename)
    match = re.match('^(\d\d\d\d)-?(\d\d)-?(\d\d)', basename)
    if match:
        return match.groups()
    return [None, None, None]


def ffmpeg_meta_args_en(filename):
    title = _get_title_en(filename)
    artist = _get_artist_en(filename)
    [year, month, day] = _get_year_month_day(filename)
    args = [
       '-metadata', 'artist=' + artist,
       '-metadata', 'title=' + title,
       '-metadata', 'album=Gupta Govardhan 2016',
       '-metadata', 'genre=Speech']
    if year:
        args += ['-metadata', 'date=' + year + '-' + month + '-' + day]
        args += ['-metadata', 'comment=' + year + '-' + month + '-' + day]
    return args


def ffmpeg_meta_args_ru_mono(filename):
    title = _get_title_ru(filename) + ' (моно)'
    artist = _get_artist_ru(filename)
    [year, month, day] = _get_year_month_day(filename)
    args = [
       '-metadata', 'artist=' + artist,
       '-metadata', 'title=' + title,
       '-metadata', 'album=Гупта Говардхан 2016',
       '-metadata', 'genre=Speech']
    if year:
        args += ['-metadata', 'date=' + year + '-' + month + '-' + day]
        args += ['-metadata', 'comment=' + year + '-' + month + '-' + day]
    return args


def ffmpeg_meta_args_ru_stereo(filename):
    title = _get_title_ru(filename)
    artist = _get_artist_ru(filename)
    [year, month, day] = _get_year_month_day(filename)
    args = [
       '-metadata', 'artist=' + artist,
       '-metadata', 'title=' + title,
       '-metadata', 'album=Гупта Говардхан 2016',
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


def get_youtube_title_en(filename):
    title = _get_title_en(filename)
    if title[-1] not in string.punctuation:
        title += '.'
    artist = _get_artist_en(filename)
    return title + ' ' + artist


def get_youtube_title_ru_stereo(filename):
    title = _get_title_ru(filename)
    if title[-1] not in string.punctuation:
        title += '.'
    artist = _get_artist_ru(filename)
    return title + ' ' + artist


def get_youtube_title_ru_mono(filename):
    title = _get_title_ru(filename)
    title_without_dot = title
    dot = '.'
    if title[-1] in string.punctuation and title[-1] != '.':
        dot = ''
    if title[-1] == '.':
        title_without_dot = title_without_dot[:-1]
    artist = _get_artist_ru(filename)
    return title_without_dot + ' (моно)' + dot + ' ' + artist


def _get_description_en(filename):
    try:
        return _yaml_data(filename)['descr_en']
    except KeyError:
        try:
            return _yaml_data(filename)['descr_eng']
        except KeyError:
            return ''


def _get_description_ru(filename):
    try:
        return _yaml_data(filename)['descr_ru']
    except KeyError:
        try:
            return _yaml_data(filename)['descr_rus']
        except KeyError:
            return ''


def _srila_maharaj_en(name):
    return 'Srila ' + name + ' Maharaj'


def _get_author_with_title_en(filename):
    authors = _get_artist_en(filename).split(', ')
    return ', '.join(map(_srila_maharaj_en, authors))


def get_youtube_description_en(filename):
    year, month, day = _get_year_month_day(filename)
    dt_obj = datetime.date(int(year), int(month), int(day))
    author_with_title = _get_author_with_title_en(filename)
    date = '{dt:%B} {dt.day}, {dt:%Y}'.format(dt=dt_obj)
    yt_descr = _get_description_en(filename) + '\n'
    yt_descr += author_with_title + '\n'  # e.g. Srila Bhakti Rañjan Madhusudan Maharaj
    yt_descr += date + '\n'  # e.g. October 11, 2016
    yt_descr += 'Theistic Media Studios, Gupta Govardhan Ashram.\n'
    yt_descr += 'Downloaded from TMS_TV livestream.com/accounts/2645002\n\n'
    yt_descr += 'На русском: (ссылка скоро будет)'
    return yt_descr


def _srila_maharaj_ru(name):
    return 'Шрила ' + name + ' Махарадж'


def _get_author_with_title_ru(filename):
    authors = _get_artist_ru(filename).split(', ')
    return ', '.join(map(_srila_maharaj_ru, authors))


def get_youtube_description_ru_stereo(filename):
    year, month, day = _get_year_month_day(filename)
    dt_obj = datetime.date(int(year), int(month), int(day))
    author_with_title = _get_author_with_title_ru(filename)
    date = babel.dates.format_datetime(dt_obj, 'dd MMMM YYYY', locale='ru_RU')
    yt_descr = _get_description_ru(filename) + '\n'
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
    yt_descr = _get_description_ru(filename) + '\n'
    yt_descr += author_with_title + '\n'  # e.g. Srila Bhakti Rañjan Madhusudan Maharaj
    yt_descr += date + '\n'  # e.g. October 11, 2016
    yt_descr += 'Студия "Теистик Медиа", Ашрам на Гупта Говардхане.\n'
    yt_descr += 'Загружено с TMS_TV livestream.com/accounts/2645002\n\n'
    yt_descr += 'English original: (link pending)\n'
    yt_descr += 'Стерео перевод: (link pending)'
    return yt_descr
