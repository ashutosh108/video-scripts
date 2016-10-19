import sys
import os
import subprocess
import multiprocessing

import meta
import upload_video


def usage_and_exit():
    print("""mux en/ru audio files into a Goswami Maharaj's video
usage: mux "yyyy-mm-dd goswamimj.mp4"
(or drag and drop the file onto me)""")
    exit()


def orig(orig_mp4_filename):
    """Prepare all files in original language: m4a, mp4, mp3"""
    lang = meta.get_lang(orig_mp4_filename)

    # first we cut m4a and mp4 version sequentially because these are
    # IO-bound tasks on the single drive, so running them in parallel
    # doesn't make much sense.
    _cut_orig_m4a(orig_mp4_filename, lang)
    cut_video_filename = meta.get_work_filename(orig_mp4_filename, ' ' + lang + '.mkv')
    _cut_orig_mp4(orig_mp4_filename, cut_video_filename, lang)

    # And now we run two long-running tasks (uploading to youtube
    # and encoding mp3) in parallel

    p_upload_orig_mp4 = multiprocessing.Process(target=_upload_orig_mp4, args=(orig_mp4_filename, cut_video_filename, lang))
    p_upload_orig_mp4.start()

    p_encode_orig_mp3 = multiprocessing.Process(target=_encode_orig_mp3, args=(orig_mp4_filename, lang))
    p_encode_orig_mp3.start()

    p_upload_orig_mp4.join()
    p_encode_orig_mp3.join()


def _cut_orig_mp4(orig_mp4_filename, cut_mp4_filename, lang):
    cmd = ['ffmpeg', '-y',
           '-i', orig_mp4_filename,
           '-c', 'copy']
    cmd += meta.ffmpeg_meta_args(orig_mp4_filename, lang)
    cmd += meta.get_ss_args(orig_mp4_filename)
    cmd += [cut_mp4_filename]
    subprocess.run(cmd, check=True)


def _upload_orig_mp4(orig_mp4_filename, cut_video_filename, lang):
    title = meta.get_youtube_title(orig_mp4_filename, lang)
    description = meta.get_youtube_description(orig_mp4_filename, lang)
    upload_video.upload(cut_video_filename, title=title, description=description)


def _cut_orig_m4a(orig_mp4_filename, lang):
    cmd = ['ffmpeg', '-y',
           '-i', orig_mp4_filename]
    cmd += meta.ffmpeg_meta_args(orig_mp4_filename, lang)
    cmd += meta.get_ss_args(orig_mp4_filename)
    cmd += ['-c:a', 'copy', '-vn',
            meta.get_work_filename(orig_mp4_filename, ' ' + lang + '.m4a')]
    subprocess.run(cmd, check=True)


def _encode_orig_mp3(orig_mp4_filename, lang):
    cmd = ['ffmpeg', '-y',
           '-i', orig_mp4_filename,
           '-ac', '1',
           '-codec:a', 'mp3', '-b:a', '96k']
    cmd += meta.get_ss_args(orig_mp4_filename)
    cmd += meta.ffmpeg_meta_args(orig_mp4_filename, lang)
    cmd += [meta.get_work_filename(orig_mp4_filename, ' ' + lang + '.mp3')]
    subprocess.run(cmd, check=True)


def main():
    try:
        orig_mp4_filename = sys.argv[1]
        if not os.path.isfile(orig_mp4_filename):
            print('file "%s" not found' % orig_mp4_filename)
            print('')
            usage_and_exit()
        orig(orig_mp4_filename)
    except IndexError:
        usage_and_exit()

if __name__ == '__main__':
    main()
