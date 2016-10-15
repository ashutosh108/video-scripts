from unittest import TestCase
import os
import yaml
import yamlupdater


class TestYamlUpdater(TestCase):
    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__), 'files', 'TestYamlUpdater.yml')

    def tearDown(self):
        os.unlink(self.filename)

    def test_set(self):
        with open(self.filename, 'w') as f:
            f.write('key: 0')
        yamlupdater.set(self.filename, 'key', 1)

        d2 = yaml.load(open(self.filename, 'r'))
        self.assertEqual(1, d2['key'])

    def test_set_saves_without_braces(self):
        with open(self.filename, 'w') as f:
            f.write('key: 1')
        yamlupdater.set(self.filename, 'key', 0)
        with open(self.filename, 'r') as f:
            self.assertEqual('key: 0\n', f.read())

    def test_set_keeps_strings_unescaped(self):
        with open(self.filename, 'w') as f:
            f.write('title_eng: Test title')
        yamlupdater.set(self.filename, 'key', 1)
        with open(self.filename, 'r') as f:
            self.assertEqual('title_eng: Test title\nkey: 1\n', f.read())

    def test_set_keeps_text_blocks_same_pipe_type(self):
        with open(self.filename, 'w') as f:
            f.write('descr_eng: |\n    - line1\n    - line2\n')
        yamlupdater.set(self.filename, 'key', 1)
        with open(self.filename, 'r') as f:
            self.assertEqual('descr_eng: |\n    - line1\n    - line2\nkey: 1\n', f.read())
