# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import os
from pathlib import Path

from construct import (
    Probe, Struct, Const, If, IfThenElse,
    Array, GreedyRange, GreedyBytes, Compressed,
    PascalString, CString, PaddedString, FlagsEnum,
    VarInt, Int64ul, Int32ul, Int8ul,
)
from ._common import BaseArchive


class BSAArchive(BaseArchive):

    archive_struct = Struct(
        "header" / Struct(
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
            "directory_count" / Int32ul,
            "file_count" / Int32ul,
            "directory_names_length" / Int32ul,
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
        ),
        "directory_records" / Array(
            lambda this: this.header.directory_count,
            Struct(
                "name_hash" / Int64ul,
                "file_count" / Int32ul,
                "_unknown_0" / Int32ul,
                "file_offset" / Int32ul,
                "_unknown_1" / Int32ul,
            )
        ),
        "file_blocks" / Array(
            lambda this: this.header.directory_count,
            Struct(
                "name" / If(
                    lambda this: this._.header.flags.has_names_for_directories,
                    PascalString(VarInt, 'utf8'),
                ),
                "records" / Array(
                    lambda this: this._.directory_records[
                        this._._index
                    ].file_count,
                    Struct(
                        "name_hash" / Int64ul,
                        "size" / Int32ul,
                        "offset" / Int32ul
                    )
                )
            )
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

        to_dir = Path(to_dir)
        for (directory_record, file_block) in zip(
            self.container.directory_records,
            self.container.file_blocks
        ):
            directory_fragment = Path(file_block.name[:-1].replace('\\', '/'))
            for (file_idx, file_record) in enumerate(file_block.records):
                if self.container.header.flags.files_compressed:
                    file_struct = Struct(
                        "name" / If(
                            self.container.header.flags.files_compressed,
                            CString('utf8')
                        ),
                        "original_size" / Int32ul,
                        "data" / Compressed(GreedyBytes, 'zlib')
                    )
                else:
                    file_struct = Struct(
                        "name" / If(
                            self.container.header.flags.files_compressed,
                            CString('utf8')
                        ),
                        "data" / GreedyBytes
                    )

                file_container = file_struct.parse(self.content[
                    file_record.offset:(file_record.offset + file_record.size)
                ])
                if file_container.name is not None:
                    file_path = Path(file_container.name.replace('\\', '/'))
                    directory_fragment = file_path.parent
                    path_fragment = file_path.name
                if self.container.file_names is not None:
                    path_fragment = self.container.file_names[file_idx]

                with to_dir.joinpath(
                    directory_fragment,
                    path_fragment
                ).open('wb') as stream:
                    stream.write(file_container.data)
