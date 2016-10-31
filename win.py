import os
import time
import builtins


def unlink(filename):
    retry_count = 0
    while True:
        try:
            os.unlink(filename)
        except PermissionError:
            if retry_count == 50:
                raise
            retry_count += 1
            time.sleep(0.01)
        else:
            break


def open(filename, mode, **kwargs):
    retry_count = 0
    while True:
        try:
            return builtins.open(filename, mode, **kwargs)
        except PermissionError:
            if retry_count == 50:
                raise
            retry_count += 1
            time.sleep(0.01)
