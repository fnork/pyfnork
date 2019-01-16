import os
import pickle
import random
import unittest

from tempfile import TemporaryDirectory

from pyfnork.collections import PersistentDict


class TestStringMethods(unittest.TestCase):

    def unique(self):
        return f'unique-{random.randint(0, 0xffffffff)}'

    def test_init(self):
        with TemporaryDirectory() as temp_dir:
            pm = PersistentDict(self.unique(), location=temp_dir)
            self.assertIsNotNone(pm)

    def test_get_set_single_key(self):
        with TemporaryDirectory() as temp_dir:
            pm = PersistentDict(self.unique(), location=temp_dir)
            pm[1] = 'test'
            self.assertEqual(pm[1], 'test')
            self.assertEqual(pm.get(1), 'test')
            self.assertNotEqual(pm[1], 'foo')

    def test_get_set_multiple_key(self):
        with TemporaryDirectory() as temp_dir:
            pm = PersistentDict(self.unique(), location=temp_dir)
            pm[1, 'key', 'something'] = 'test'
            self.assertEqual(pm[1, 'key', 'something'], 'test')
            self.assertEqual(pm.get((1, 'key', 'something')), 'test')
            self.assertNotEqual(pm[1, 'key', 'something'], 'different')
            self.assertTrue((1, 'key', 'something') in pm)
            self.assertFalse((1, 'key') in pm)

    def test_false_true(self):
        with TemporaryDirectory() as temp_dir:
            pm = PersistentDict(self.unique(), location=temp_dir)
            self.assertFalse(pm)
            pm[1] = 'test'
            self.assertTrue(pm)

    def test_len(self):
        with TemporaryDirectory() as temp_dir:
            pm = PersistentDict(self.unique(), location=temp_dir)
            self.assertEqual(len(pm), 0)
            for i in range(10):
                pm[i] = 'test'
                self.assertEqual(len(pm), i + 1)
            pm[1] = 'foo'
            self.assertEqual(len(pm), 10)
            pm[1] = 'bar'
            self.assertEqual(len(pm), 10)

    def test_in(self):
        with TemporaryDirectory() as temp_dir:
            pm = PersistentDict(self.unique(), location=temp_dir)
            self.assertFalse('test' in pm)
            pm['test'] = 42
            self.assertTrue('test' in pm)
            pm['test', 4, 'foo'] = 42
            self.assertTrue(('test', 4, 'foo') in pm)

    def test_delete(self):
        with TemporaryDirectory() as temp_dir:
            key = 'test'
            pm = PersistentDict(self.unique(), location=temp_dir)
            file_path = pm._get_path(key)
            self.assertFalse(os.path.exists(file_path))
            self.assertFalse(key in pm)
            pm['test'] = 'some value'
            self.assertTrue(os.path.exists(file_path))
            self.assertTrue(key in pm)
            del(pm['test'])
            self.assertFalse(os.path.exists(file_path))
            self.assertFalse(key in pm)

    def test_clear(self):
        with TemporaryDirectory() as temp_dir:
            pm = PersistentDict(self.unique(), location=temp_dir)
            pm.clear()
            self.assertFalse(pm)
            pm['key'] = 'value'
            self.assertTrue(pm)
            pm.clear()
            self.assertFalse(pm)

    def test_equals(self):
        with TemporaryDirectory() as temp_dir_1:
            same_1 = self.unique()
            pm_1_a = PersistentDict(same_1, location=temp_dir_1)
            pm_1_b = PersistentDict(same_1, location=temp_dir_1)
            pm_1_c = PersistentDict('different', location=temp_dir_1)
            with TemporaryDirectory() as temp_dir_2:
                same_2 = self.unique()
                pm_2_a = PersistentDict(same_2, location=temp_dir_2)
                pm_2_b = PersistentDict(same_2, location=temp_dir_2)
                self.assertEqual(pm_1_a, pm_1_b)
                self.assertEqual(pm_2_a, pm_2_b)
                self.assertNotEqual(pm_1_b, pm_1_c)
                self.assertNotEqual(pm_1_a, pm_2_a)

    def test_purge(self):
        now = 1547678156.4535859
        with TemporaryDirectory() as temp_dir:
            pm = PersistentDict(self.unique(), location=temp_dir)
            pm.set('old', 'old value', timestamp=now - 1)
            pm.set('same', 'same value', timestamp=now)
            pm.set('new', 'new value', timestamp=now + 1)
            pm.purge(now)
            self.assertFalse('old' in pm)
            self.assertTrue('same' in pm)
            self.assertTrue('new' in pm)

    def test_unsafe(self):
        with TemporaryDirectory() as temp_dir:
            pm = PersistentDict(self.unique(), location=temp_dir)
            pm['foo'] = complex(1, 4)
            self.assertEqual(pm['foo'], 1+4j)
            pm['bar'] = os.system
            self.assertRaises(pickle.UnpicklingError, pm.get, 'bar')


if __name__ == '__main__':
    unittest.main()
