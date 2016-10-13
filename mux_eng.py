import sys
import os
import subprocess

import meta
import upload_video

def usage_and_exit():
    print("""mux eng/rus audio files into a Goswami Maharaj's video
usage: mux "yyyy-mm-dd goswamimj.mp4"
(or drag and drop the file onto me)""")
    exit()

def mux_eng(filename):
    skip_time = meta.get_ss_arg_for_file(filename)
    if skip_time:
        ss_args = ['-ss', skip_time]
    else:
        ss_args = []

    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    basename_wo_ext = os.path.splitext(basename)[0]
    eng_mp4 = os.path.join(dirname, 'temp', basename_wo_ext + '_eng.mp4')

    cmd = ['ffmpeg', '-y',
           '-i', filename,
           '-c', 'copy',
           '-movflags', '+faststart']
    cmd += meta.ffmpeg_meta_args(filename)
    cmd += ss_args
    cmd += [eng_mp4]
    subprocess.run(cmd, check=True)

    cmd = ['python', 'C:\\Users\\ashutosh\\Dropbox\\Reference\\S\scripts\\upload_video.py',
           '--file', eng_mp4]
    subprocess.run(cmd, check=True)


def main():
    try:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print('file "%s" not found' % filename)
            print('')
            usage_and_exit()
        mux_eng(filename)
    except IndexError:
        usage_and_exit()

if __name__ == '__main__':
    main()
