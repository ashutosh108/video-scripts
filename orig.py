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


def orig(orig_mp4_filename):
    """Prepare all files in original language: m4a, mp4, mp3"""
    cut_mp4_filename = _create_orig_mp4(orig_mp4_filename)
    _upload_orig_mp4(orig_mp4_filename, cut_mp4_filename)
    _create_orig_m4a(orig_mp4_filename)
    _create_orig_mp3(orig_mp4_filename)


def _create_orig_mp4(orig_mp4_filename):
    cut_mp4_filename = meta.get_work_filename(orig_mp4_filename, ' eng.mp4')
    cmd = ['ffmpeg', '-y',
           '-i', orig_mp4_filename,
           '-c', 'copy',
           '-movflags', '+faststart']
    cmd += meta.ffmpeg_meta_args(orig_mp4_filename)
    cmd += meta.get_ss_args(orig_mp4_filename)
    cmd += [cut_mp4_filename]
    subprocess.run(cmd, check=True)
    return cut_mp4_filename


def _upload_orig_mp4(orig_mp4_filename, cut_mp4_filename):
    title = meta.get_youtube_title_eng(orig_mp4_filename)
    description = meta.get_youtube_description_eng(orig_mp4_filename)
    upload_video.upload(cut_mp4_filename, title=title, description=description)


def _create_orig_m4a(orig_mp4_filename):
    cmd = ['ffmpeg', '-y',
           '-i', orig_mp4_filename]
    cmd += meta.ffmpeg_meta_args(orig_mp4_filename)
    cmd += meta.get_ss_args(orig_mp4_filename)
    cmd += ['-c:a', 'copy', '-vn',
            meta.get_work_filename(orig_mp4_filename, ' eng.m4a')]
    subprocess.run(cmd, check=True)


def _create_orig_mp3(orig_mp4_filename):
    cmd = ['ffmpeg', '-y',
           '-i', orig_mp4_filename,
           '-ac', '1',
           '-codec:a', 'mp3', '-b:a', '96k']
    cmd += meta.get_ss_args(orig_mp4_filename)
    cmd += meta.ffmpeg_meta_args(orig_mp4_filename)
    cmd += [meta.get_work_filename(orig_mp4_filename, ' eng.mp3')]
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
