""" util.py - Additional utility functions
"""

__all__ = ['persistent_hash']

import numbers
import hashlib


def persistent_hash(*key, hash_func=hashlib.md5):
    hasher = hash_func()

    def _hash_item(item):
        if item is None:
            hasher.update(b'\x00')
            return

        hasher.update(str(type(item)).encode('UTF-8'))

        if isinstance(item, (tuple, list, set)):
            for i in item:
                _hash_item(i)

        elif isinstance(item, dict):
            for k, v in item.items():
                _hash_item(k)
                _hash_item(v)

        elif isinstance(item, bytes):
            hasher.update(item)

        elif isinstance(item, int):
            length = (item.bit_length() + 7) // 8
            hasher.update(item.to_bytes(length, byteorder='big'))

        elif isinstance(item, numbers.Number):
            _hash_item(hash(item))

        elif isinstance(item, str):
            _hash_item(item.encode('UTF-8'))

        else:
            raise TypeError(f"Unsupported type: {type(item)}")

    for item in key:
        _hash_item(item)

    return hasher.hexdigest()
