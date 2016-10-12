import sys
import os

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
    skip_time = get_ss_arg_for_file(filename)
    ss_arg = ('-ss ' + skip_time) if skip_time  else ''
    title = get_title_for_file(filename)

    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    basename_wo_ext = os.path.splitext(basename)[0]
    eng_m4a = os.path.join(dirname, 'temp', basename_wo_ext + '_eng.m4a')
    plain_m4a = os.path.join(dirname, 'temp', basename_wo_ext + '.m4a')
    cmd = 'ffmpeg ^\
        -y ^\
        -i "%s" ^\
        -map 0:a -c:a copy -movflags +faststart ^\
        %s ^\
        -metadata artist="Bhakti Sudhir Goswami" ^\
        -metadata title="%s" ^\
        -metadata album="Gupta Govardhan 2016" ^\
        "%s" ^\
        -map 0:a -c:a copy -movflags +faststart ^\
        "%s"' % (filename, ss_arg, title, eng_m4a, plain_m4a)
    print(cmd)
    p = os.popen(cmd, 'r')
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
