import sys
import os
import subprocess

import meta

def usage_and_exit():
    print("""echo mux eng/rus audio files into a Goswami Maharaj's video
echo usage: mux "yyyy-mm-dd goswamimj.mp4"
echo (or drag and drop the file onto me)""")
    exit()


def create_and_upload_rus_files(orig_mp4_filename):
    _create_and_upload_rus_stereo_mp4(orig_mp4_filename)
    _create_and_upload_rus_mono_mp4(orig_mp4_filename)
    _create_mp3_rus_mono_and_stereo(orig_mp4_filename)


def _create_and_upload_rus_stereo_mp4(orig_mp4_filename):
    print('stereo start')
    subprocess.run(
        'start C:\\Users\\ashutosh\\Dropbox\\Reference\\S\\scripts\\mux_rus_stereo.cmd "%s"' % orig_mp4_filename,
        shell=True, check=True)
    print('stereo finish')


def _create_and_upload_rus_mono_mp4(orig_mp4_filename):
    rus_mono_m4a = meta.get_work_filename(orig_mp4_filename, ' rus_mono.m4a')
    rus_mono_mp4 = meta.get_work_filename(orig_mp4_filename, ' rus_mono.mp4')
    cmd = ['D:\\video\\GoswamiMj-videos\\ffmpeg-hi8-heaac.exe', '-y',
           '-i', meta.get_work_filename(orig_mp4_filename, ' rus_mixdown.wav'),
           '-c:a', 'libfdk_aac', '-ac', '1', '-b:a', '128k',
           '-metadata:s:a:0', 'language=rus']
    cmd += meta.ffmpeg_meta_args_rus_mono(orig_mp4_filename)
    cmd += [rus_mono_m4a]
    subprocess.run(cmd, check=True)

    cmd = ['ffmpeg', '-y',
           '-i', orig_mp4_filename,
           '-i', rus_mono_m4a,
           '-map', '0:v',
           '-map', '1:a',
           '-c', 'copy',
           '-movflags', '+faststart']
    cmd += meta.ffmpeg_meta_args_rus_mono(orig_mp4_filename)
    cmd += meta.get_ss_args(orig_mp4_filename)
    cmd += [rus_mono_mp4]
    subprocess.run(cmd, check=True)

    cmd = ['python', 'C:\\Users\\ashutosh\\Dropbox\\Reference\\S\scripts\\upload_video.py',
           '--file', rus_mono_mp4]
    subprocess.run(cmd, check=True)


def _create_mp3_rus_mono_and_stereo(filename):
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

    p_rus_stereo.communicate()
    p_rus_mono.communicate()

def main():
    try:
        orig_mp4_filename = sys.argv[1]
        if not os.path.isfile(orig_mp4_filename):
            print('file "%s" not found' % orig_mp4_filename)
            print('')
            usage_and_exit()
        create_and_upload_rus_files(orig_mp4_filename)
    except IndexError:
        usage_and_exit()

if __name__ == '__main__':
    main()
