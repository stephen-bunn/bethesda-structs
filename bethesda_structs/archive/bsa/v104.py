# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

from typing import Generator
from pathlib import PureWindowsPath

from construct import (
    If,
    Array,
    Bytes,
    Struct,
    VarInt,
    CString,
    Int32ul,
    Int64ul,
    FlagsEnum,
    Compressed,
    GreedyBytes,
    PascalString
)

from .._common import ArchiveFile, BaseArchive


class BSAArchive(BaseArchive):
    """BSAArchive for version 104 of BSA files.

    Note:
        - Used by Skyrim
    """

    SIZE_MASK = 0x3fffffff
    COMPRESSED_MASK = 0xc0000000

    header_struct = Struct(
        "magic" / Bytes(4),
        "version" / Int32ul,
        "directory_offset" / Int32ul,
        "archive_flags"
        / FlagsEnum(
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
        "file_flags"
        / FlagsEnum(
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
        "hash" / Int64ul, "file_count" / Int32ul, "name_offset" / Int32ul
    )
    file_record_struct = Struct("hash" / Int64ul, "size" / Int32ul, "offset" / Int32ul)
    directory_block_struct = Struct(
        "name"
        / If(
            lambda this: this._.header.archive_flags.directories_named,
            PascalString(VarInt, "utf8"),
        ),
        "file_records"
        / Array(
            lambda this: this._.directory_records[this._._index].file_count,
            file_record_struct,
        ),
    )
    archive_struct = Struct(
        "header" / header_struct,
        "directory_records"
        / Array(lambda this: this.header.directory_count, directory_record_struct),
        "directory_blocks"
        / Array(lambda this: this.header.directory_count, directory_block_struct),
        "file_names"
        / If(
            lambda this: this.header.archive_flags.files_named,
            Array(lambda this: this.header.file_count, CString("utf8")),
        ),
    )

    @classmethod
    def can_handle(cls, filepath: str) -> bool:
        header = cls.header_struct.parse_file(filepath)
        return header.magic == b"BSA\x00" and header.version == 104

    def iter_files(self) -> Generator[ArchiveFile, None, None]:
        """Iterates over the parsed data and yeilds instances of `ArchiveFile`

        Raises:
            ValueError: If a filename cannot be determined for a specific file record

        Yeilds:
            ArchiveFile: An file contained within the archive
        """

        # locally define file structures
        uncompressed_file_struct = Struct(
            "data" / GreedyBytes
        ) * "Structure for uncompressed files"
        compressed_file_struct = Struct(
            "original_size" / Int32ul, "data" / Compressed(GreedyBytes, "zlib")
        ) * "Structure for compressed files"

        file_index = 0
        file_struct = uncompressed_file_struct
        if self.container.header.archive_flags.files_compressed:
            file_struct = compressed_file_struct

        for (directory_record, directory_block) in zip(
            self.container.directory_records, self.container.directory_blocks
        ):
            # get directory path from directory block
            directory_path = PureWindowsPath(directory_block.name[:-1])
            for file_record in directory_block.file_records:
                # choose compressed file structure if compressed mask is set
                if file_record.size > 0 and (
                    self.container.header.archive_flags.files_compressed
                    != bool(file_record.size & self.COMPRESSED_MASK)
                ):
                    file_struct = compressed_file_struct

                file_container = file_struct.parse(
                    self.content[
                        file_record.offset:(
                            file_record.offset + (file_record.size & self.SIZE_MASK)
                        )
                    ]
                )

                if len(self.container.file_names) <= 0:
                    raise ValueError(
                        (
                            f"no available file name for file {file_container!r}, "
                            f"maybe corrupt file or unsupported format"
                        )
                    )

                archived_path = directory_path.joinpath(
                    self.container.file_names[file_index]
                )
                file_index += 1

                yield ArchiveFile(filepath=archived_path, data=file_container.data)
