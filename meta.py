import os
import re
import yaml
import datetime
import string

_yaml_data = {}


def yaml_data(filename):
    global _yaml_data
    if filename not in _yaml_data:
        try:
            yaml_filename = os.path.splitext(filename)[0] + '.yml'
            with open(yaml_filename, 'r', encoding='UTF-8') as f:
                _yaml_data[filename] = yaml.load(f)
        except (IndexError, FileNotFoundError) as e:
            _yaml_data[filename] = dict()
    return _yaml_data[filename]


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
    y = yaml_data(filename)
    try:
        return str(datetime.timedelta(seconds=y['skip']))
    except KeyError:
        return None


def get_ss_args(filename):
    skip_time = get_skip_time(filename)
    if skip_time:
        return ['-ss', skip_time]
    else:
        return []


def get_title_for_file(filename):
    basename = os.path.basename(filename)
    basename_wo_ext = os.path.splitext(basename)[0]
    title = basename_wo_ext.replace(' goswamimj', '')
    return title


def get_title_eng(filename):
    y = yaml_data(filename)
    try:
        return y['title_eng']
    except KeyError:
        return os.path.basename(os.path.splitext(filename)[0])


def get_title_rus(filename):
    y = yaml_data(filename)
    try:
        return y['title_rus']
    except KeyError:
        return os.path.basename(os.path.splitext(filename)[0])


def artist_real_name(artist):
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


def artist_real_name_rus(artist):
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


def get_artist_eng(filename):
    basename = os.path.basename(filename)
    match = re.match('^(\d\d\d\d)-?(\d\d)-?(\d\d)\s+(.*)\.', basename)
    if match is not None:
        artists_str = match.group(4)
        artists = []
        for artist in artists_str.split('_'):
            artists.append(artist_real_name(artist))
        return ', '.join(artists)
    else:
        return 'Unknown'


def get_artist_rus(filename):
    basename = os.path.basename(filename)
    match = re.match('^(\d\d\d\d)-?(\d\d)-?(\d\d)\s+(.*)\.', basename)
    if match is not None:
        artists_str = match.group(4)
        artists = []
        for artist in artists_str.split('_'):
            artists.append(artist_real_name_rus(artist))
        return ', '.join(artists)
    else:
        return 'Автор неизвестен'


def get_year_month_day(filename):
    basename = os.path.basename(filename)
    match = re.match('^(\d\d\d\d)-?(\d\d)-?(\d\d)', basename)
    if match:
        return match.groups()
    return [None, None, None]


def ffmpeg_meta_args(filename):
    title = get_title_eng(filename)
    artist = get_artist_eng(filename)
    [year, month, day] = get_year_month_day(filename)
    args = [
       '-metadata', 'artist=' + artist,
       '-metadata', 'title=' + title,
       '-metadata', 'album=Gupta Govardhan 2016',
       '-metadata', 'genre=Speech']
    if year:
        args += ['-metadata', 'date=' + year + '-' + month + '-' + day]
        args += ['-metadata', 'comment=' + year + '-' + month + '-' + day]
    return args


def ffmpeg_meta_args_rus_mono(filename):
    title = get_title_rus(filename) + ' (моно)'
    artist = get_artist_rus(filename)
    [year, month, day] = get_year_month_day(filename)
    args = [
       '-metadata', 'artist=' + artist,
       '-metadata', 'title=' + title,
       '-metadata', 'album=Гупта Говардхан 2016',
       '-metadata', 'genre=Speech']
    if year:
        args += ['-metadata', 'date=' + year + '-' + month + '-' + day]
        args += ['-metadata', 'comment=' + year + '-' + month + '-' + day]
    return args


def ffmpeg_meta_args_rus_stereo(filename):
    title = get_title_rus(filename)
    artist = get_artist_rus(filename)
    [year, month, day] = get_year_month_day(filename)
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
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    basename_wo_ext = os.path.splitext(basename)[0]
    return os.path.join(dirname, 'temp', basename_wo_ext + add)


def get_youtube_title_eng(filename):
    title = get_title_eng(filename)
    if title[-1] not in string.punctuation:
        title += '.'
    artist = get_artist_eng(filename)
    return title + ' ' + artist


def get_description_eng(filename):
    try:
        return yaml_data(filename)['descr_eng']
    except KeyError:
        return ''


def srila_maharaj_eng(name):
    return 'Srila ' + name + ' Maharaj'


def get_author_with_title_eng(filename):
    authors = get_artist_eng(filename).split(', ')
    return ', '.join(map(srila_maharaj_eng, authors))


def get_youtube_description_eng(filename):
    year, month, day = get_year_month_day(filename)
    dt_obj = datetime.date(int(year), int(month), int(day))
    author_with_title = get_author_with_title_eng(filename)
    date = '{dt:%B} {dt.day}, {dt:%Y}'.format(dt=dt_obj)
    yt_descr = get_description_eng(filename) + '\n'
    yt_descr += author_with_title + '\n'  # e.g. Srila Bhakti Rañjan Madhusudan Maharaj
    yt_descr += date + '\n'  # e.g. October 11, 2016
    yt_descr += 'Theistic Media Studios, Gupta Govardhan Ashram.\n'
    yt_descr += 'Downloaded from TMS_TV livestream.com/accounts/2645002\n\n'
    yt_descr += 'На русском: (ссылка скоро будет)'
    return yt_descr
