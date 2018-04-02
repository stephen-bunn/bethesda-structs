# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import os

from construct import (
    Probe, Struct, Const, If, IfThenElse,
    Array, GreedyRange, GreedyBytes,
    PascalString, CString, PaddedString, FlagsEnum,
    VarInt, Int64ul, Int32ul, Int8ul,
)
from ._common import BaseArchive


class BSAArchive(BaseArchive):

    compressed_file_struct = Struct(
        "name" / If(
            lambda this: this._.header.flags.files_compressed,
            CString('utf8')
        ),
        "original_size" / Int32ul,
        "data" / GreedyBytes
    )

    file_struct = Struct(
        "name" / If(
            lambda this: this._.header.flags.files_compressed,
            CString('utf8')
        ),
        "data" / GreedyBytes
    )

    file_record_struct = Struct(
        "name_hash" / Int64ul,
        "size" / Int32ul,
        "offset" / Int32ul
    )

    file_block_struct = Struct(
        "name" / PascalString(VarInt, 'utf8'),
        "records" / Array(
            lambda this: this._.folder_records[this._._index].file_count,
            file_record_struct
        )
    )

    folder_record_struct = Struct(
        "name_hash" / Int64ul,
        "file_count" / Int32ul,
        "_unknown_0" / Int32ul,
        "file_offset" / Int32ul,
        "_unknown_1" / Int32ul,
    )

    header_struct = Struct(
        "magic" / Const(b'BSA\x00'),
        "version" / Int32ul,
        "offset" / Int32ul,
        "flags" / FlagsEnum(
            Int32ul,
            has_names_for_directories=0x001,
            has_names_for_files=0x002,
            files_compressed=0x004,
            _unknown_0=0x008,
            _unknown_1=0x010,
            _unknown_2=0x020,
            xbox360_archive=0x040,
            _unknown_3=0x100,
            _unknown_4=0x200,
            _unknown_5=0x400
        ),
        "folder_count" / Int32ul,
        "file_count" / Int32ul,
        "folder_names_length" / Int32ul,
        "file_names_length" / Int32ul,
        "file_flags" / FlagsEnum(
            Int32ul,
            meshes=0x001,
            textures=0x002,
            menus=0x004,
            sounds=0x008,
            voices=0x010,
            shaders=0x020,
            trees=0x040,
            fonts=0x080,
            miscellaneous=0x100
        )
    )

    archive_struct = Struct(
        "header" / header_struct,
        "folder_records" / Array(
            lambda this: this.header.folder_count,
            folder_record_struct
        ),
        "file_blocks" / Array(
            lambda this: this.header.folder_count,
            file_block_struct
        ),
        "file_names" / If(
            lambda this: this.header.flags.has_names_for_files,
            Array(lambda this: this.header.file_count, CString('utf8'))
        )
    )

    @classmethod
    def can_handle(cls, filepath: str) -> bool:
        header = cls.header_struct.parse_file(filepath)
        return header.bsa == b'BSA\x00' and header.version == 105

    def extract(self, to_dir: str):
        if not os.path.isdir(to_dir):
            raise NotADirectoryError(f"no such directory '{to_dir!r}' exists")
        for file_block in self.file_blocks:
            print(file_block)
            input()
