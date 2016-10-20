import os
import time


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


def open(filename, mode):
    retry_count = 0
    while True:
        try:
            return __builtins__.open(filename, mode)
        except PermissionError:
            if retry_count == 50:
                raise
            retry_count += 1
            time.sleep(0.01)
