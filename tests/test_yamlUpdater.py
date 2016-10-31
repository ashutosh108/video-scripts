from unittest import TestCase
import os
import yaml
import yamlupdater
import sys
import inspect

import win


class TestYamlUpdater(TestCase):
    DEBUG = False

    @staticmethod
    def begin():
        if TestYamlUpdater.DEBUG:
            caller = inspect.stack()[1][3]
            print('{%s...' % caller, end='')
            sys.stdout.flush()

    @staticmethod
    def mark(msg):
        if TestYamlUpdater.DEBUG:
            caller = inspect.stack()[1][3]
            print('%s.%s' % (caller, msg), end='')
            sys.stdout.flush()

    @staticmethod
    def end():
        if TestYamlUpdater.DEBUG:
            caller = inspect.stack()[1][3]
            print(' %s}' % caller)
            sys.stdout.flush()

    def setUp(self):
        self.begin()
        self.filename = os.path.join(os.path.dirname(__file__), 'files', 'TestYamlUpdater.yml')
        self.f = win.open(self.filename, 'w', encoding='utf-8')
        self.end()

    def tearDown(self):
        self.begin()
        self.f.close()
        win.unlink(self.filename)
        self.end()

    def test_set(self):
        self.begin()
        self.f.write('key: 0')
        self.f.close()
        self.mark('init completed...')
        yamlupdater.set(self.filename, 'key', 1)
        self.mark('yaml update completed...')

        self.f = open(self.filename, 'r')
        d2 = yaml.load(self.f)
        self.assertEqual(1, d2['key'])
        self.end()

    def test_set_saves_without_braces(self):
        self.begin()
        self.f.write('key: 1')
        self.f.close()
        self.mark('file init completed...')
        yamlupdater.set(self.filename, 'key', 0)
        self.mark('yaml update completed...')
        self.f = open(self.filename, 'r')
        self.assertEqual('key: 0\n', self.f.read())
        self.end()

    def test_set_keeps_strings_unescaped(self):
        self.begin()
        self.f.write('title_en: Test title')
        self.f.close()
        self.mark('file init completed...')
        yamlupdater.set(self.filename, 'key', 1)
        self.mark('yaml update completed...')
        self.f = open(self.filename, 'r')
        self.assertEqual('title_en: Test title\nkey: 1\n', self.f.read())
        self.end()

    def test_set_keeps_text_blocks_same_pipe_type(self):
        self.begin()
        self.f.write('descr_en: |\n    - line1\n    - line2\n')
        self.f.close()
        self.mark('file init completed...')
        yamlupdater.set(self.filename, 'key', 1)
        self.mark('yaml update completed...')
        self.f = open(self.filename, 'r')
        self.assertEqual('descr_en: |\n    - line1\n    - line2\nkey: 1\n', self.f.read())
        self.end()

    def test_set_works_with_chars_outside_cp1251(self):
        # U+2600 is \xE2\x98\x80 in utf-8
        # and \x98 is not defined for windows-1251 encoding
        # so it's a good char to test
        self.f.write('key1: \u2600')
        self.f.close()

        yamlupdater.set(self.filename, 'key2', 2)

        self.f = open(self.filename, 'r', encoding='utf-8')
        self.assertEqual('key1: \u2600\nkey2: 2\n', self.f.read())
