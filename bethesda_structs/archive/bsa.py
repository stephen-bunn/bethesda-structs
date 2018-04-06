# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import os
from typing import Callable
from pathlib import Path, PureWindowsPath

import lz4.frame
from construct import (
    If,
    Array,
    Bytes,
    Probe,
    Union,
    Struct,
    Switch,
    VarInt,
    Adapter,
    CString,
    Int32ul,
    Int64ul,
    Embedded,
    FlagsEnum,
    Compressed,
    IfThenElse,
    GreedyBytes,
    PascalString,
    EmbeddedSwitch,
    ExprSymmetricAdapter
)

from ._common import BaseArchive


class LZ4CompressionAdapter(Adapter):

    def _decode(self, obj, context, path):
        return lz4.frame.decompress(obj)

    def _encode(self, obj, context, path):
        return lz4.frame.compress(obj)


class BSAArchive(BaseArchive):
    """The archive for BSA file structures.

    Based on the structures implemented by `BAE`_.

    Note:
        This archive does *not* extract the file structures from the given
        content during parsing. Instead, this is handled during extraction due to the
        nature of how the file offsets need to be chosen from the file and directory
        records with a bit more logic than the base structure should handle.

    .. _BAE:
        https://github.com/jonwd7/bae
    """

    OB_VERSION = 0x67
    FO3_VERSION = 0x68
    SSE_VERSION = 0x69

    SIZE_MASK = 0x3fffffff
    COMPRESSED_MASK = 0xc0000000

    header_struct = Struct(
        "magic" / Bytes(4),
        "version" / Int32ul,
        "directory_offset" / Int32ul,
        "archive_flags" / FlagsEnum(
            Int32ul,
            directories_named=0x001,
            files_named=0x002,
            files_compressed=0x004,
            _unknown_0=0x008,
            _unknown_1=0x010,
            _unknown_2=0x020,
            xbox360_archive=0x040,
            files_prefixed=0x100,
            _unknown_4=0x200,
            _unknown_5=0x400,
        ),
        "directory_count" / Int32ul,
        "file_count" / Int32ul,
        "directory_names_length" / Int32ul,
        "file_names_length" / Int32ul,
        "file_flags" / FlagsEnum(
            Int32ul,
            nif=0x001,
            dds=0x002,
            xml=0x004,
            wav=0x008,
            mp3=0x010,
            txt=0x020,
            html=0x020,
            bat=0x020,
            scc=0x020,
            spt=0x040,
            tex=0x080,
            fnt=0x080,
            ctl=0x100,
        ),
    )

    directory_record_struct = Struct(
        "hash" / Int64ul * "Directory hash",
        "file_count" / Int32ul * "Number of files in directory",
        "_unknown_0" / If(
            lambda this: this._.header.version != BSAArchive.OB_VERSION,
            Int32ul
        ) * "Unknown",
        "name_offset" / IfThenElse(
            lambda this: this._.header.version == BSAArchive.OB_VERSION,
            Int32ul,
            Int64ul,
        ) * "Directory name offset",
    )

    file_record_struct = Struct(
        "hash" / Int64ul * "Filename hash",
        "size" / Int32ul * "Raw file size flags",
        "offset" / Int32ul * "Raw file data offset",
    )

    directory_block_struct = Struct(
        "name" / If(
            lambda this: this._.header.archive_flags.directories_named,
            PascalString(VarInt, "utf8"),
        ) * "Directory name",
        "file_records" / Array(
            lambda this: this._.directory_records[this._._index].file_count,
            file_record_struct,
        ) * "File records within the directory",
    )

    archive_struct = Struct(
        "header" / header_struct * "Archive header",
        "directory_records" / Array(
            lambda this: this.header.directory_count,
            directory_record_struct
        ) * "Array of directory records",
        "directory_blocks" / Array(
            lambda this: this.header.directory_count,
            directory_block_struct
        ) * "Array of file blocks",
        "file_names" / If(
            lambda this: this.header.archive_flags.files_named,
            Array(lambda this: this.header.file_count, CString("utf8")),
        ) * "Array of file names",
    )

    @classmethod
    def can_handle(cls, filepath: str) -> bool:
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"no such file {filepath!r} exists")

        header = Struct("magic" / Bytes(4), "version" / Int32ul).parse_file(filepath)
        return header.magic == b"BSA\x00" and header.version in (
            cls.OB_VERSION, cls.FO3_VERSION, cls.SSE_VERSION
        )

    def extract(
        self, to_dir: str, progress_hook: Callable[[int, int, str], None] = None
    ):
        if not os.path.isdir(to_dir):
            raise NotADirectoryError(f"no such directory {to_dir!r} exists")

        to_dir = Path(to_dir)
        file_index = 0
        total_size = sum(
            record.size & self.SIZE_MASK
            for block in self.container.directory_blocks
            for record in block.file_records
        )
        current_size = 0

        compressed_file_struct = Struct(
            "name" / If(
                self.container.header.version != self.OB_VERSION
                and self.container.header.archive_flags.files_prefixed,
                CString('utf8')
            ),
            "original_size" / Int32ul,
            "data" / IfThenElse(
                self.container.header.version != self.SSE_VERSION,
                Compressed(GreedyBytes, "zlib"),
                LZ4CompressionAdapter(GreedyBytes)
            )
        ) * "File structure for compressed files"
        uncompressed_file_struct = Struct(
            "name" / If(
                self.container.header.version != self.OB_VERSION
                and self.container.header.archive_flags.files_prefixed,
                CString("utf8"),
            ),
            "data" / GreedyBytes
        ) * "File structure for uncompressed files"

        file_struct = uncompressed_file_struct
        if self.container.header.archive_flags.files_compressed:
            file_struct = compressed_file_struct

        for (directory_record, directory_block) in zip(
            self.container.directory_records, self.container.directory_blocks
        ):
            directory_path = to_dir
            if isinstance(directory_block.name, str):
                directory_path = directory_path.joinpath(
                    PureWindowsPath(directory_block.name[:-1])
                )

            for file_record in directory_block.file_records:
                to_path = directory_path

                if file_record.size > 0 and (
                    self.container.header.archive_flags.files_compressed != bool(
                        file_record.size & self.COMPRESSED_MASK
                    )
                ):
                    file_struct = compressed_file_struct

                # FIXME: for SSE I am encountering some kind of header which I haven't seen yet
                # And after the file content header, it doesnt even look like the data is compressed
                # no signs of zlib magic...
                # TODO: LZ4F extraction...
                file_container = file_struct.parse(
                    self.content[
                        file_record.offset:(file_record.offset + file_record.size)
                    ]
                )

                if isinstance(file_container.name, str):
                    to_path = to_dir.joinpath(PureWindowsPath(file_container.name))
                else:
                    if len(self.container.file_names) <= 0:
                        raise ValueError((
                            f"no available file name for file {file_container!r}, "
                            f"maybe corrupt file or unsuported bsa format"
                        ))

                    to_path = directory_path.joinpath(self.container.file_names[file_index])
                    file_index += 1

                if not to_path.parent.is_dir():
                    to_path.parent.mkdir(parents=True)
                with to_path.open("wb") as stream:
                    stream.write(file_container.data)
                current_size += len(file_container.data)
