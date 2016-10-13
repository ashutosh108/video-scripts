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
    cmd = ['ffmpeg',
           '-y',
           '-i', filename]
    cmd += meta.ffmpeg_meta_args(filename)
    cmd += meta.get_ss_args(filename)
    cmd += ['-c:a', 'copy', '-vn',
            meta.get_work_filename(filename, '_eng.m4a'),
            '-c:a', 'copy', '-vn',
            meta.get_work_filename(filename, '.m4a')]
    print(repr(cmd))
    subprocess.run(cmd, check=True)


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
