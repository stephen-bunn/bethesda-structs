# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import os
from typing import Callable
from pathlib import Path, PureWindowsPath

from construct import (
    If,
    Array,
    Bytes,
    Const,
    Probe,
    Int8ul,
    Struct,
    VarInt,
    CString,
    Int32ul,
    Int64ul,
    FlagsEnum,
    Compressed,
    IfThenElse,
    GreedyBytes,
    GreedyRange,
    PaddedString,
    PascalString,
    EmbeddedSwitch
)

from ._common import BaseArchive


class BSAArchive(BaseArchive):
    """The archive for BSA file formats.

    Note:
        This archive does *not* extract the file structures from the given
        content. This is handled during extraction due to the nature of how the file
        offsets need to be chosen from the file and directory records with a bit more
        logic than the base structure should handle.
    """
    archive_struct = Struct(
        "header" / Struct(
            "magic" / Const(b"BSA\x00"),
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
                _unknown_5=0x400,
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
                miscellaneous=0x100,
            ),
        ),
        "directory_records" / Array(
            lambda this: this.header.directory_count,
            Struct(
                "name_hash" / Int64ul,
                "file_count" / Int32ul,
                "_unknown_0" / Int32ul,
                "file_offset" / Int32ul,
                "_unknown_1" / Int32ul,
            ),
        ),
        "file_blocks" / Array(
            lambda this: this.header.directory_count,
            Struct(
                "name" / If(
                    lambda this: this._.header.flags.has_names_for_directories,
                    PascalString(VarInt, "utf8"),
                ),
                "records" / Array(
                    lambda this: this._.directory_records[this._._index].file_count,
                    Struct(
                        "name_hash" / Int64ul,
                        "size" / Int32ul,
                        "offset" / Int32ul
                    ),
                ),
            ),
        ),
        "file_names" / If(
            lambda this: this.header.flags.has_names_for_files,
            Array(
                lambda this: this.header.file_count,
                CString("utf8")
            ),
        ),
    )

    @classmethod
    def can_handle(cls, filepath: str) -> bool:
        """Determines if a given `filepath` can be handled by the archive.

        Args:
            filepath (str): The filepath to evaluate

        Raises:
            NotImplementedError: Subclasses must implement

        Returns:
            bool: True if the `filepath` can be handled, otherwise False
        """
        header = cls.header_struct.parse_file(filepath)
        return header.magic == b"BSA\x00" and header.version in (103, 104, 105)

    def extract(self, to_dir: str, progress_hook: Callable[[int, int, str], None]=None):
        """Extract the content of a BSA archive out to a given directory.

        Note:
            Progress hooks are very basic and implemented in two stages. This means
            that you will mostly get duplicate calls with the same ``current``,
            ``total``, and ``current_filepath``. This shouldn't be much of a problem
            for your hooks because you should make sure that an update with duplicate
            data doesn't change the displayed progress.

        Args:
            to_dir (str): The directory to extract the content into
            progress_hook (Callable[[int, int, str], None], optional): Defaults to None.
                A progress hook that should expect (``current``, ``total``,
                ``current_filepath``) as arguments

        Raises:
            NotADirectoryError: If the given directory does not exist
            ValueError: Various file reading errors
        """
        if not os.path.isdir(to_dir):
            raise NotADirectoryError(f"no such directory '{to_dir!r}' exists")

        # defines the compressed and uncompressed file structure using an EmbeddedSwitch
        file_struct = EmbeddedSwitch(
            Struct(
                "name" / If(
                    self.container.header.flags.files_compressed,
                    CString("utf8")
                )
            ),
            self.container.header.flags.files_compressed,
            {
                True: Struct(
                    "original_size" / Int32ul,
                    "data" / Compressed(GreedyBytes, "zlib")
                ),
                False: Struct("data" / GreedyBytes),
            },
        )

        # NOTE: could be either compressed or uncompressed size
        total_size = sum(
            record.size
            for block in self.container.file_blocks
            for record in block.records
        )
        current_size = 0
        file_index = 0
        to_dir = Path(to_dir)

        # iterate over zipped directory records and file blocks
        # (should always be the same length)
        for (directory_record, file_block) in zip(
            self.container.directory_records, self.container.file_blocks
        ):
            directory_path = to_dir
            if isinstance(file_block.name, str):
                directory_path = directory_path.joinpath(
                    PureWindowsPath(file_block.name[:-1])
                )

            # iterate over all files in the file block
            for file_record in file_block.records:
                to_path = directory_path
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
                            f"maybe corrupt file or unsupported bsa version"
                        ))

                    # archive file names should always be the same length of the
                    # header's `file_count`
                    to_path = directory_path.joinpath(
                        self.container.file_names[file_index]
                    )
                    file_index += 1

                posix_path = to_path.as_posix()
                # push pre-stage progress (includes 0.0 for first call)
                if callable(progress_hook):
                    progress_hook(current_size, total_size, posix_path)

                # create parent directories and write data out
                if not to_path.parent.is_dir():
                    to_path.parent.mkdir(parents=True)
                with to_path.open("wb") as stream:
                    stream.write(file_container.data)
                current_size += len(file_container.data)

                # push post-stage progress (includes 100.0 for last call)
                if callable(progress_hook):
                    progress_hook(current_size, total_size, posix_path)
