# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

from enum import IntEnum
from typing import Generator
from pathlib import PureWindowsPath

from construct import (
    Enum,
    Array,
    Bytes,
    Int8ul,
    Struct,
    Switch,
    VarInt,
    Default,
    Int16ul,
    Int32ul,
    Int64ul,
    FlagsEnum,
    PaddedString,
    PascalString,
)

from ._common import ArchiveFile, BaseArchive


def MAKEFOURCC(ch0: str, ch1: str, ch2: str, ch3: str) -> int:
    return (ord(ch0) << 0) | (ord(ch1) << 8) | (ord(ch2) << 16) | (ord(ch3) << 24)


class DXGIFormats(IntEnum):
    """ Formats for DXGI resources.

    .. tip:: The original values for this enumeration were taken \
        directly from `Microsoft's DXGI format documentation \
        <https://msdn.microsoft.com/en-us/library/windows/desktop/bb173059(v=vs.85).aspx>`_
    """

    DXGI_FORMAT_UNKNOWN = 0
    DXGI_FORMAT_R32G32B32A32_TYPELESS = 1
    DXGI_FORMAT_R32G32B32A32_FLOAT = 2
    DXGI_FORMAT_R32G32B32A32_UINT = 3
    DXGI_FORMAT_R32G32B32A32_SINT = 4
    DXGI_FORMAT_R32G32B32_TYPELESS = 5
    DXGI_FORMAT_R32G32B32_FLOAT = 6
    DXGI_FORMAT_R32G32B32_UINT = 7
    DXGI_FORMAT_R32G32B32_SINT = 8
    DXGI_FORMAT_R16G16B16A16_TYPELESS = 9
    DXGI_FORMAT_R16G16B16A16_FLOAT = 10
    DXGI_FORMAT_R16G16B16A16_UNORM = 11
    DXGI_FORMAT_R16G16B16A16_UINT = 12
    DXGI_FORMAT_R16G16B16A16_SNORM = 13
    DXGI_FORMAT_R16G16B16A16_SINT = 14
    DXGI_FORMAT_R32G32_TYPELESS = 15
    DXGI_FORMAT_R32G32_FLOAT = 16
    DXGI_FORMAT_R32G32_UINT = 17
    DXGI_FORMAT_R32G32_SINT = 18
    DXGI_FORMAT_R32G8X24_TYPELESS = 19
    DXGI_FORMAT_D32_FLOAT_S8X24_UINT = 20
    DXGI_FORMAT_R32_FLOAT_X8X24_TYPELESS = 21
    DXGI_FORMAT_X32_TYPELESS_G8X24_UINT = 22
    DXGI_FORMAT_R10G10B10A2_TYPELESS = 23
    DXGI_FORMAT_R10G10B10A2_UNORM = 24
    DXGI_FORMAT_R10G10B10A2_UINT = 25
    DXGI_FORMAT_R11G11B10_FLOAT = 26
    DXGI_FORMAT_R8G8B8A8_TYPELESS = 27
    DXGI_FORMAT_R8G8B8A8_UNORM = 28
    DXGI_FORMAT_R8G8B8A8_UNORM_SRGB = 29
    DXGI_FORMAT_R8G8B8A8_UINT = 30
    DXGI_FORMAT_R8G8B8A8_SNORM = 31
    DXGI_FORMAT_R8G8B8A8_SINT = 32
    DXGI_FORMAT_R16G16_TYPELESS = 33
    DXGI_FORMAT_R16G16_FLOAT = 34
    DXGI_FORMAT_R16G16_UNORM = 35
    DXGI_FORMAT_R16G16_UINT = 36
    DXGI_FORMAT_R16G16_SNORM = 37
    DXGI_FORMAT_R16G16_SINT = 38
    DXGI_FORMAT_R32_TYPELESS = 39
    DXGI_FORMAT_D32_FLOAT = 40
    DXGI_FORMAT_R32_FLOAT = 41
    DXGI_FORMAT_R32_UINT = 42
    DXGI_FORMAT_R32_SINT = 43
    DXGI_FORMAT_R24G8_TYPELESS = 44
    DXGI_FORMAT_D24_UNORM_S8_UINT = 45
    DXGI_FORMAT_R24_UNORM_X8_TYPELESS = 46
    DXGI_FORMAT_X24_TYPELESS_G8_UINT = 47
    DXGI_FORMAT_R8G8_TYPELESS = 48
    DXGI_FORMAT_R8G8_UNORM = 49
    DXGI_FORMAT_R8G8_UINT = 50
    DXGI_FORMAT_R8G8_SNORM = 51
    DXGI_FORMAT_R8G8_SINT = 52
    DXGI_FORMAT_R16_TYPELESS = 53
    DXGI_FORMAT_R16_FLOAT = 54
    DXGI_FORMAT_D16_UNORM = 55
    DXGI_FORMAT_R16_UNORM = 56
    DXGI_FORMAT_R16_UINT = 57
    DXGI_FORMAT_R16_SNORM = 58
    DXGI_FORMAT_R16_SINT = 59
    DXGI_FORMAT_R8_TYPELESS = 60
    DXGI_FORMAT_R8_UNORM = 61
    DXGI_FORMAT_R8_UINT = 62
    DXGI_FORMAT_R8_SNORM = 63
    DXGI_FORMAT_R8_SINT = 64
    DXGI_FORMAT_A8_UNORM = 65
    DXGI_FORMAT_R1_UNORM = 66
    DXGI_FORMAT_R9G9B9E5_SHAREDEXP = 67
    DXGI_FORMAT_R8G8_B8G8_UNORM = 68
    DXGI_FORMAT_G8R8_G8B8_UNORM = 69
    DXGI_FORMAT_BC1_TYPELESS = 70
    DXGI_FORMAT_BC1_UNORM = 71
    DXGI_FORMAT_BC1_UNORM_SRGB = 72
    DXGI_FORMAT_BC2_TYPELESS = 73
    DXGI_FORMAT_BC2_UNORM = 74
    DXGI_FORMAT_BC2_UNORM_SRGB = 75
    DXGI_FORMAT_BC3_TYPELESS = 76
    DXGI_FORMAT_BC3_UNORM = 77
    DXGI_FORMAT_BC3_UNORM_SRGB = 78
    DXGI_FORMAT_BC4_TYPELESS = 79
    DXGI_FORMAT_BC4_UNORM = 80
    DXGI_FORMAT_BC4_SNORM = 81
    DXGI_FORMAT_BC5_TYPELESS = 82
    DXGI_FORMAT_BC5_UNORM = 83
    DXGI_FORMAT_BC5_SNORM = 84
    DXGI_FORMAT_B5G6R5_UNORM = 85
    DXGI_FORMAT_B5G5R5A1_UNORM = 86
    DXGI_FORMAT_B8G8R8A8_UNORM = 87
    DXGI_FORMAT_B8G8R8X8_UNORM = 88
    DXGI_FORMAT_R10G10B10_XR_BIAS_A2_UNORM = 89
    DXGI_FORMAT_B8G8R8A8_TYPELESS = 90
    DXGI_FORMAT_B8G8R8A8_UNORM_SRGB = 91
    DXGI_FORMAT_B8G8R8X8_TYPELESS = 92
    DXGI_FORMAT_B8G8R8X8_UNORM_SRGB = 93
    DXGI_FORMAT_BC6H_TYPELESS = 94
    DXGI_FORMAT_BC6H_UF16 = 95
    DXGI_FORMAT_BC6H_SF16 = 96
    DXGI_FORMAT_BC7_TYPELESS = 97
    DXGI_FORMAT_BC7_UNORM = 98
    DXGI_FORMAT_BC7_UNORM_SRGB = 99
    DXGI_FORMAT_AYUV = 100
    DXGI_FORMAT_Y410 = 101
    DXGI_FORMAT_Y416 = 102
    DXGI_FORMAT_NV12 = 103
    DXGI_FORMAT_P010 = 104
    DXGI_FORMAT_P016 = 105
    DXGI_FORMAT_420_OPAQUE = 106
    DXGI_FORMAT_YUY2 = 107
    DXGI_FORMAT_Y210 = 108
    DXGI_FORMAT_Y216 = 109
    DXGI_FORMAT_NV11 = 110
    DXGI_FORMAT_AI44 = 111
    DXGI_FORMAT_IA44 = 112
    DXGI_FORMAT_P8 = 113
    DXGI_FORMAT_A8P8 = 114
    DXGI_FORMAT_B4G4R4A4_UNORM = 115
    DXGI_FORMAT_P208 = 130
    DXGI_FORMAT_V208 = 131
    DXGI_FORMAT_V408 = 132
    DXGI_FORMAT_FORCE_UINT = 0xffffffff


class BTDXArchive(BaseArchive):

    DDS_MAGIC = 0x20534444
    DDS_PIXELFORMAT = Struct(
        "dwSize" / Int32ul,
        "dwFlags"
        / FlagsEnum(
            Int32ul,
            fourcc=0x00000004,
            rgb=0x00000040,
            rgba=0x00000041,
            luminance=0x00020000,
            alpha=0x00000002,
        ),
        "dwFourCC" / Int32ul,
        "dwRGBBitCount" / Default(Int32ul, 0),
        "dwRBitMask" / Default(Int32ul, 0),
        "dwGBitMask" / Default(Int32ul, 0),
        "dwBBitMask" / Default(Int32ul, 0),
        "dwABitMask" / Default(Int32ul, 0),
    )
    DDS_HEADER = Struct(
        "dwSize" / Int32ul,
        "dwHeaderFlags"
        / FlagsEnum(
            Int32ul,
            texture=0x00001007,
            mipmap=0x00020000,
            volume=0x00800000,
            pitch=0x00000008,
            linearsize=0x00080000,
        ),
        "dwHeight" / Int32ul,
        "dwWidth" / Int32ul,
        "dwPitchOrLinearSize" / Int32ul,
        "dwDepth" / Int32ul,
        "dwMipMapCount" / Int32ul,
        "dwReserved1" / Array(11, Int32ul),
        "ddspf" / DDS_PIXELFORMAT,
        "dwSurfaceFlags"
        / FlagsEnum(Int32ul, texture=0x00001000, mipmap=0x00400008, cubemap=0x00000008),
        "dwCubemapFlags"
        / FlagsEnum(
            Int32ul,
            positivex=0x00000600,
            negativex=0x00000a00,
            positivey=0x00001200,
            negativey=0x00002200,
            positivez=0x00004200,
            negativez=0x00008200,
        ),
        "dwReserved2" / Array(3, Int32ul),
    )
    """Struct: Structure for DDS headers.

    Note:
        https://github.com/Microsoft/DirectXTex/blob/master/DirectXTex/DDS.h
    """

    DDS_HEADER_DX10 = Struct(
        "dxgiFormat" / Int32ul,
        "resourceDimension" / Enum(Int32ul, texture1d=2, texture2d=3, texture3d=4),
        "miscFlag" / Int32ul,
        "arraySize" / Int32ul,
        "miscFlags2" / Int32ul,
    )

    header_struct = Struct(
        "magic" / Bytes(4),
        "version" / Int32ul,
        "type" / PaddedString(4, "utf8"),
        "file_count" / Int32ul,
        "names_offset" / Int64ul,
    )
    file_struct = Struct(
        "hash" / Int32ul,
        "ext" / PaddedString(4, "utf8"),
        "directory_hash" / Int32ul,
        "_unknown_0" / Int32ul,
        "offset" / Int64ul,
        "packed_size" / Int32ul,
        "unpacked_size" / Int32ul,
        "_unknown_1" / Int32ul,
    )
    tex_header_struct = Struct(
        "hash" / Int32ul,
        "ext" / PaddedString(4, "utf8"),
        "directory_hash" / Int32ul,
        "_unknown_0" / Int8ul,
        "chunks_count" / Int8ul,
        "chunk_header_size" / Int16ul,
        "height" / Int16ul,
        "width" / Int16ul,
        "mips_count" / Int8ul,
        "format" / Int8ul,
        "_unknown_1" / Int16ul,
    )
    tex_chunk_struct = Struct(
        "offset" / Int64ul,
        "packed_size" / Int32ul,
        "unpacked_size" / Int32ul,
        "start_mip" / Int16ul,
        "end_mip" / Int16ul,
        "_unknown_0" / Int32ul,
    )
    tex_struct = Struct(
        "header" / tex_header_struct,
        "chunks" / Array(lambda this: this.header.chunks_count, tex_chunk_struct),
    )
    archive_struct = Struct(
        "header" / header_struct,
        "files"
        / Array(
            lambda this: this.header.file_count,
            Switch(
                lambda this: this.header.type, {"GNRL": file_struct, "DX10": tex_struct}
            ),
        ),
    )

    @classmethod
    def can_handle(cls, filepath: str) -> bool:
        """Determines if a given file can be handled by the current archive.

        Args:
            filepath (str): The filepath to check if can be handled

        Returns:
            bool: True if the file can be handled, otherwise False
        """
        header = cls.header_struct.parse_file(filepath)
        return header.magic == "BTDX" and header.version >= 1

    def _iter_gnrl_files(self) -> Generator[ArchiveFile, None, None]:
        """Iterates over the parsed data for GNRL fiels and yields instances of
            `ArchiveFile`.

        Raises:
            ValueError: If a filename cannot be determined for a specific file record

        Yields:
            ArchiveFile: An file contained within the archive
        """
        filename_offset = 0
        for (file_idx, file_container) in enumerate(self.container.files):
            filepath_content = self.content[
                (self.container.header.names_offset + filename_offset):
            ]
            filepath = PascalString(VarInt, "utf8").parse(filepath_content)
            # filename offset increased by length of parsed string accounting for
            # prefix and suffix bytes
            filename_offset += len(filepath) + 2

            yield ArchiveFile(
                filepath=PureWindowsPath(filepath[1:]),
                data=self.content[
                    file_container.offset:(
                        file_container.offset + file_container.unpacked_size
                    )
                ],
            )

    def _iter_dx10_files(self) -> Generator[ArchiveFile, None, None]:
        """Iterates over the parsed data for DX10 archives and yields instances of
            `ArchiveFile`.

        Raises:
            ValueError: If a filename cannot be determined for a specific file record

        Yields:
            ArchiveFile: An file contained within the archive
        """
        filename_offset = 0
        for (file_idx, file_container) in enumerate(self.container.files):

            header_dict = {
                "dwSize": self.DDS_HEADER.sizeof(),
                "dwHeaderFlags": {"texture": True, "linearsize": True, "mipmap": True},
                "dwHeight": file_container.header.height,
                "dwWidth": file_container.header.width,
                "dwMipMapCount": file_container.header.mips_count,
                "dwSurfaceFlags": {"texture": True, "mipmap": True},
            }

            if file_container.header._unknown_1 == 2049:
                header_dict["dwCubemapFlags"] = {
                    "positivex": True,
                    "negativex": True,
                    "positivey": True,
                    "negativey": True,
                    "positivez": True,
                    "negativez": True,
                }

            pixel_dict = {"dwSize": self.DDS_PIXELFORMAT.sizeof()}
            dx10_header_dict = {}
            if file_container.header.format == DXGIFormats.DXGI_FORMAT_BC1_UNORM:
                pixel_dict.update(
                    {
                        "dwFlags": {"fourcc": True},
                        "dwFourCC": MAKEFOURCC("D", "X", "T", "1"),
                    }
                )
                header_dict[
                    "dwPitchOrLinearSize"
                ] = file_container.header.width * file_container.header.height / 2
            elif file_container.header.format == DXGIFormats.DXGI_FORMAT_BC2_UNORM:
                pixel_dict.update(
                    {
                        "dwFlags": {"fourcc": True},
                        "dwFourCC": MAKEFOURCC("D", "X", "T", "3"),
                    }
                )
                header_dict[
                    "dwPitchOrLinearSize"
                ] = file_container.header.width * file_container.header.height
            elif file_container.header.format == DXGIFormats.DXGI_FORMAT_BC3_UNORM:
                pixel_dict.update(
                    {
                        "dwFlags": {"fourcc": True},
                        "dwFourCC": MAKEFOURCC("D", "X", "T", "5"),
                    }
                )
                header_dict[
                    "dwPitchOrLinearSize"
                ] = file_container.header.width * file_container.header.height
            elif file_container.header.format == DXGIFormats.DXGI_FORMAT_BC5_UNORM:
                pixel_dict.update(
                    {
                        "dwFlags": {"fourcc": True},
                        "dwFourCC": MAKEFOURCC("A", "T", "I", "2"),
                    }
                )
                header_dict[
                    "dwPitchOrLinearSize"
                ] = file_container.header.width * file_container.header.height
            elif file_container.header.format == DXGIFormats.DXGI_FORMAT_BC7_UNORM:
                pixel_dict.update(
                    {
                        "dwFlags": {"fourcc": True},
                        "dwFourCC": MAKEFOURCC("D", "X", "1", "0"),
                    }
                )
                header_dict[
                    "dwPitchOrLinearSize"
                ] = file_container.header.width * file_container.header.height
                dx10_header_dict["dxgiFormat"] = file_container.header.format
            elif file_container.header.format == DXGIFormats.DXGI_FORMAT_B8G8R8A8_UNORM:
                pixel_dict.update(
                    {
                        "dwFlags": {"rgba": True},
                        "dwRGBBitCount": 32,
                        "dwRBitMask": 0x00ff0000,
                        "dwGBitMask": 0x0000ff00,
                        "dwBBitMask": 0x000000ff,
                        "dwABitMask": 0xff000000,
                    }
                )
                header_dict[
                    "dwPitchOrLinearSize"
                ] = file_container.header.width * file_container.header.height * 4
            elif file_container.header.format == DXGIFormats.DXGI_FORMAT_R8_UNORM:
                pixel_dict.update(
                    {"dwFlags": {"rgb": True}, "dwRGBBitCount": 8, "dwRBitMask": 0xff}
                )
                header_dict[
                    "dwPitchOrLinearSize"
                ] = file_container.header.width * file_container.header.height
            else:
                raise ValueError(
                    f"unsupported dxgi format {file_container.header.format!r}"
                )

            print(pixel_dict)
            print(self.DDS_PIXELFORMAT.build(pixel_dict))

            input()

    def iter_files(self) -> Generator[ArchiveFile, None, None]:
        """Iterates over the parsed data and yields instances of `ArchiveFile`

        Raises:
            ValueError: If a filename cannot be determined for a specific file record

        Yields:
            ArchiveFile: An file contained within the archive
        """
        iter_method = {"GNRL": self._iter_gnrl_files, "DX10": self._iter_dx10_files}[
            self.container.header.type
        ]
        for archive_file in iter_method():
            yield archive_file
