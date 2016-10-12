import os
import subprocess
import sys

import meta


def usage_and_exit():
    print("""demux: extract (demux) english AAC audio from Goswami Maharaj's video into separate m4a file
usage: demux "yyyy-mm-dd goswamimj.mp4"
(or drag and drop the file onto me)""")
    exit()


def demux_file(filename: str) -> None:
    skip_time = meta.get_ss_arg_for_file(filename)
    title = meta.get_title_for_file(filename)
    artist = meta.get_artist_eng(filename)
    [year, month, day] = meta.get_year_month_day(filename)

    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    basename_wo_ext = os.path.splitext(basename)[0]
    eng_m4a = os.path.join(dirname, 'temp', basename_wo_ext + '_eng.m4a')
    plain_m4a = os.path.join(dirname, 'temp', basename_wo_ext + '.m4a')
    cmd = ['ffmpeg',
           '-y',
           '-i', filename,
           '-metadata', 'artist=' + artist,
           '-metadata', 'title=' + title,
           '-metadata', 'album=Gupta Govardhan 2016',
           '-metadata', 'genre=Speech']
    if year:
        cmd += ['-metadata', 'date=' + year + '-' + month + '-' + day]
        cmd += ['-metadata', 'comment=' + year + '-' + month + '-' + day]
    if skip_time:
        cmd += ['-ss', skip_time]
    cmd += [
        '-c', 'copy', '-movflags', '+faststart',
        eng_m4a,
        '-c', 'copy', '-movflags', '+faststart',
        plain_m4a]
    print(repr(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    while 1:
        line = p.readline()
        if not line: break
        print(line)

def main():
    try:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print('file "%s" not found' % filename)
            print('')
            usage_and_exit()
        demux_file(filename)
    except IndexError:
        usage_and_exit()

if __name__ == '__main__':
    main()
