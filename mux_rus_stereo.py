import sys
import os
import subprocess

import meta


def usage_and_exit():
    print("""mux_rus_stereo: mux video with russian stereo mix and upload it to youtube""")
    exit()


def mux_rus_stereo(filename):
    skip_time = meta.get_skip_time(filename)
    if skip_time:
        ss_args = ['-ss', skip_time]
    else:
        ss_args = []

    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    basename_wo_ext = os.path.splitext(basename)[0]
    rus_stereo_mp4 = os.path.join(dirname, 'temp', basename_wo_ext + '_rus_stereo.mp4')
    rus_mixdown_wav = os.path.join(dirname, 'temp', basename_wo_ext + '_rus_mixdown.wav')
    cmd = ['D:\\video\\GoswamiMj-videos\\ffmpeg-hi8-heaac.exe', '-y',
           '-i', filename,
           '-i', rus_mixdown_wav,
           '-map', '0:v',
           '-c:v', 'copy',
           '-map', '1:a',
           '-c:a:0', 'libfdk_aac',
           '-b:a', '384k',
           '-metadata:s:a:0', 'language=rus',
           '-movflags', '+faststart']
    cmd += meta.ffmpeg_meta_args_rus_stereo(filename)
    cmd += ss_args
    cmd += [rus_stereo_mp4]
    subprocess.run(cmd, check=True)

    cmd = ['python', 'C:\\Users\\ashutosh\\Dropbox\\Reference\\S\scripts\\upload_video.py',
           '--file', rus_stereo_mp4]
    subprocess.run(cmd, check=True)
pass


def main():
    try:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print('file "%s" not found' % filename)
            print('')
            usage_and_exit()
        mux_rus_stereo(filename)
    except IndexError:
        usage_and_exit()

if __name__ == '__main__':
    main()