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
            with open(filename, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = []
        has_line = False
        new_lines = []
        for line in lines:
            if line.startswith(key + ':'):
                line = key + ': ' + str(value) + '\n'
                has_line = True
            new_lines.append(line)
        if new_lines:
            # append new line at the end if it's missing
            if new_lines[-1][-1] != '\n':
                new_lines[-1] += '\n'
        if not has_line:
            new_lines.append(key + ': ' + str(value) + '\n')
        with atomic_open(filename) as f:
            f.write(''.join(new_lines))
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
        with os.fdopen(fd, 'w') as f:
            yield f
        os.replace(filename, filename_bak)
        os.replace(tmp_name, filename)
        tmp_name = None
    finally:
        with contextlib.suppress(Exception):
            if tmp_name:
                os.unlink(tmp_name)
            os.unlink(filename_bak)
