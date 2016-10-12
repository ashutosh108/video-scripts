import sys
import os
import re

def usage_and_exit():
    print("""demux: extract (demux) english AAC audio from Goswami Maharaj's video into separate m4a file
usage: demux "yyyy-mm-dd goswamimj.mp4"
(or drag and drop the file onto me)""")
    exit()


def get_ss_arg_for_file(filename: str) -> str:
    """
    get proper argument for -ss min:sec part of the ffmpeg command line
    e.g. '2:51' if that's what's written in filename_offset.txt
    or None if that _offset file is not found
    :param filename:
    :return: string or None
    """
    try:
        name_wo_ext = os.path.splitext(filename)[0]
        offset_filename = '%s_offset.txt' % name_wo_ext
        with open(offset_filename) as f:
            return f.readline().rstrip()
    except FileNotFoundError:
        return None


def get_title_for_file(filename):
    basename = os.path.basename(filename)
    basename_wo_ext = os.path.splitext(basename)[0]
    title = basename_wo_ext.replace(' goswamimj', '')
    return title


def demux_file(filename: str) -> None:
    ss_arg = get_ss_arg_for_file(filename)
    title = get_title_for_file(filename)
    # ffmpeg ^
    #     -y ^
    #     -i %1 ^
    #     -map 0:a -c:a copy -movflags +faststart %ss_arg% ^
    #     -metadata artist="Bhakti Sudhir Goswami" ^
    #     -metadata title="%title%" ^
    #     -metadata album="Gupta Govardhan 2016" ^
    #     "%~dp1temp\%~n1_eng.m4a" ^
    #     -map 0:a -c:a copy -movflags +faststart          "%~dp1temp\%~n1.m4a"
    # pause
    #
    # :EXIT
    return

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
