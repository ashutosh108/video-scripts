import unittest
import os
import contextlib
import io

import ffmpegrunner
import win


class TestFfmpegrunner(unittest.TestCase):

    def prepare_files(self, source, target):
        files_dir = os.path.join(os.path.dirname(__file__), 'files')
        mp4_filename = os.path.join(files_dir, source)
        self.assertTrue(os.path.exists(mp4_filename), 'source file ' + source + ' must exist')
        mkv_filename = os.path.join(files_dir, target)
        try:
            win.unlink(mkv_filename)
        except FileNotFoundError:
            pass
        self.assertFalse(
            os.path.exists(mkv_filename),
            'dest file ' + target + ' must NOT exist before ffmpeg')
        return mp4_filename, mkv_filename

    def test_run_is_silent(self):
        (mp4_filename, mkv_filename) = self.prepare_files('one_sec.mp4', 'test_ffmpegrunner_tmp.mkv')
        cmd = ['ffmpeg', '-i', mp4_filename, '-c', 'copy', mkv_filename]
        out = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(out):
            with contextlib.redirect_stderr(stderr):
                ffmpegrunner.run(cmd)
        self.assertNotEqual(
            0,
            os.stat(mkv_filename).st_size,
            'dest file test_ffmpegrunner_tmp.mkv must not be empty after ffmpeg')
        win.unlink(mkv_filename)
        self.assertEqual('', out.getvalue(), 'should not print anything during ffmpeg run')
        self.assertEqual('', stderr.getvalue(), 'should not print anything to stderr during ffmpeg run')

    def test_run_does_call_callback(self):
        (mp4_filename, mkv_filename) = self.prepare_files('one_sec.mp4', 'test_ffmpegrunner_tmp.mkv')
        cmd = ['ffmpeg', '-i', mp4_filename, '-c', 'copy', mkv_filename]
        callback_count = 0
        callback_total = None
        callback_last_curr = None

        def callback(curr, total):
            nonlocal callback_count, callback_total, callback_last_curr
            callback_count += 1
            if callback_total is None:
                callback_total = total
            else:
                self.assertEqual(callback_total, total, '"total" must be the same in all callbacks')
            if callback_last_curr is None:
                callback_last_curr = curr
            else:
                self.assertLessEqual(callback_last_curr, curr, 'curr should be growing monotonously')
                callback_last_curr = curr
        out = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(out):
            with contextlib.redirect_stderr(stderr):
                ffmpegrunner.run(cmd, callback)
        self.assertNotEqual(
            0,
            os.stat(mkv_filename).st_size,
            'dest file test_ffmpegrunner_tmp.mkv must not be empty after ffmpeg')
        win.unlink(mkv_filename)
        self.assertEqual('', out.getvalue(), 'should not print anything during ffmpeg run')
        self.assertEqual('', stderr.getvalue(), 'should not print anything to stderr during ffmpeg run')
        self.assertNotEqual(0, callback_count, 'callback should have been called at least once')
