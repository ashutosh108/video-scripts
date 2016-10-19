import sys
import os
import subprocess
import multiprocessing

import meta
import upload_video


def usage_and_exit():
    print("""echo mux eng/rus audio files into a Goswami Maharaj's video
echo usage: mux "yyyy-mm-dd goswamimj.mp4"
echo (or drag and drop the file onto me)""")
    exit()


def create_and_upload_rus_files(orig_mp4_filename):
    p1 = multiprocessing.Process(target=_create_and_upload_rus_mono_mp4, args=(orig_mp4_filename,))
    p1.start()
    p2 = multiprocessing.Process(target=_create_and_upload_rus_stereo_mp4, args=(orig_mp4_filename,))
    p2.start()
    p3 = multiprocessing.Process(target=_create_mp3_rus_mono, args=(orig_mp4_filename,))
    p3.start()
    p4 = multiprocessing.Process(target=_create_mp3_rus_stereo, args=(orig_mp4_filename,))
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()


def _create_and_upload_rus_stereo_mp4(orig_mp4_filename):
    rus_stereo_mp4_filename = meta.get_work_filename(orig_mp4_filename, ' rus_stereo.mp4')
    cmd = ['D:\\video\\GoswamiMj-videos\\ffmpeg-hi8-heaac.exe', '-y',
           '-i', orig_mp4_filename,
           '-i', meta.get_work_filename(orig_mp4_filename, ' rus_mixdown.wav'),
           '-map', '0:v',
           '-c:v', 'copy',
           '-map', '1:a',
           '-c:a:0', 'libfdk_aac',
           '-b:a', '384k',
           '-metadata:s:a:0', 'language=rus',
           '-movflags', '+faststart']
    cmd += meta.ffmpeg_meta_args_ru_stereo(orig_mp4_filename)
    cmd += meta.get_ss_args(orig_mp4_filename)
    cmd += [rus_stereo_mp4_filename]
    subprocess.run(cmd, check=True)

    title = meta.get_youtube_title_ru_stereo(orig_mp4_filename)
    description = meta.get_youtube_description_ru_stereo(orig_mp4_filename)
    upload_video.upload(rus_stereo_mp4_filename, title=title, description=description)


def _create_and_upload_rus_mono_mp4(orig_mp4_filename):
    rus_mono_m4a = meta.get_work_filename(orig_mp4_filename, ' rus_mono.m4a')
    cmd = ['D:\\video\\GoswamiMj-videos\\ffmpeg-hi8-heaac.exe', '-y',
           '-i', meta.get_work_filename(orig_mp4_filename, ' rus_mixdown.wav'),
           '-c:a', 'libfdk_aac', '-ac', '1', '-b:a', '128k',
           '-metadata:s:a:0', 'language=rus']
    cmd += meta.ffmpeg_meta_args_ru_mono(orig_mp4_filename)
    cmd += [rus_mono_m4a]
    subprocess.run(cmd, check=True)

    rus_mono_mp4_filename = meta.get_work_filename(orig_mp4_filename, ' rus_mono.mp4')
    cmd = ['ffmpeg', '-y',
           '-i', orig_mp4_filename,
           '-i', rus_mono_m4a,
           '-map', '0:v',
           '-map', '1:a',
           '-c', 'copy',
           '-movflags', '+faststart']
    cmd += meta.ffmpeg_meta_args_ru_mono(orig_mp4_filename)
    cmd += meta.get_ss_args(orig_mp4_filename)
    cmd += [rus_mono_mp4_filename]
    subprocess.run(cmd, check=True)

    title = meta.get_youtube_title_ru_mono(orig_mp4_filename)
    description = meta.get_youtube_description_ru_mono(orig_mp4_filename)
    upload_video.upload(rus_mono_mp4_filename, title=title, description=description)


def _create_mp3_rus_mono(filename):
    cmd = ['ffmpeg', '-y',
           '-i', (meta.get_work_filename(filename, ' rus_mixdown.wav')),
           '-codec:a', 'mp3',
           '-ac', '1',
           '-b:a', '96k']
    cmd += meta.get_ss_args(filename)
    cmd += meta.ffmpeg_meta_args_ru_mono(filename)
    cmd += [meta.get_work_filename(filename, ' rus_mono.mp3')]
    subprocess.run(cmd, check=True)


def _create_mp3_rus_stereo(filename):
    cmd = ['ffmpeg', '-y',
           '-i', (meta.get_work_filename(filename, ' rus_mixdown.wav')),
           '-codec:a', 'mp3',
           '-b:a', '128k']
    cmd += meta.get_ss_args(filename)
    cmd += meta.ffmpeg_meta_args_ru_stereo(filename)
    cmd += [meta.get_work_filename(filename, ' rus_stereo.mp3')]
    subprocess.run(cmd, check=True)

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
