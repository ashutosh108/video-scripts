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
        cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', filename]
        res = subprocess.run(cmd, stdout=subprocess.PIPE)
        json_str = res.stdout.decode('utf-8')
        json_obj = json.loads(json_str)
        return [int(json_obj['streams'][0]['width']), int(json_obj['streams'][0]['height'])]
    except KeyError:
        return [1280, 720]


# return array of ffmpeg options to match the video in the given file (same h.264 profile, same level)
def get_ffmpeg_encoding_options_from_video_file(filename):
    (h264_profile, h264_level) = get_h264_profile_and_level(filename)
    return ['-c:a', 'copy', '-c:v', 'libx264', '-profile:v', h264_profile, '-level:v', h264_level]


def get_h264_profile_and_level(filename):
    try:
        cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', filename]
        res = subprocess.run(cmd, stdout=subprocess.PIPE)
        json_str = res.stdout.decode('utf-8')
        json_obj = json.loads(json_str)
        profile = str.lower(json_obj['streams'][0]['profile'])
        level = str(json_obj['streams'][0]['level'])
        level_dotted = level[0] + '.' + level[1]
        return [profile, level_dotted]
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

    f_transparent = 'geq=r=r(X\,Y):a=if(r(X\,Y)\,r(X\,Y)\,16)'
    filter_complex = ''
    filter_complex += ',' + f_author
    filter_complex += ',' + f_shift_down
    filter_complex += ',' + f_title
    filter_complex += ',' + f_shift_up
    filter_complex += ',' + f_transparent
    filter_complex = filter_complex[1:]
    cmd = ['ffmpeg',
            '-f', 'lavfi', '-i', 'color=c=black:s={width}x{height}:d=10,format=rgba'.format(width=width, height=height),
            '-filter_complex', filter_complex,
            '-frames:v', '1',
            '-y', png_filename
            ]
    os.environ['FONTCONFIG_FILE'] = 'C:\\Users\\ashutosh\\Dropbox\\Reference\\S\\scripts\\fonts\\fonts.conf'
    subprocess.run(cmd)
    os.remove(author_srt)
    os.remove(title_srt)
    return png_filename


def make_title_ts(orig_mp4_filename, lang, seconds):
    png_filename = make_png(orig_mp4_filename, lang)
    ts_title_filename = meta.get_work_filename(orig_mp4_filename, ' {lang}_title.ts'.format(lang=lang))

    filter_complex = ''
    filter_complex += ';[1:v]fade=out:st=9:d=1:alpha=1[title]'
    filter_complex += ';[0:v][title]overlay,format=yuv420p'
    filter_complex = filter_complex[1:]
    cmd = ['ffmpeg', '-y']
    cmd += ffmpeg.ss_args(orig_mp4_filename)
    cmd += ['-i', orig_mp4_filename,
            '-loop', '1', '-i', png_filename,
            '-filter_complex', filter_complex,
            '-bsf:v', 'h264_mp4toannexb',
            '-t', str(seconds)]
    cmd += get_ffmpeg_encoding_options_from_video_file(orig_mp4_filename)
    cmd += [ts_title_filename]
    print(cmd)
    subprocess.run(cmd)
    return ts_title_filename


def make_rest_ts(orig_mp4_filename, lang, title_end_time):
    ts_rest_filename = meta.get_work_filename(orig_mp4_filename, ' {lang}_rest.ts'.format(lang=lang))
    cmd = ['ffmpeg', '-y',
           '-i', orig_mp4_filename,
           '-c', 'copy', '-bsf:v', 'h264_mp4toannexb']
    cmd += ['-ss', str(title_end_time)]
    cmd += ffmpeg.to_args(orig_mp4_filename)
    cmd += [ts_rest_filename]
    print(cmd)
    subprocess.run(cmd)
    return ts_rest_filename


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


def concatenate_ts_to_mp4(filename_ts1, filename_ts2, filename_mp4):
    print(filename_ts1, filename_ts2, filename_mp4)
    cmd = ['ffmpeg', '-y',
           '-i', 'concat:{}|{}'.format(filename_ts1, filename_ts2),
           '-c', 'copy', '-bsf:a', 'aac_adtstoasc',
           filename_mp4]
    print(cmd)
    subprocess.run(cmd)


def make_mp4_with_title(orig_mp4_filename, lang, cut_video_filename):
    ts_title_filename, ts_rest_filename = make_ts_files_with_title_and_rest(orig_mp4_filename, lang)
    concatenate_ts_to_mp4(ts_title_filename, ts_rest_filename, cut_video_filename)


def make_ts_files_with_title_and_rest(orig_mp4_filename, lang):
    title_start_time = meta.get_skip_time_timedelta(orig_mp4_filename)
    min_title_end_time = title_start_time + datetime.timedelta(seconds=10)
    title_end_time = get_next_keyframe_timestamp(orig_mp4_filename, min_title_end_time)
    title_len_seconds = (title_end_time - title_start_time).total_seconds()
    ts_title_filename = make_title_ts(orig_mp4_filename, lang, title_len_seconds)
    ts_rest_filename = make_rest_ts(orig_mp4_filename, lang, title_end_time)
    return ts_title_filename, ts_rest_filename


def main():
    filename = sys.argv[1]
    # make_title_mp4(filename, meta.get_lang(filename))
    # make_rest_mp4(filename, meta.get_lang(filename))
    # get_keyframes_timestamps(filename)
    lang = meta.get_lang(filename)
    cut_video_filename = meta.get_work_filename(filename, ' {} titled.mp4'.format(lang))
    make_mp4_with_title(filename, lang, cut_video_filename)
    cut_video_filename_ru = meta.get_work_filename(filename, ' {} titled.mp4'.format('ru'))
    make_mp4_with_title(filename, 'ru', cut_video_filename_ru)


if __name__ == '__main__':
    main()
