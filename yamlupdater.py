"""
Warning: supports only limited subset of yaml (basically, simple array of values).
This is the easiest way to keep the original formatting intact which is important for us.
"""
import filelock
import contextlib
import tempfile
import os
import ruamel.yaml


def set(filename, key, value):
    with filelock.FileLock(filename + '.lock'):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                old = ruamel.yaml.round_trip_load(f)
        except FileNotFoundError:
            old = {}
        old.update({key: value})
        with atomic_open(filename) as f:
            yaml_str = ruamel.yaml.round_trip_dump(old, indent=4)
            f.write(yaml_str.encode('UTF-8'))
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
