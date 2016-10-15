import yaml
import filelock


def set(filename, key, value):
    with filelock.FileLock(filename + '.lock'):
        try:
            f = open(filename, 'r+')
            d = yaml.load(f)
        except FileNotFoundError:
            d = None
            f = open(filename, 'w')
        if d is None:
            d = {}
        d[key] = value
        f.seek(0)
        f.truncate()
        yaml.dump(d, f)
