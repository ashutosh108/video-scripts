import subprocess
import re


def run(cmd, callback=None):
    curr = 0
    total = None
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    for line in p.stderr:
        m = re.search(r'Duration: (\d+([:.]\d+)+)', line)
        if m:
            total = time_to_secs(m.group(1))
            if callback is not None:
                callback(curr, total)

        m = re.search('time=(\d+([:.]\d+)+)', line)
        if m:
            curr = time_to_secs(m.group(1))
            if callback is not None:
                callback(curr, total)

    p.communicate()


regex = re.compile(r'(?P<hours>\d+):'
                   r'(?P<min>\d+):'
                   r'(?P<sec>\d+\.\d+)')


def time_to_secs(time):
    m = re.match(regex, time)
    parts = m.groupdict()
    return int(parts['hours'])*3600 + int(parts['min'])*60 + float(parts['sec'])
