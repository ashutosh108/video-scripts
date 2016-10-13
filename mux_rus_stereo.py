import sys
import os
import subprocess

import meta


def usage_and_exit():
    print("""mux_rus_stereo: mux video with russian stereo mix and upload it to youtube""")
    exit()


def mux_rus_stereo(filename):
    rus_stereo_mp4 = meta.get_work_filename(filename, '_rus_stereo.mp4')
    cmd = ['D:\\video\\GoswamiMj-videos\\ffmpeg-hi8-heaac.exe', '-y',
           '-i', filename,
           '-i', meta.get_work_filename(filename, '_rus_mixdown.wav'),
           '-map', '0:v',
           '-c:v', 'copy',
           '-map', '1:a',
           '-c:a:0', 'libfdk_aac',
           '-b:a', '384k',
           '-metadata:s:a:0', 'language=rus',
           '-movflags', '+faststart']
    cmd += meta.ffmpeg_meta_args_rus_stereo(filename)
    cmd += meta.get_ss_args(filename)
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
