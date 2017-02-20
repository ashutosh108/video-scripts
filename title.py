import os
import subprocess
import sys
import json
import datetime
import re

import meta
import ffmpeg


def get_video_size(filename):
    try:
        args = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', filename]
        res = subprocess.run(args, stdout=subprocess.PIPE)
        json_str = res.stdout.decode('utf-8')
        json_obj = json.loads(json_str)
        return [int(json_obj['streams'][0]['width']), int(json_obj['streams'][0]['height'])]
    except KeyError:
        return [1280, 720]


# return array of ffmpeg options to match the video in the given file (same h.264 profile, same level)
def get_ffmpeg_encoding_options_from_video_file(filename):
    h264_profile = get_h264_profile(filename)
    return ['-profile:v', h264_profile]


def get_h264_profile(filename):
    try:
        args = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', filename]
        res = subprocess.run(args, stdout=subprocess.PIPE)
        json_str = res.stdout.decode('utf-8')
        json_obj = json.loads(json_str)
        return str.lower(json_obj['streams'][0]['profile'])
    except KeyError:
        return 'main'


def make_png(orig_mp4_filename, lang):
    png_filename = meta.get_work_filename(orig_mp4_filename, ' ' + lang + '_title.png')

    [width, height] = get_video_size(orig_mp4_filename)
    scale = float(height) / 720

    authors = meta.get_artist(orig_mp4_filename, lang, 100)
    author_srt = meta.get_work_filename(orig_mp4_filename, ' ' + lang + '_author.srt')
    with open(author_srt, 'w', encoding='utf8') as f:
        f.write('1\n00:00:00,000 --> 09:59:59,990\n' + authors)
    author_srt_escaped = author_srt.replace('\\', '/')
    author_srt_escaped = author_srt_escaped.replace(':', '\\\\:')
    f_author = ('subtitles=filename={srt}' +
                ':force_style=\'FontName=Charis SIL,Fontsize={fontsize},' +
                'Alignment=10,PlayResX={width},PlayResY={height},PrimaryColour=&Hffffff\''
                ).format(srt=author_srt_escaped, fontsize=int(60*scale), width=width, height=height)
    f_shift_down = ('crop={width}:{height}-{shift}:0:0,pad={width}:{height}:0:{shift}:color=black@0.0'
                    ).format(shift=int(200*scale), width=width, height=height)

    title = meta.get_title(orig_mp4_filename, lang)
    title_srt = meta.get_work_filename(orig_mp4_filename, ' ' + lang + '_title.srt')
    with open(title_srt, 'w', encoding='utf8') as f:
        f.write('1\n00:00:00,000 --> 09:59:59,990\n' + title)
    title_srt_escaped = title_srt.replace('\\', '/')
    title_srt_escaped = title_srt_escaped.replace(':', '\\\\:')
    f_title = ('subtitles=filename={srt}' +
               ':force_style=\'FontName=Charis SIL,Fontsize={fontsize},' +
               'Alignment=10,PlayResX={width},PlayResY={height},PrimaryColour=&Hffffff\''
               ).format(srt=title_srt_escaped, fontsize=int(108*scale), width=width, height=height)
    f_shift_up = ('crop={width}:{height}-{shift}:0:{shift},pad={width}:{height}:0:0:color=black@0.0'
                  ).format(shift=int(80*scale), width=width, height=height)

    f_transparent = 'geq=r=r(X\,Y):a=if(r(X\,Y)\,r(X\,Y)\,122)'
    filter_complex = ''
    filter_complex += ',' + f_author
    filter_complex += ',' + f_shift_down
    filter_complex += ',' + f_title
    filter_complex += ',' + f_shift_up
    filter_complex += ',' + f_transparent
    filter_complex = filter_complex[1:]
    args = ['ffmpeg',
            '-f', 'lavfi', '-i', 'color=c=black:s={width}x{height}:d=10,format=rgba'.format(width=width, height=height),
            '-filter_complex', filter_complex,
            '-frames:v', '1',
            '-y', png_filename
            ]
    os.environ['FONTCONFIG_FILE'] = 'C:\\Users\\ashutosh\\Dropbox\\Reference\\S\\scripts\\fonts\\fonts.conf'
    subprocess.run(args)
    os.remove(author_srt)
    os.remove(title_srt)
    return png_filename


def make_title_mp4(orig_mp4_filename, lang, seconds):
    png_filename = make_png(orig_mp4_filename, lang)
    mp4_title_filename = meta.get_work_filename(orig_mp4_filename, ' {lang}_title.mp4'.format(lang=lang))

    filter_complex = ''
    filter_complex += ';[1:v]fade=out:st=9:d=1:alpha=1[title]'
    filter_complex += ';[0:v][title]overlay,format=yuv420p'
    filter_complex = filter_complex[1:]
    args = ['ffmpeg', '-y']
    args += ffmpeg.ss_args(orig_mp4_filename)
    args += ['-i', orig_mp4_filename,
            '-loop', '1', '-i', png_filename,
            '-filter_complex', filter_complex,
            '-t', str(seconds)]
    args += get_ffmpeg_encoding_options_from_video_file(orig_mp4_filename)
    args += [mp4_title_filename]
    subprocess.run(args)
    return mp4_title_filename


def make_rest_mp4(orig_mp4_filename, lang, title_end_time):
    mp4_rest_filename = meta.get_work_filename(orig_mp4_filename, ' {lang}_rest.mp4'.format(lang=lang))
    cmd = ['ffmpeg', '-y',
           '-i', orig_mp4_filename,
           '-c', 'copy']
    cmd += ['-ss', str(title_end_time)]
    cmd += ffmpeg.to_args(orig_mp4_filename)
    cmd += [mp4_rest_filename]
    subprocess.run(cmd)
    return mp4_rest_filename


def get_next_keyframe_timestamp(filename, start_time: datetime.timedelta):
    cmd = ['ffprobe', '-select_streams', 'v', '-show_frames',
           '-show_entries', 'frame=pict_type,best_effort_timestamp_time',
           '-of','csv',
           '-read_intervals', str(start_time)+'%+#500',
           filename]
    res = subprocess.run(cmd, stdout=subprocess.PIPE)
    res_arr = res.stdout.decode('utf-8').splitlines()
    for line in res_arr:
        m = re.match('^frame,(\d+\.\d+),I$', line)
        if m:
            timestamp = datetime.timedelta(seconds=float(m.group(1)))
            if timestamp >= start_time:
                return timestamp
    raise RuntimeError('Could not find next keyframe after ' + start_time)


def make_mp4_with_title(orig_mp4_filename, lang):
    skip_time_str = meta.get_skip_time(orig_mp4_filename)
    m = re.match('^((?P<h>\d+):)?(?P<m>\d+):(?P<s>\d+)$', skip_time_str)
    if not m:
        raise RuntimeError('Can\'t parse skip time as [hh:]mm:ss: "', skip_time_str, '"')
    title_start_time = datetime.timedelta(hours=int(m.group('h')), minutes=int(m.group('m')), seconds=int(m.group('s')))
    min_title_end_time = title_start_time + datetime.timedelta(seconds=10)
    title_end_time = get_next_keyframe_timestamp(orig_mp4_filename, min_title_end_time)
    title_len_seconds = (title_end_time - title_start_time).total_seconds()

    mp4_title_filename = make_title_mp4(orig_mp4_filename, lang, title_len_seconds)
    mp4_rest_filename = make_rest_mp4(orig_mp4_filename, lang, title_end_time)
    # concatenate_videos(mp4_title_filename, mp4_rest_filename, cut_video_filename)


if __name__ == '__main__':
    filename = sys.argv[1]
    # make_title_mp4(filename, meta.get_lang(filename))
    # make_rest_mp4(filename, meta.get_lang(filename))
    # get_keyframes_timestamps(filename)
    make_mp4_with_title(filename, meta.get_lang(filename))
