import os
import re
import yaml

_yaml_data = {}


def yaml_data(filename):
    global _yaml_data
    if filename not in _yaml_data:
        try:
            yaml_filename = os.path.splitext(filename)[0] + '.yml'
            with open(yaml_filename, 'r', encoding='UTF-8') as f:
                _yaml_data[filename] = yaml.load(f)
        except IndexError as e:
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
    return None


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
