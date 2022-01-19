from unittest import TestCase

from letsdns.configuration import is_truthy


class Test(TestCase):
    def test_is_truthy1(self):
        self.assertFalse(is_truthy('false'))

    def test_is_truthy2(self):
        self.assertFalse(is_truthy(None))

    def test_is_truthy3(self):
        self.assertTrue(is_truthy('YES'))

    def test_is_truthy4(self):
        self.assertTrue(is_truthy(1))
