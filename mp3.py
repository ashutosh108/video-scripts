import sys
import os
import subprocess

import meta

def usage_and_exit():
    print("""echo mp3: encode rus audio track for Goswami Maharaj's video from wav to mp3
echo usage: mp3 "yyyy-mm-dd goswamimj.mp4"
echo (or drag and drop the file onto me)""")
    exit()


def mp3(filename):
    rus_mixdown_wav = meta.get_work_filename(filename, ' rus_mixdown.wav')

    cmd = ['ffmpeg', '-y',
           '-i', rus_mixdown_wav,
           '-codec:a', 'mp3',
           '-b:a', '128k']
    cmd += meta.get_ss_args(filename)
    cmd += meta.ffmpeg_meta_args_rus_stereo(filename)
    cmd += [meta.get_work_filename(filename, ' rus_stereo.mp3')]
    p_rus_stereo = subprocess.Popen(cmd)

    cmd = ['ffmpeg', '-y',
           '-i', rus_mixdown_wav,
           '-codec:a', 'mp3',
           '-ac', '1',
           '-b:a', '96k']
    cmd += meta.get_ss_args(filename)
    cmd += meta.ffmpeg_meta_args_rus_mono(filename)
    cmd += [meta.get_work_filename(filename, ' rus_mono.mp3')]
    p_rus_mono = subprocess.Popen(cmd)

    cmd = ['ffmpeg', '-y',
           '-i', meta.get_work_filename(filename, '.m4a'),
           '-ac', '1',
           '-codec:a', 'mp3', '-b:a', '96k']
    cmd += meta.get_ss_args(filename)
    cmd += meta.ffmpeg_meta_args(filename)
    cmd += [meta.get_work_filename(filename, ' eng.mp3')]
    p_eng = subprocess.Popen(cmd)

    p_rus_stereo.communicate()
    p_rus_mono.communicate()
    p_eng.communicate()

def main():
    try:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print('file "%s" not found' % filename)
            print('')
            usage_and_exit()
        mp3(filename)
    except IndexError:
        usage_and_exit()

if __name__ == '__main__':
    main()
