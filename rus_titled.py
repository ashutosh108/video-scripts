import sys
import os
import subprocess
import multiprocessing

import ffmpeg
import meta
import my_youtube
import title


def usage_and_exit():
    print("""echo mux en/ru audio files into a Goswami Maharaj's video
echo usage: mux "yyyy-mm-dd goswamimj.mp4"
echo (or drag and drop the file onto me)""")
    exit()


def create_and_upload_ru_files(orig_mp4_filename):
    ts_title_filename, ts_rest_filename = title.make_ts_files_with_title_and_rest(orig_mp4_filename, 'ru')
    p1 = multiprocessing.Process(target=_create_and_upload_ru_mono_video, args=(orig_mp4_filename, ts_title_filename, ts_rest_filename, ))
    p1.start()
    p2 = multiprocessing.Process(target=_create_and_upload_ru_stereo_video, args=(orig_mp4_filename, ts_title_filename, ts_rest_filename, ))
    p2.start()
    p3 = multiprocessing.Process(target=_create_mp3_ru_mono, args=(orig_mp4_filename,))
    p3.start()
    p4 = multiprocessing.Process(target=_create_mp3_ru_stereo, args=(orig_mp4_filename,))
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()


def _create_and_upload_ru_stereo_video(orig_mp4_filename, ts_title_filename, ts_rest_filename):
    concat_str = _get_concat_args(ts_title_filename, ts_rest_filename)
    ru_stereo_titled_mp4_filename = meta.get_work_filename(orig_mp4_filename, ' ru_stereo titled.mp4')
    cmd = ['D:\\video\\GoswamiMj-videos\\ffmpeg-hi8-heaac.exe', '-y',
           '-i', concat_str]
    cmd += ffmpeg.ss_args(orig_mp4_filename)
    cmd += ['-i', meta.get_work_filename(orig_mp4_filename, ' ru_mixdown.wav')]
    cmd += ['-c:v', 'copy']
    cmd += ['-c:a', 'libfdk_aac']
    # cmd += ['-ac', '1']  # mono
    cmd += ffmpeg.to_args(orig_mp4_filename)
    cmd += [ru_stereo_titled_mp4_filename]
    os.chdir('D:\\video\GoswamiMj-videos')
    subprocess.run(cmd, check=True)
    os.chdir('C:\\Users\\ashutosh\\Dropbox\\Reference\S\scripts')

    title = meta.get_youtube_title_ru_stereo(orig_mp4_filename)
    description = meta.get_youtube_description_ru_stereo(orig_mp4_filename)
    youtube_id = my_youtube.upload(ru_stereo_titled_mp4_filename, title=title, description=description, lang='ru')
    meta.update_yaml(orig_mp4_filename, 'youtube_id_rus_stereo', youtube_id)


def _get_concat_args(filename1, filename2):
    arg1 = 'temp\\' + os.path.basename(filename1)
    arg2 = 'temp\\' + os.path.basename(filename2)
    return 'concat:' + arg1 + '|' + arg2


def _create_and_upload_ru_mono_video(orig_mp4_filename, ts_title_filename, ts_rest_filename):
    concat_str = _get_concat_args(ts_title_filename, ts_rest_filename)
    ru_mono_titled_mp4_filename = meta.get_work_filename(orig_mp4_filename, ' ru_mono titled.mp4')
    cmd = ['D:\\video\\GoswamiMj-videos\\ffmpeg-hi8-heaac.exe', '-y',
           '-i', concat_str]
    cmd += ffmpeg.ss_args(orig_mp4_filename)
    cmd += ['-i', meta.get_work_filename(orig_mp4_filename, ' ru_mixdown.wav')]
    cmd += ['-c:v', 'copy']
    cmd += ['-c:a', 'libfdk_aac']
    cmd += ['-ac', '1']  # mono
    cmd += ffmpeg.to_args(orig_mp4_filename)
    cmd += [ru_mono_titled_mp4_filename]
    os.chdir('D:\\video\GoswamiMj-videos')
    subprocess.run(cmd, check=True)
    os.chdir('C:\\Users\\ashutosh\\Dropbox\\Reference\S\scripts')

    title = meta.get_youtube_title_ru_mono(orig_mp4_filename)
    description = meta.get_youtube_description_ru_mono(orig_mp4_filename)
    youtube_id = my_youtube.upload(ru_mono_titled_mp4_filename, title=title, description=description, lang='ru')
    meta.update_yaml(orig_mp4_filename, 'youtube_id_rus_mono', youtube_id)


def _create_mp3_ru_mono(filename):
    cmd = ['ffmpeg', '-y',
           '-i', (meta.get_work_filename(filename, ' ru_mixdown.wav')),
           '-codec:a', 'mp3',
           '-ac', '1',
           '-b:a', '96k']
    cmd += ffmpeg.ss_args(filename)
    cmd += ffmpeg.to_args(filename)
    cmd += ffmpeg.meta_args_ru_mono(filename)
    cmd += [meta.get_work_filename(filename, ' ru_mono.mp3')]
    subprocess.run(cmd, check=True)


def _create_mp3_ru_stereo(filename):
    cmd = ['ffmpeg', '-y',
           '-i', (meta.get_work_filename(filename, ' ru_mixdown.wav')),
           '-codec:a', 'mp3',
           '-b:a', '128k']
    cmd += ffmpeg.ss_args(filename)
    cmd += ffmpeg.to_args(filename)
    cmd += ffmpeg.meta_args_ru_stereo(filename)
    cmd += [meta.get_work_filename(filename, ' ru_stereo.mp3')]
    subprocess.run(cmd, check=True)


def main():
    try:
        orig_mp4_filename = sys.argv[1]
        if not os.path.isfile(orig_mp4_filename):
            print('file "%s" not found' % orig_mp4_filename)
            print('')
            usage_and_exit()
        create_and_upload_ru_files(orig_mp4_filename)
    except IndexError:
        usage_and_exit()

if __name__ == '__main__':
    main()
