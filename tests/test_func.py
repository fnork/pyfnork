import unittest

from tempfile import TemporaryDirectory
from pyfnork import func


class TestStringMethods(unittest.TestCase):

    def test_simple(self):
        with TemporaryDirectory() as temp_dir:
            call_count = 0

            @func.persistent_cache(location=temp_dir)
            def foo(arg, kwarg=None):
                nonlocal call_count
                call_count += 1
                return [arg, kwarg]
            self.assertEqual(call_count, 0)
            self.assertEqual(foo('kossa'), ['kossa', None])
            self.assertEqual(call_count, 1)
            self.assertEqual(foo('kossa'), ['kossa', None])
            self.assertEqual(call_count, 1)


if __name__ == '__main__':
    unittest.main()
