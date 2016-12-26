from meta import get_skip_time, get_cut_time, get_artist_en, get_title_en, get_artist_ru, get_title_ru, \
    get_year_month_day


def get_ss_args(filename):
    skip_time = get_skip_time(filename)
    if skip_time:
        return ['-ss', skip_time]
    else:
        return []


def get_to_args(filename):
    cut_time = get_cut_time(filename)
    if cut_time:
        return ['-to', cut_time]
    else:
        return []


def ffmpeg_meta_args(filename, lang):
    if lang == 'ru':
        return ffmpeg_meta_args_ru_stereo(filename)
    else:
        return _ffmpeg_meta_args_en(filename)


def _ffmpeg_meta_args_en(filename):
    artist = get_artist_en(filename)
    title = get_title_en(filename)
    return _ffmpeg_meta_args(filename, artist, title, album='Gupta Govardhan 2016')


def ffmpeg_meta_args_ru_mono(filename):
    artist = get_artist_ru(filename)
    title = get_title_ru(filename) + ' (моно)'
    return _ffmpeg_meta_args(filename, artist, title, 'Гупта Говардхан 2016')


def ffmpeg_meta_args_ru_stereo(filename):
    artist = get_artist_ru(filename)
    title = get_title_ru(filename)
    return _ffmpeg_meta_args(filename, artist, title, 'Гупта Говардхан 2016')


def _ffmpeg_meta_args(filename, artist, title, album):
    [year, month, day] = get_year_month_day(filename)
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
