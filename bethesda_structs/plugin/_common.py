# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import os
import io
import abc
from typing import (TypeVar, Generic, List, Generator,)

from construct import (Struct, Container,)
from multidict import (CIMultiDict,)


T_BasePlugin = TypeVar('BasePlugin')


class BasePlugin(abc.ABC, Generic[T_BasePlugin]):

    record_registry = CIMultiDict()
    form_registry = CIMultiDict()

    def __init__(self, content: bytes, masters: List[T_BasePlugin]=None):
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

    def iter_records(
        self, record_type: str=None, include_header: bool=False
    ) -> Generator[Container, None, None]:
        if include_header:
            if isinstance(record_type, str) and record_type.lower() != 'hedr':
                pass
            else:
                yield self.header

        for group in self.groups:
            for record in group.records:
                if isinstance(record_type, str) and \
                        record.type.lower() != record_type.lower():
                    continue
                yield record
