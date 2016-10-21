import sys
import os
import multiprocessing
import progressbar
import colorama

import meta
import upload_video
import ffmpegrunner


def usage_and_exit():
    print("""mux en/ru audio files into a Goswami Maharaj's video
usage: mux "yyyy-mm-dd goswamimj.mp4"
(or drag and drop the file onto me)""")
    exit()


def orig(orig_mp4_filename):
    colorama.init()
    print('\x1b[2J', end='')  # clear screen
    """Prepare all files in original language: m4a, mp4, mp3"""
    lang = meta.get_lang(orig_mp4_filename)

    # first we cut m4a and mp4 version sequentially because these are
    # IO-bound tasks on the single drive, so running them in parallel
    # doesn't make much sense.
    _cut_orig_m4a(orig_mp4_filename, lang, 0)
    cut_video_filename = meta.get_work_filename(orig_mp4_filename, ' ' + lang + '.mkv')
    _cut_orig_mp4(orig_mp4_filename, cut_video_filename, lang, 1)

    # And now we run two long-running tasks (uploading to youtube
    # and encoding mp3) in parallel

    p_upload_orig_mp4 = multiprocessing.Process(target=_upload_orig_mp4, args=(orig_mp4_filename, cut_video_filename, lang, 2))
    p_upload_orig_mp4.start()

    p_encode_orig_mp3 = multiprocessing.Process(target=_encode_orig_mp3, args=(orig_mp4_filename, lang, 3))
    p_encode_orig_mp3.start()

    p_upload_orig_mp4.join()
    p_encode_orig_mp3.join()


def _cut_orig_mp4(orig_mp4_filename, cut_mp4_filename, lang, line):
    cmd = ['ffmpeg', '-y',
           '-i', orig_mp4_filename,
           '-c', 'copy']
    cmd += meta.ffmpeg_meta_args(orig_mp4_filename, lang)
    cmd += meta.get_ss_args(orig_mp4_filename)
    cmd += [cut_mp4_filename]
    _run_ffmpeg_at_line(cmd, line)


def _upload_orig_mp4(orig_mp4_filename, cut_video_filename, lang, line):
    colorama.init()
    bar = None

    def update(curr, max):
        nonlocal bar, line
        cursor_down(line)
        if bar is None:
            bar = progressbar.ProgressBar(max_value=max)
        bar.update(curr)
        cursor_up(line)

    title = meta.get_youtube_title(orig_mp4_filename, lang)
    description = meta.get_youtube_description(orig_mp4_filename, lang)
    upload_video.upload(cut_video_filename, title=title, description=description, lang=lang, update=update)
    cursor_down(line)
    bar.finish()
    cursor_up(line + 1)


def _cut_orig_m4a(orig_mp4_filename, lang, line):
    cmd = ['ffmpeg', '-y',
           '-i', orig_mp4_filename]
    cmd += meta.ffmpeg_meta_args(orig_mp4_filename, lang)
    cmd += meta.get_ss_args(orig_mp4_filename)
    cmd += ['-c:a', 'copy', '-vn',
            meta.get_work_filename(orig_mp4_filename, ' ' + lang + '.m4a')]
    _run_ffmpeg_at_line(cmd, line)


def cursor_down(line):
    print('\x1b[%dB' % line, end='')


def cursor_up(line):
    print('\x1b[%dA' % line, end='')


def _run_ffmpeg_at_line(cmd, line):
    bar = None

    def update(curr, max):
        nonlocal bar, line
        cursor_down(line)
        if bar is None:
            bar = progressbar.ProgressBar(max_value=max)
        bar.update(curr)
        cursor_up(line)

    ffmpegrunner.run(cmd, update)
    cursor_down(line)
    bar.finish()
    cursor_up(line + 1)


def _encode_orig_mp3(orig_mp4_filename, lang, line):
    colorama.init()
    cmd = ['ffmpeg', '-y',
           '-i', orig_mp4_filename,
           '-ac', '1',
           '-codec:a', 'mp3', '-b:a', '96k']
    cmd += meta.get_ss_args(orig_mp4_filename)
    cmd += meta.ffmpeg_meta_args(orig_mp4_filename, lang)
    cmd += [meta.get_work_filename(orig_mp4_filename, ' ' + lang + '.mp3')]
    _run_ffmpeg_at_line(cmd, line)


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
