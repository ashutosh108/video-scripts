"""
Warning: supports only limited subset of yaml (basically, simple array of values).
This is the easiest way to keep the original formatting intact which is important for us.
"""
import filelock



def set(filename, key, value):
    with filelock.FileLock(filename + '.lock'):
        try:
            f = open(filename, 'r+')
            lines = f.readlines()
        except FileNotFoundError:
            lines = []
            f = open(filename, 'w')
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
        f.seek(0)
        f.truncate()
        f.write(''.join(new_lines))
