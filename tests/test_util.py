import unittest

from pyfnork.util import persistent_hash


class TestStringMethods(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(persistent_hash(), persistent_hash())
        self.assertNotEqual(persistent_hash(), '')
        self.assertNotEqual(persistent_hash(), None)

    def test_single_types_equal(self):
        self.assertEqual(persistent_hash(12), persistent_hash(12))
        self.assertEqual(persistent_hash(1.2), persistent_hash(1.2))
        self.assertEqual(persistent_hash(1+2j), persistent_hash(1+2j))
        self.assertEqual(persistent_hash(None), persistent_hash(None))
        self.assertEqual(persistent_hash(b'foo'), persistent_hash(b'foo'))
        self.assertEqual(persistent_hash('foo'), persistent_hash('foo'))
        self.assertEqual(persistent_hash(dict()), persistent_hash(dict()))
        self.assertEqual(persistent_hash(set()), persistent_hash(set()))
        self.assertEqual(persistent_hash(list()), persistent_hash(list()))
        self.assertEqual(persistent_hash(tuple()), persistent_hash(tuple()))

    def test_single_types_different(self):
        self.assertNotEqual(persistent_hash(12), persistent_hash(21))
        self.assertNotEqual(persistent_hash(1.2), persistent_hash(2.1))
        self.assertNotEqual(persistent_hash(1.0), persistent_hash(1))
        self.assertNotEqual(persistent_hash(1+2j), persistent_hash(2+1j))
        self.assertNotEqual(persistent_hash(None), persistent_hash())
        self.assertNotEqual(persistent_hash('a'), persistent_hash('ab'))
        self.assertNotEqual(persistent_hash(b'foo'), persistent_hash('foo'))

    def test_single_tuples(self):
        self.assertNotEqual(persistent_hash(tuple()), persistent_hash(set()))
        self.assertNotEqual(persistent_hash(tuple()), persistent_hash(list()))
        self.assertNotEqual(persistent_hash({}), persistent_hash({'a': None}))

    def test_single_types(self):
        self.assertNotEqual(persistent_hash(12), persistent_hash(21))
        self.assertNotEqual(persistent_hash(1.2), persistent_hash(2.1))
        self.assertNotEqual(persistent_hash(1.0), persistent_hash(1))
        self.assertNotEqual(persistent_hash(1+2j), persistent_hash(2+1j))
        self.assertNotEqual(persistent_hash('a'), persistent_hash('b'))
        self.assertNotEqual(persistent_hash(tuple()), persistent_hash(set()))

    def test_nested_types(self):
        self.assertNotEqual(
            persistent_hash([[1], [1, 1]]),
            persistent_hash([[1, 1], 1]))
        self.assertNotEqual(
            persistent_hash([{1}]),
            persistent_hash([[1]]))
        self.assertNotEqual(
            persistent_hash([1]),
            persistent_hash([[1]]))

    def test_unsupported_types(self):
        self.assertRaises(TypeError, persistent_hash, object())
        self.assertRaises(TypeError, persistent_hash, 'a', None, object())
