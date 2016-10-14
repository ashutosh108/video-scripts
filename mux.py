import sys
import os
import subprocess

import meta

def usage_and_exit():
    print("""echo mux eng/rus audio files into a Goswami Maharaj's video
echo usage: mux "yyyy-mm-dd goswamimj.mp4"
echo (or drag and drop the file onto me)""")
    exit()


def mux(filename):
    subprocess.run(
        'start C:\\Users\\ashutosh\\Dropbox\\Reference\\S\\scripts\\mux_rus_stereo.cmd "%s"' % filename,
        shell=True, check=True)

    rus_mono_m4a = meta.get_work_filename(filename, ' rus_mono.m4a')
    rus_mono_mp4 = meta.get_work_filename(filename, ' rus_mono.mp4')
    cmd = ['D:\\video\\GoswamiMj-videos\\ffmpeg-hi8-heaac.exe', '-y',
           '-i', meta.get_work_filename(filename, ' rus_mixdown.wav'),
           '-c:a', 'libfdk_aac', '-ac', '1', '-b:a', '128k',
           '-metadata:s:a:0', 'language=rus']
    cmd += meta.ffmpeg_meta_args_rus_mono(filename)
    cmd += [rus_mono_m4a]
    subprocess.run(cmd, check=True)

    cmd = ['ffmpeg', '-y',
           '-i', filename,
           '-i', rus_mono_m4a,
           '-map', '0:v',
           '-map', '1:a',
           '-c', 'copy',
           '-movflags', '+faststart']
    cmd += meta.ffmpeg_meta_args_rus_mono(filename)
    cmd += meta.get_ss_args(filename)
    cmd += [rus_mono_mp4]
    subprocess.run(cmd, check=True)

    cmd = ['python', 'C:\\Users\\ashutosh\\Dropbox\\Reference\\S\scripts\\upload_video.py',
           '--file', rus_mono_mp4]
    subprocess.run(cmd, check=True)


def main():
    try:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print('file "%s" not found' % filename)
            print('')
            usage_and_exit()
        mux(filename)
    except IndexError:
        usage_and_exit()

if __name__ == '__main__':
    main()
