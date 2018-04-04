# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import os
from typing import Callable
from pathlib import Path, PureWindowsPath

from construct import (
    Array,
    Bytes,
    Const,
    Int8ul,
    Struct,
    Switch,
    VarInt,
    Int16ul,
    Int32ul,
    Int64ul,
    Pointer,
    GreedyBytes,
    PaddedString,
    PascalString,
)

from ._common import BaseArchive


class BA2Archive(BaseArchive):

    header_struct = Struct(
        "magic" / Const(b"BTDX"),
        "version" / Int32ul,
        "type" / PaddedString(4, "utf8"),
        "file_count" / Int32ul,
        "name_table_offset" / Int64ul,
    )

    general_struct = Struct(
        "name_hash" / Int32ul,
        "extension" / PaddedString(4, "utf8"),
        "directory_hash" / Int32ul,
        "_unknown_0" / Int32ul,  # potentially flags (unknown meanings)
        "offset" / Int64ul,
        "packed_size" / Int32ul,
        "full_size" / Int32ul,
        "_unknown_1" / Int32ul,
    )

    texture_chunk_struct = Struct(
        "offset" / Int64ul,
        "packed_size" / Int32ul,
        "full_size" / Int32ul,
        "start_mipmap" / Int16ul,
        "end_mipmap" / Int16ul,
        "_unknown_0" / Int32ul,
    )

    texture_struct = Struct(
        "name_hash" / Int32ul,
        "extension" / PaddedString(4, "utf8"),
        "folder_hash" / Int32ul,
        "_unknown_0" / Bytes(1),
        "chunk_count" / Int8ul,
        "chunk_size" / Int16ul,
        "height" / Int16ul,
        "width" / Int16ul,
        "mipmap_count" / Int8ul,
        "format" / Bytes(1),
        "_unknown_1" / Bytes(2),
        "texture_chunks" / Array(lambda this: this.mipmap_count, texture_chunk_struct),
    )

    archive_struct = Struct(
        "header" / header_struct,
        "file_records" / Array(
            lambda this: this.header.file_count,
            Switch(
                lambda this: this.header.type,
                {"GNRL": general_struct, "DX10": texture_struct},
            ),
        ),
        "name_table" / Pointer(
            lambda this: this.header.name_table_offset,
            Array(lambda this: this.header.file_count, PascalString(Int16ul, "utf8")),
        ),
    )

    @classmethod
    def can_handle(cls, filepath: str) -> bool:
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"no such file {filepath!r} exists")

        header = cls.header_struct.parse_file(filepath)
        return header.magic == b"BTDX" and header.version in (1,) and header.type in (
            "GNRL", "DX10"
        )

    def _extract_general(
        self, to_dir: Path, progress_hook: Callable[[int, int, str], None] = None
    ):
        for (file_record, file_path) in zip(
            self.container.file_records, self.container.name_table
        ):
            to_path = to_dir.joinpath(PureWindowsPath(file_path))
            if not to_path.parent.is_dir():
                to_path.parent.mkdir(parents=True)
            with to_path.open("wb") as stream:
                stream.write(
                    self.content[
                        file_record.offset:(file_record.offset + file_record.full_size)
                    ]
                )

    def extract(
        self, to_dir: str, progress_hook: Callable[[int, int, str], None] = None
    ):
        to_dir = Path(to_dir)
        if not to_dir.is_dir():
            raise NotADirectoryError(f"no such directory {to_dir.as_posix()!r} exists")

        if self.container.header.type.upper() == "GNRL":
            self._extract_general(to_dir, progress_hook=progress_hook)
