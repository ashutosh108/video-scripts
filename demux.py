import os
import subprocess
import sys

import meta


def usage_and_exit():
    print("""demux: extract (demux) english AAC audio from Goswami Maharaj's video into separate m4a file
usage: demux "yyyy-mm-dd goswamimj.mp4"
(or drag and drop the file onto me)""")
    exit()


def demux_file(orig_mp4_filename: str) -> None:
    cmd = ['ffmpeg',
           '-y',
           '-i', orig_mp4_filename,
           '-c:a', 'copy', '-vn',
           meta.get_work_filename(orig_mp4_filename, '.m4a')]
    subprocess.run(cmd, check=True)


def main():
    try:
        orig_mp4_filename = sys.argv[1]
        if not os.path.isfile(orig_mp4_filename):
            print('file "%s" not found' % orig_mp4_filename)
            print('')
            usage_and_exit()
        demux_file(orig_mp4_filename)
    except IndexError:
        usage_and_exit()

if __name__ == '__main__':
    main()
