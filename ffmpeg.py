from meta import get_skip_time, get_cut_time, get_artist_en, get_title_en, get_artist_ru, get_title_ru, \
    get_year_month_day


def ss_args(filename):
    skip_time = get_skip_time(filename)
    if skip_time:
        return ['-ss', skip_time]
    else:
        return []


def to_args(filename):
    cut_time = get_cut_time(filename)
    if cut_time:
        return ['-to', cut_time]
    else:
        return []


def meta_args(filename, lang):
    if lang == 'ru':
        return meta_args_ru_stereo(filename)
    else:
        return _meta_args_en(filename)


def _meta_args_en(filename):
    artist = get_artist_en(filename)
    title = get_title_en(filename)
    [year, month, day] = get_year_month_day(filename)
    return _meta_args(filename, artist, title, album='Gupta Govardhan ' + year)


def meta_args_ru_mono(filename):
    artist = get_artist_ru(filename)
    title = get_title_ru(filename) + ' (моно)'
    [year, month, day] = get_year_month_day(filename)
    return _meta_args(filename, artist, title, 'Гупта Говардхан ' + year)


def meta_args_ru_stereo(filename):
    artist = get_artist_ru(filename)
    title = get_title_ru(filename)
    [year, month, day] = get_year_month_day(filename)
    return _meta_args(filename, artist, title, 'Гупта Говардхан ' + year)


def _meta_args(filename, artist, title, album):
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
