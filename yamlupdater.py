"""
Warning: supports only limited subset of yaml (basically, simple array of values).
This is the easiest way to keep the original formatting intact which is important for us.
"""
import filelock
import contextlib
import tempfile
import os


def set(filename, key, value):
    with filelock.FileLock(filename + '.lock'):
        try:
            with open(filename, 'rb') as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = []
        has_line = False
        new_lines = []
        for line in lines:
            if line.startswith(key.encode('utf-8') + b':'):
                line = key.encode('utf-8') + b': ' + str(value).encode('utf-8') + b'\n'
                has_line = True
            new_lines.append(line)
        if new_lines:
            # append new line at the end if it's missing
            # we use '10' because for byte-strings [] returns int, not string
            if new_lines[-1][-1] != 10:
                new_lines[-1] += b'\n'
        if not has_line:
            new_lines.append(key.encode('utf-8') + b': ' + str(value).encode('utf-8') + b'\n')
        with atomic_open(filename) as f:
            f.write(b''.join(new_lines))
            f.flush()
            os.fsync(f.fileno())


@contextlib.contextmanager
def atomic_open(filename):
    tmp_name = None
    filename_bak = filename + '.bak'
    try:
        file_dir = os.path.dirname(filename)
        prefix = os.path.basename(filename) + '.'
        fd, tmp_name = tempfile.mkstemp(prefix=prefix, dir=file_dir)
        with os.fdopen(fd, 'wb') as f:
            yield f
        try:
            os.replace(filename, filename_bak)
        except FileNotFoundError:
            # the original file might not even exist yet and then it's OK
            pass
        os.replace(tmp_name, filename)
        tmp_name = None
    finally:
        with contextlib.suppress(Exception):
            if tmp_name:
                os.unlink(tmp_name)
            os.unlink(filename_bak)
