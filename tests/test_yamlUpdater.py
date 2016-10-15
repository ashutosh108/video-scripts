from unittest import TestCase
import os
import yaml
import yamlupdater


class TestYamlUpdater(TestCase):
    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__), 'files', 'TestYamlUpdater.yml')

    def test_set(self):
        with open(self.filename, 'w') as f:
            f.write('key: 0')
        yamlupdater.set(self.filename, 'key', 1)

        d2 = yaml.load(open(self.filename, 'r'))
        self.assertEqual(1, d2['key'])
        os.unlink(self.filename)
