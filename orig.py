import sys
import os
import multiprocessing
import progressbar
import colorama

import ffmpeg
import meta
import my_youtube
import ffmpegrunner
import title


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
    _cut_orig_m4a(orig_mp4_filename, lang, line=0)
    cut_video_filename = meta.get_work_filename(orig_mp4_filename, ' ' + lang + '.mkv')
    _cut_orig_mp4(orig_mp4_filename, cut_video_filename, lang, line=1)

    # And now we run two long-running tasks (uploading to youtube
    # and encoding mp3) in parallel

    p_upload_orig_mp4 = multiprocessing.Process(
        target=_upload_orig_mp4,
        kwargs={'orig_mp4_filename': orig_mp4_filename, 'cut_video_filename': cut_video_filename, 'lang': lang, 'line': 2})
    p_upload_orig_mp4.start()

    p_encode_orig_mp3 = multiprocessing.Process(
        target=_encode_orig_mp3,
        kwargs={'orig_mp4_filename': orig_mp4_filename, 'lang': lang, 'line': 3})
    p_encode_orig_mp3.start()

    p_upload_orig_mp4.join()
    p_encode_orig_mp3.join()


def _cut_orig_mp4(orig_mp4_filename, cut_mp4_filename, lang, line):
    title.make_mp4_with_title(orig_mp4_filename, lang)
    cmd = ['ffmpeg', '-y',
           '-i', orig_mp4_filename,
           '-c', 'copy']
    cmd += ffmpeg.meta_args(orig_mp4_filename, lang)
    cmd += ffmpeg.ss_args(orig_mp4_filename)
    cmd += ffmpeg.to_args(orig_mp4_filename)
    cmd += [cut_mp4_filename]
    _run_ffmpeg_at_line(cmd, line, 'mkv')


def _upload_orig_mp4(orig_mp4_filename, cut_video_filename, lang, line):
    def run(callback):
        title = meta.get_youtube_title(orig_mp4_filename, lang)
        description = meta.get_youtube_description_orig(orig_mp4_filename, lang)
        youtube_id = my_youtube.upload(
            cut_video_filename,
            title=title,
            description=description,
            lang=lang,
            update=callback)
        meta.update_yaml(orig_mp4_filename, 'youtube_id_orig', youtube_id)
    run_with_progressbar(line, run, 'upload')


def run_with_progressbar(line, run, name):
    colorama.init()
    bar = None

    def callback(curr_value, max_value):
        nonlocal bar, line
        cursor_down(line)
        if bar is None:
            bar = progressbar.ProgressBar(
                widgets=[name, ': ', progressbar.Bar(), ' ', progressbar.ETA()],
                max_value=max_value)
        bar.update(curr_value)
        cursor_up(line)

    run(callback)

    cursor_down(line)
    bar.finish()
    cursor_up(line + 1)


def _cut_orig_m4a(orig_mp4_filename, lang, line):
    cmd = ['ffmpeg', '-y',
           '-i', orig_mp4_filename]
    cmd += ffmpeg.meta_args(orig_mp4_filename, lang)
    cmd += ffmpeg.ss_args(orig_mp4_filename)
    cmd += ffmpeg.to_args(orig_mp4_filename)
    cmd += ['-c:a', 'copy', '-vn',
            meta.get_work_filename(orig_mp4_filename, ' ' + lang + '.m4a')]
    _run_ffmpeg_at_line(cmd, line, 'm4a')


def cursor_down(line):
    print('\x1b[%dB' % line, end='')


def cursor_up(line):
    print('\x1b[%dA' % line, end='')


def _run_ffmpeg_at_line(cmd, line, name):
    def run(callback):
        ffmpegrunner.run(cmd, callback)
    run_with_progressbar(line, run, name)


def _encode_orig_mp3(orig_mp4_filename, lang, line):
    cmd = ['ffmpeg', '-y',
           '-i', orig_mp4_filename,
           '-ac', '1',
           '-codec:a', 'mp3', '-b:a', '96k']
    cmd += ffmpeg.ss_args(orig_mp4_filename)
    cmd += ffmpeg.to_args(orig_mp4_filename)
    cmd += ffmpeg.meta_args(orig_mp4_filename, lang)
    cmd += [meta.get_work_filename(orig_mp4_filename, ' ' + lang + '.mp3')]
    _run_ffmpeg_at_line(cmd, line, 'mp3')


def main():
    try:
        orig_mp4_filename = sys.argv[1]
        if not os.path.isfile(orig_mp4_filename):
            print('file "%s" not found' % orig_mp4_filename)
            print('')
            usage_and_exit()
        orig(orig_mp4_filename)
    except (IndexError, KeyboardInterrupt):
        usage_and_exit()

if __name__ == '__main__':
    main()
