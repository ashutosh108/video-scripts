import os
import subprocess
import sys
import json

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


def make_png(orig_mp4_filename, lang):
    png_filename = meta.get_work_filename(orig_mp4_filename, ' ' + lang + '_title.png')

    [width, height] = get_video_size(orig_mp4_filename)
    scale = float(height) / 720;

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


def make_title_mp4(orig_mp4_filename, lang):
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
            '-t', '10',
             mp4_title_filename]
    subprocess.run(args)

if __name__ == '__main__':
    filename = sys.argv[1]
    make_title_mp4(filename, meta.get_lang(filename))
