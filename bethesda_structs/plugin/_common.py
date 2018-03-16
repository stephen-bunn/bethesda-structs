# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import os
import io
import abc
from typing import (TypeVar, Generic, List,)

from construct import (Struct, Container,)


T_BasePlugin = TypeVar('BasePlugin')


class BasePlugin(abc.ABC, Generic[T_BasePlugin]):

    def __init__(self, content: bytes):
        self.content = content

    @property
    def content(self) -> bytes:
        if not hasattr(self, '_content'):
            self._content = bytearray()
        return self._content

    @content.setter
    def content(self, content: bytes):
        assert isinstance(content, bytes), (
            f'content must be bytes, received {type(content)!r}'
        )
        self._content = content
        for (name, data) in self.plugin_structure.parse(content).items():
            setattr(self, name, data)

    @abc.abstractproperty
    def plugin_structure(self) -> Struct:
        raise NotImplementedError()

    @classmethod
    def from_bytes(cls, content: bytes) -> T_BasePlugin:
        return cls(content)

    @classmethod
    def from_stream(cls, stream: io.BufferedIOBase) -> T_BasePlugin:
        return cls(stream.read())

    @classmethod
    def from_file(cls, filepath: str) -> T_BasePlugin:
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"no such file {filepath!r} exists")
        with open(filepath, 'rb') as stream:
            return cls(stream.read())

    @abc.abstractclassmethod
    def can_handle(self, filepath: str) -> bool:
        raise NotImplementedError()

    def find(self, record_type: str) -> List[Container]:
        for group in self.groups:
            for record in group.records:
                if record.type == record_type:
                    yield record
