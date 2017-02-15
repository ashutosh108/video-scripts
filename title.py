import os
import subprocess
import sys

import meta


def make_png(orig_mp4_filename, lang):
    png_filename = meta.get_work_filename(orig_mp4_filename, ' ' + lang + '_title.png')

    width = 1280
    height = 720

    authors = meta.get_artist(orig_mp4_filename, lang, 100)
    author_srt = meta.get_work_filename(orig_mp4_filename, ' ' + lang + '_author.srt')
    with open(author_srt, 'w', encoding='utf8') as f:
        f.write('1\n00:00:00,000 --> 09:59:59,990\n' + authors)
    author_srt_escaped = author_srt.replace('\\', '/')
    author_srt_escaped = author_srt_escaped.replace(':', '\\\\:')
    f_author = ('subtitles=filename={srt}' +
                ':force_style=\'FontName=Charis SIL,Fontsize={fontsize},' +
                'Alignment=10,PlayResX={width},PlayResY={height},PrimaryColour=&Hffffff\''
                ).format(srt=author_srt_escaped, fontsize=60, width=width, height=height)
    f_shift_down = ('crop={width}:{height}-{shift}:0:0,pad={width}:{height}:0:{shift}:color=black@0.0'
                    ).format(shift=200, width=width, height=height)

    title = meta.get_title(orig_mp4_filename, lang)
    title_srt = meta.get_work_filename(orig_mp4_filename, ' ' + lang + '_title.srt')
    with open(title_srt, 'w', encoding='utf8') as f:
        f.write('1\n00:00:00,000 --> 09:59:59,990\n' + title)
    title_srt_escaped = title_srt.replace('\\', '/')
    title_srt_escaped = title_srt_escaped.replace(':', '\\\\:')
    f_title = ('subtitles=filename={srt}' +
               ':force_style=\'FontName=Charis SIL,Fontsize={fontsize},' +
               'Alignment=10,PlayResX={width},PlayResY={height},PrimaryColour=&Hffffff\''
               ).format(srt=title_srt_escaped, fontsize=108, width=width, height=height)
    f_shift_up = ('crop={width}:{height}-{shift}:0:{shift},pad={width}:{height}:0:0:color=black@0.0'
                  ).format(shift=80, width=width, height=height)

    f_transparent = 'geq=r=r(X\,Y):a=if(r(X\,Y)\,alpha(X\,Y)\,122)'
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


def old():
    # MakeEnTitlePng()

    filter_complex = ''
    filter_complex += ';[1:v]fade=out:st=9:d=1:alpha=1[title]'
    filter_complex += ';[0:v][title]overlay,format=yuv420p'
    # filter_complex += ';[title]null[out]'
    # filter_complex += ';[0:v]format=rgba,drawbox=0:0:1280:720:color=black@0.4:t=max,overlay'
    # filter_complex += ';[v0]null[v0fade]'
    # filter_complex += ';[2:v]null[v1fade]'
    # filter_complex += ';[v0]format=pix_fmts=yuva420p,fade=out:st=1:d=2:alpha=1[v0fade]'
    # filter_complex += ';[2:v]format=pix_fmts=yuva420p,fade=in:st=1:d=2:alpha=1[v1fade]'
    # filter_complex += ';[3:v][v0fade]overlay[over]'
    # filter_complex += ';[over][v1fade]overlay'
    filter_complex = filter_complex[1:]
    args = ['ffmpeg',
            '-ss', '1:15', '-i', '2017-01-25 goswamimj.mp4',
            '-loop', '1', '-i', 'qwe.png',
            '-filter_complex', filter_complex,
            '-y',
            # '-map', '[out]',
            # '-frames:v', '1',
            # '-v', 'debug',
            '-t', '10',
            'qwe.mp4']

    subprocess.call(args)
    subprocess.call(['C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe', '--sub-track-id=99', 'qwe.mp4'])
    # subprocess.run('start qwe.png', shell=True)

if __name__ == '__main__':
    filename = sys.argv[1]
    make_png(filename, meta.get_lang(filename))
