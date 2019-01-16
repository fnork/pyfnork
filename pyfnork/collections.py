import builtins
import ctypes
import os
import pickle
import shutil
import time

from .util import persistent_hash
from collections.abc import MutableMapping


class _RestrictedUnpickler(pickle.Unpickler):

    _SAFE_BUILTINS = {
        'range',
        'complex',
        'set',
        'frozenset',
        'slice',
    }

    def find_class(self, module, name):
        # Only allow safe classes from builtins.
        if module == "builtins" and name in self._SAFE_BUILTINS:
            return getattr(builtins, name)
        # Forbid everything else.
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" %
                                     (module, name))


class PersistentDict(MutableMapping):

    _MAGIC_NUMBER = 'pypm'
    _CURRENT_VERSION = 1

    def __init__(self, identifier,
                 location='.persistent_map', encoding='UTF-8'):
        self.__identifier = identifier
        self._dir_path = os.path.join(location, identifier)
        self._encoding = encoding
        self._linesep = self._encode(os.linesep)
        self._create_dir()

    def __getitem__(self, key):
        path = self._get_path(key)
        try:
            return self._get_key_item(path)['value']
        except LookupError:
            raise KeyError(key)

    def __setitem__(self, key, value, timestamp=time.time()):
        path = self._get_path(key)
        with open(path, 'wb+') as f:
            header = (str(x) for x in (
                self._MAGIC_NUMBER,
                self._CURRENT_VERSION))
            f.write(self._encode('|'.join(header)))
            f.write(self._linesep)

            data = {
                'value': value,
                'key': key,
                'timestamp': timestamp,
                }
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    def __delitem__(self, key):
        path = self._get_path(key)
        if not os.path.isfile(path):
            raise KeyError(key)
        os.remove(path)

    def __iter__(self):
        return (self._get_key_item(path)['key'] for path in self._iter_files())

    def __len__(self):
        return len(list(self._iter_files()))

    def __eq__(self, other):
        return self._dir_path == other._dir_path

    setdefault = MutableMapping.setdefault
    update = MutableMapping.update
    pop = MutableMapping.pop
    keys = MutableMapping.keys
    values = MutableMapping.values
    items = MutableMapping.items
    __ne__ = MutableMapping.__ne__
    set = __setitem__

    def clear(self):
        shutil.rmtree(self._dir_path)
        self._create_dir()

    def purge(self, before):
        purged = 0
        for path in self._iter_files():
            data = self._get_key_item(path)
            if data['timestamp'] >= before:
                continue
            os.remove(path)
            purged += 1
        return purged

    def _get_path(self, *key):
        filename = f'{persistent_hash(key)}.dat'
        return os.path.join(self._dir_path, filename)

    def _create_dir(self):
        if not os.path.exists(self._dir_path):
            os.makedirs(self._dir_path)

    def _get_key_item(self, path):
        if not os.path.isfile(path):
            raise KeyError(path)

        with open(path, 'rb') as file:
            parts = self._decode(file.readline()).strip().split('|')
            if len(parts) < 2:
                raise KeyError(path)

            (magic, version) = parts
            if magic != self._MAGIC_NUMBER:
                raise KeyError(path)

            if version != '1':
                raise KeyError(path)

            return _RestrictedUnpickler(file).load()

    def _iter_files(self):
        gen = os.listdir(self._dir_path)
        return (os.path.join(self._dir_path, file) for file in gen)

    def _encode(self, s):
        return s.encode(self._encoding)

    def _decode(self, s):
        return s.decode(self._encoding)
