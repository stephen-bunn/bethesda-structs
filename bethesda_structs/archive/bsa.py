# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://choosealicense.com/licenses/mit/>

from typing import Generator
from pathlib import PureWindowsPath

import lz4.frame
from construct import (
    If,
    Array,
    Bytes,
    Struct,
    VarInt,
    Adapter,
    CString,
    Int32ul,
    Int64ul,
    Container,
    FlagsEnum,
    Compressed,
    IfThenElse,
    GreedyBytes,
    PascalString,
)

from ._common import ArchiveFile, BaseArchive


class LZ4CompressedAdapter(Adapter):
    """An adapter for LZ4 compressed data.

    Note:
        v105 BSA's utilize `LZ4 <https://github.com/lz4/lz4>`_ compression instead of
        `zlib <https://zlib.net/>`_.
    """

    def _decode(self, obj: bytes, context: Container, path: str) -> bytes:
        """Decompresses the given bytes.

        Args:
            obj (bytes): The LZ4 compressed bytes
            context (Container): The context container
            path (str): The construct path

        Returns:
            bytes: The resulting decompressed bytes
        """
        return lz4.frame.decompress(obj)

    def _encode(self, obj: bytes, context: Container, path: str) -> bytes:
        """Compresses the given bytes.

        Args:
            obj (bytes): The uncompressed bytes
            context (Container): The context container
            path (str): The construct path

        Returns:
            bytes: The resulting compressed bytes
        """
        return lz4.frame.compress(obj)


class BSAArchive(BaseArchive):
    """Archive type for BSA files.

    BSA stands for "Bethesda ? Archive".
    These archives are compressed meshes, textures and other static resources that can
    be loaded as a single file instead of a directory of files (loose files).

    There are currently 4 versions of BSA:
        - ???: Morrowind
        - 103: Oblivion
        - 104: Fallout 3, Fallout: New Vegas, and Skyrim
        - 105: Skyrim: Special Edition

    Note:
        BSA archives to not read the file data on initialization.
        Header's, records and names are read in and files are built during
        :func:`~BSAArchive.iter_files`.

    **Credit:**
        - `BAE <https://github.com/jonwd7/bae>`_
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
    """The structure of BSA headers.

    Returns:
        :class:`~construct.core.Struct`: The structure of BSA headers
    """

    directory_record_struct = Struct(
        "hash" / Int64ul,
        "file_count" / Int32ul,
        "_unknown_0" / If(lambda this: this._.header.version >= 105, Int32ul),
        "name_offset"
        / IfThenElse(lambda this: this._.header.version >= 105, Int64ul, Int32ul),
    )
    """The structure of directory records.

    Returns:
        :class:`~construct.core.Struct`: The structure of directory records
    """

    file_record_struct = Struct("hash" / Int64ul, "size" / Int32ul, "offset" / Int32ul)
    """The structure of file records.

    Returns:
        :class:`~construct.core.Struct`: The structure of file records
    """

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
    """The structure of directory blocks.

    Returns:
        :class:`~construct.core.Struct`: The structure of directory blocks
    """

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
    """The **partial** structure of BSA archives.

    Return:
        :class:`~construct.core.Struct`: The **partial** structure of BSA archives
    """

    @property
    def uncompressed_file_struct(self) -> Struct:
        """The uncompressed file structure for uncompressed files.

        Returns:
            :class:`~construct.core.Struct`: The uncompressed file structure for
            uncompressed files.
        """
        return Struct("data" / GreedyBytes)

    @property
    def compressed_file_struct(self) -> Struct:
        """The compressed file structure for compressed files.

        Returns:
            :class:`~construct.core.Struct`: The compressed file structure for
            compressed files.
        """
        return Struct(
            "original_size" / Int32ul,
            "data"
            / IfThenElse(
                self.container.header.version >= 105,
                LZ4CompressedAdapter(GreedyBytes),
                Compressed(GreedyBytes, "zlib"),
            ),
        )

    @classmethod
    def can_handle(cls, filepath: str) -> bool:
        """Determines if a given file can be handled by the current archive.

        Args:
            filepath (str): The filepath to check if can be handled
        """

        header = cls.header_struct.parse_file(filepath)
        return header.magic == b"BSA\x00" and header.version in (103, 104, 105)

    def iter_files(self) -> Generator[ArchiveFile, None, None]:
        """Iterates over the parsed data and yields instances of :class:`.ArchiveFile`.

        Yields:
            :class:`.ArchiveFile`: An file contained within the archive
        """

        file_index = 0
        file_struct = self.uncompressed_file_struct
        if self.container.header.archive_flags.files_compressed:
            file_struct = self.compressed_file_struct

        for directory_block in self.container.directory_blocks:
            # get directory path from directory block
            directory_path = PureWindowsPath(directory_block.name[:-1])
            for file_record in directory_block.file_records:
                # choose the compressed file structure if compressed mask is set
                if (
                    file_record.size > 0
                    and (
                        self.container.header.archive_flags.files_compressed
                        != bool(file_record.size & self.COMPRESSED_MASK)
                    )
                ):
                    file_struct = self.compressed_file_struct

                file_container = file_struct.parse(
                    self.content[
                        file_record.offset:(
                            file_record.offset + (file_record.size & self.SIZE_MASK)
                        )
                    ]
                )

                yield ArchiveFile(
                    filepath=directory_path.joinpath(
                        self.container.file_names[file_index]
                    ),
                    data=file_container.data,
                )

                file_index += 1
