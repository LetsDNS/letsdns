import os
import subprocess
from tempfile import NamedTemporaryFile
from unittest import TestCase

from letsdns.configuration import Config
from letsdns.configuration import is_truthy


class Test(TestCase):
    def test_dump(self):
        conf = Config()
        conf.init()
        f = NamedTemporaryFile(mode='wt', delete=False)
        conf.dump(f)
        f.close()
        diff = subprocess.run(['diff', 'dump-expected', f.name])
        os.unlink(f.name)
        self.assertEqual(0, diff.returncode)

    def test_is_truthy1(self):
        self.assertFalse(is_truthy('false'))

    def test_is_truthy2(self):
        self.assertFalse(is_truthy(None))

    def test_is_truthy3(self):
        self.assertTrue(is_truthy('YES'))

    def test_is_truthy4(self):
        self.assertTrue(is_truthy(1))
