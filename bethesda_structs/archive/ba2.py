# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import os
import enum
import zlib
import ctypes
import struct
from typing import (List, Callable, Union,)

from .. import (meta,)
from ._common import (AbstractArchive,)


def fourcc(char0: str, char1: str, char2: str, char3: str) -> int:
    """ Substitute for Microsoft's MAKEFOURCC macro.

    .. tip:: The logic of this macro was taken directly from \
        `Microsoft's DirectXTex DDS header \
        <https://github.com/Microsoft/DirectXTex/blob/master/DirectXTex/DDS.h>`_

    :param char0: The first character
    :type char0: str
    :param char1: The second character
    :type char1: str
    :param char2: The third character
    :type char2: str
    :param char3: The fourth character
    :type char3: str
    :returns: The generated FOURCC code
    """

    return (
        (ord(char0) << 0x0) |
        (ord(char1) << 0x8) |
        (ord(char2) << 0x10) |
        (ord(char3) << 0x18)
    )


class DXGIFormats(enum.IntEnum):
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


class DDSFlags(enum.IntEnum):
    """ Flags for Microsoft's DDS files used in DirectX.

    .. note:: This enumeration is not unique as some duplicate values \
        are meant to be used in different contexts.\
        For example, ``DDS_FOURCC`` and ``DDS_WIDTH`` share the value ``4``.
        However, the ``DDS_FOURCC`` key is used in DDS headers while the \
        ``DDS_WIDTH`` is used in texture definitons.

    .. tip:: The original values for this enumeration were taken \
        directly from `Microsoft's DirectXTex DDS header \
        <https://github.com/Microsoft/DirectXTex/blob/master/DirectXTex/DDS.h>`_
    """

    DDS_MAGIC = 0x20534444
    DDS_FOURCC = 0x00000004
    DDS_RGB = 0x00000040
    DDS_RGBA = 0x00000041
    DDS_LUMINANCE = 0x00020000
    DDS_LUMINANCEA = 0x00020001
    DDS_ALPHA = 0x00000002
    DDS_PAL8 = 0x00000020
    DDS_HEADER_FLAGS_TEXTURE = 0x00001007
    DDS_HEADER_FLAGS_MIPMAP = 0x00020000
    DDS_HEADER_FLAGS_VOLUME = 0x00800000
    DDS_HEADER_FLAGS_PITCH = 0x00000008
    DDS_HEADER_FLAGS_LINEARSIZE = 0x00080000
    DDS_HEIGHT = 0x00000002
    DDS_WIDTH = 0x00000004
    DDS_SURFACE_FLAGS_TEXTURE = 0x00001000
    DDS_SURFACE_FLAGS_MIPMAP = 0x00400008
    DDS_SURFACE_FLAGS_CUBEMAP = 0x00000008
    DDS_CUBEMAP_POSITIVEX = 0x00000600
    DDS_CUBEMAP_POSITIVEY = 0x00001200
    DDS_CUBEMAP_NEGATIVEX = 0x00000a00
    DDS_CUBEMAP_NEGATIVEY = 0x00002200
    DDS_CUBEMAP_POSITIVEZ = 0x00004200
    DDS_CUBEMAP_NEGATIVEZ = 0x00008200
    DDS_CUBEMAP_ALLFACES = (
        DDS_CUBEMAP_POSITIVEX | DDS_CUBEMAP_NEGATIVEX |
        DDS_CUBEMAP_POSITIVEY | DDS_CUBEMAP_NEGATIVEY |
        DDS_CUBEMAP_POSITIVEZ | DDS_CUBEMAP_NEGATIVEZ
    )
    DDS_CUBEMAP = 0x00000200
    DDS_FLAGS_VOLUME = 0x00200000


class DDSPixelFormat(ctypes.Structure):
    """ The C structure DDS_PIXELFORMAT.

    The ``_fields_`` class variable is defined as the following:

    .. code-block:: python

        _fields_ = [
            ('dwSize', ctypes.c_uint32),
            ('dwFlags', ctypes.c_uint32),
            ('dwFourCC', ctypes.c_uint32),
            ('dwRGBBitCount', ctypes.c_uint32),
            ('dwRBitMask', ctypes.c_uint32),
            ('dwGBitMask', ctypes.c_uint32),
            ('dwBBitMask', ctypes.c_uint32),
            ('dwABitMask', ctypes.c_uint32),
        ]

    .. tip:: This structure is taken directly from \
        `Microsoft's DDS_PIXELFORMAT documentation \
        <https://msdn.microsoft.com/en-us/library/windows/desktop/bb943984(v=vs.85).aspx>`_
    """

    _fields_ = [
        ('dwSize', ctypes.c_uint32),
        ('dwFlags', ctypes.c_uint32),
        ('dwFourCC', ctypes.c_uint32),
        ('dwRGBBitCount', ctypes.c_uint32),
        ('dwRBitMask', ctypes.c_uint32),
        ('dwGBitMask', ctypes.c_uint32),
        ('dwBBitMask', ctypes.c_uint32),
        ('dwABitMask', ctypes.c_uint32),
    ]


class DDSHeader(ctypes.Structure):
    """ The C structure DDS_HEADER.

    The ``_fields_`` class variable is defined as the following:

    .. code-block:: python

        _fields_ = [
            ('dwSize', ctypes.c_uint32),
            ('dwFlags', ctypes.c_uint32),
            ('dwHeight', ctypes.c_uint32),
            ('dwWidth', ctypes.c_uint32),
            ('dwPitchOrLinearSize', ctypes.c_uint32),
            ('dwDepth', ctypes.c_uint32),
            ('dwMipMapCount', ctypes.c_uint32),
            ('dwReserved1', ctypes.c_uint32 * 11),
            ('ddspf', DDSPixelFormat),
            ('dwCaps', ctypes.c_uint32),
            ('dwCaps2', ctypes.c_uint32),
            ('dwCaps3', ctypes.c_uint32),
            ('dwCaps4', ctypes.c_uint32),
            ('dwReserved2', ctypes.c_uint32),
        ]

    .. tip:: This structure is taken directly from \
        `Microsoft's DDS_HEADER documentation \
        <https://msdn.microsoft.com/en-us/library/windows/desktop/bb943982(v=vs.85).aspx>`_
    """

    _fields_ = [
        ('dwSize', ctypes.c_uint32),
        ('dwFlags', ctypes.c_uint32),
        ('dwHeight', ctypes.c_uint32),
        ('dwWidth', ctypes.c_uint32),
        ('dwPitchOrLinearSize', ctypes.c_uint32),
        ('dwDepth', ctypes.c_uint32),
        ('dwMipMapCount', ctypes.c_uint32),
        ('dwReserved1', ctypes.c_uint32 * 11),
        ('ddspf', DDSPixelFormat),
        ('dwCaps', ctypes.c_uint32),
        ('dwCaps2', ctypes.c_uint32),
        ('dwCaps3', ctypes.c_uint32),
        ('dwCaps4', ctypes.c_uint32),
        ('dwReserved2', ctypes.c_uint32),
    ]


class BA2TextureChunk(meta.Prefixed):
    """ An object representing an BA2 texture chunk.
    """

    _prefix_struct = '<QLLHHL'
    _prefix_names = (
        '_offset', '_packed_size', '_full_size',
        '_start_mipmap', '_end_mipmap', '_align',
    )

    def __repr__(self) -> str:
        """ Builds a human readable string to represent the object.

        :returns: A human readable string to represent the object.
        """

        return (
            '<{self.__class__.__name__} {self.offset} {compressed}>'
        ).format(
            compressed=('(compressed)' if self.packed_size > 0 else ''),
            **locals()
        )

    def __len__(self) -> int:
        """ Returns the length of the BA2 DX10 texture file chunk in bytes.

        :returns: The length of the BA2 DX10 texture file chunk in bytes
        """

        return self.full_size

    @property
    def offset(self) -> int:
        """ The offset of the DX10 texture file chunk content.

        :getter: Returns the offset of the DX10 texture file chunk content
        :setter: Does not allow setting
        """

        return self._offset

    @property
    def packed_size(self) -> int:
        """ The size of the compressed chunk content.

        :getter: Returns the size of the compressed chunk content
        :setter: Does not allow setting
        """

        return self._packed_size

    @property
    def full_size(self) -> int:
        """ The full size of the chunk content.

        :getter: Returns the full size of the chunk content
        :setter: Does not allow setting
        """

        return self._full_size

    @property
    def start_mipmap(self) -> int:
        """ The starting byte offset of the chunk mipmap.

        :getter: Returns the starting byte offset of the chunk mipmap
        :setter: Does not allow setting
        """

        return self._start_mipmap

    @property
    def end_mipmap(self) -> int:
        """ The ending byte offset of the chunk mipmap.

        :getter: Returns the ending byte offset of the chunk mipmap
        :setter: Does not allow setting
        """

        return self._end_mipmap

    @property
    def align(self) -> int:
        """ Unknown chunk alignment value.

        :getter: Returns the unknown chunk alignment value
        :setter: Does not allow setting
        """

        return self._align


class BA2TextureFile(meta.Prefixed):
    """ An object representing an archived BA2 compressed texture file.
    """

    _prefix_struct = '<L4sLBBHHHBBH'
    _prefix_names = (
        '_name_hash', '_extension', '_folder_hash', '_unk_8',
        '_chunk_count', '_chunk_size', '_height', '_width',
        '_mipmap_count', '_format', '_unk_16',
    )

    def __init__(self, buffer: bytes, filepath: str):
        """ Initializes the BA2 compressed texture file object.

        :param buffer: The archive buffer starting at the file object offset
        :type buffer: bytes
        :param filepath: The file path of the BA2 compressed texture file
        :type filepath: str
        """

        super().__init__(buffer)
        self._filepath = os.path.normpath(filepath).strip('.')

    def __repr__(self) -> str:
        """ Builds a human readable string to represent the object.

        :returns: A human readable string to represent the object.
        """

        return (
            '<{self.__class__.__name__} "{self.filepath}" '
            '({self.chunk_count} chunks)>'
        ).format(**locals())

    def __len__(self) -> int:
        """ Returns the length of the BA2 compressed texture file in bytes.

        :returns: The length of the BA2 compressed texture file in bytes
        """

        # need to account for all the chunks that make up the texture
        return (
            self._prefix_size + (
                len(self.chunks) *
                struct.calcsize(BA2TextureChunk._prefix_struct)
            )
        )

    @property
    def name_hash(self) -> int:
        """ A unique hash for the file name in the archive.

        :getter: Returns a unique hash for the file name in the archive
        :setter: Does not allow setting
        """

        return self._name_hash

    @property
    def extension(self) -> str:
        """ The extension of the file.

        .. note:: The extension is stored within ``4`` fixed characters.
            Empty characters are replaced with null bytes.

        :getter: Returns the extension of the file
        :setter: Does not allow setting
        """

        return self._extension

    @property
    def folder_hash(self) -> int:
        """ A unique hash for the folder name in the archive.

        :getter: Returns a unique hash for the folder name in the archive
        :setter: Does not allow setting
        """

        return self._folder_hash

    @property
    def unk_8(self) -> int:
        """ Unknown value with tag 8.

        :getter: Returns the unkown value with tag 8
        :setter: Does not allow setting
        """

        return self._unk_8

    @property
    def chunk_count(self) -> int:
        """ The number of chunks within a DX10 texture file.

        :getter: Returns the number of chunks within a DX10 texture file
        :setter: Does not allow setting
        """

        return self._chunk_count

    @property
    def chunk_size(self) -> int:
        """ The size of chunks within a DX10 texture file.

        :getter: Returns the size of chunks within a DX10 texture file
        :setter: Does not allow setting
        """

        return self._chunk_size

    @property
    def height(self) -> int:
        """ The height in pixels of a DX10 texture file.

        :getter: Returns the height in pixels of a DX10 texture file
        :setter: Does not allow setting
        """

        return self._height

    @property
    def width(self) -> int:
        """ The width in pixels of a DX10 texture file.

        :getter: Returns the width in pixels of a DX10 texture file
        :setter: Does not allow setting
        """

        return self._width

    @property
    def mipmap_count(self) -> int:
        """ The number of mipmaps within a DX10 texture file.

        :getter: Returns the number of mipmaps within a DX10 texture file
        :setter: Does not allow setting
        """

        return self._mipmap_count

    @property
    def format(self) -> int:
        """ The DXGI format of the DX10 texture file.

        .. note:: Should be found in :class:`~DXGIFormats`.

        :getter: Returns the DXGI format for the DX10 texture file
        :setter: Does not allow setting
        """

        return self._format

    @property
    def unk_16(self) -> int:
        """ Unknown value with tag 16.

        :getter: Returns the unkown value with tag 16
        :setter: Does not allow setting
        """

        return self._unk_16

    @property
    def filepath(self) -> str:
        """ The archived filepath of the BA2 file.

        :getter: Returns the archived filepath of the BA2 file
        :setter: Does not allow setting
        """

        return self._filepath

    @property
    def chunks(self) -> List[BA2TextureChunk]:
        """ The chunks that make up the content of a texture file.

        :getter: Returns the chunks that make up the content of a texture file.
        :setter: Does not allow setting
        """

        if not hasattr(self, '_chunks'):
            self._chunks = []

            # chunk prefix should just be calculated once
            chunk_prefix_size = struct.calcsize(BA2TextureChunk._prefix_struct)
            buffer_offset = self._prefix_size
            for chunk_idx in range(self.chunk_count):
                # initialize a new chunk given the current buffer
                chunk_ = BA2TextureChunk(self._buffer[
                    buffer_offset:(buffer_offset + chunk_prefix_size)
                ])
                # add the initialized texture chunk to the file's chunks
                self._chunks.append(chunk_)
                # chunk size is only as large as the prefix
                # offset indicates where content is actually stored
                buffer_offset += chunk_prefix_size

        return self._chunks


class BA2File(meta.Prefixed):
    """ An object representing an archived BA2 file.
    """

    _prefix_struct = '<L4sLLQLLL'
    _prefix_names = (
        '_name_hash', '_extension', '_folder_hash', '_flags', '_offset',
        '_packed_size', '_full_size', '_align',
    )

    def __init__(self, buffer: bytes, filepath: str):
        """ Initializes the BA2 file object.

        :param buffer: The archive buffer starting at the file object offset
        :type buffer: bytes
        :param filepath: The file path of the BA2 file
        :type filepath: str
        """

        super().__init__(buffer)
        self._filepath = os.path.normpath(filepath).strip('.')

    def __repr__(self) -> str:
        """ Builds a human readable string to represent the object.

        :returns: A human readable string to represent the object.
        """

        return (
            '<{self.__class__.__name__} "{self.filepath}" '
            '({self.full_size} bytes)>'
        ).format(**locals())

    def __len__(self) -> int:
        """ Returns the length of the BA2 file in bytes.

        :returns: The length of the BA2 file in bytes
        """

        return self.full_size

    @property
    def name_hash(self) -> int:
        """ A unique hash for the file name in the archive.

        :getter: Returns a unique hash for the file name in the archive
        :setter: Does not allow setting
        """

        return self._name_hash

    @property
    def extension(self) -> str:
        """ The extension of the file.

        .. note:: The extension is stored within ``4`` fixed characters.
            Empty characters are replaced with null bytes.

        :getter: Returns the extension of the file
        :setter: Does not allow setting
        """

        return self._extension

    @property
    def folder_hash(self) -> int:
        """ A unique hash for the folder name in the archive.

        :getter: Returns a unique hash for the folder name in the archive
        :setter: Does not allow setting
        """

        return self._folder_hash

    @property
    def flags(self) -> int:
        """ Flags identifying specific features of the file.

        .. note:: I have no clue how to interpret these flags 😞

        :getter: Returns the flags of the file
        :setter: Does not allow setting
        """

        return self._flags

    @property
    def offset(self) -> int:
        """ The offset to where the file contents start.

        :getter: Returns the offset to where the file contents start
        :setter: Does not allow setting
        """

        return self._offset

    @property
    def packed_size(self) -> int:
        """ The size of the packed data in bytes.

        .. note:: Should be equal to ``0`` if data is not packed

        :getter: Returns the size of the packed data in bytes
        :setter: Does not allow setting
        """

        return self._packed_size

    @property
    def full_size(self) -> int:
        """ The full size of the data in bytes.

        :getter: Returns the size of the unpacked data in bytes
        :setter: Does not allow setting
        """

        return self._full_size

    @property
    def align(self) -> int:
        """ Unknown alignment value.

        .. note:: Seems to be a constant (``3131961357``) for GNRL archives. \
            I don't know what it really means 😞

        :getter: Returns the unknown alignment value
        :setter: Does not allow setting
        """

        return self._align

    @property
    def filepath(self) -> str:
        """ The archived filepath of the BA2 file.

        :getter: Returns the archived filepath of the BA2 file
        :setter: Does not allow setting
        """

        return self._filepath


class BA2Header(meta.Prefixed):
    """ An object representing an archived BA2 header.
    """

    _prefix_struct = '<4sL4sLQ'
    _prefix_names = (
        '_ba2', '_version', '_type', '_file_count', '_names_offset',
    )

    def __repr__(self) -> str:
        """ Builds a human readable string to represent the object.

        :returns: A human readable string to represent the object.
        """

        return (
            '<{self.__class__.__name__} {self.type}>'
        ).format(**locals())

    def __len__(self) -> int:
        """ Returns the length of the BA2 header prefix in bytes.

        :returns: The length of the BA2 header prefix in bytes
        """

        return self._prefix_size

    @property
    def ba2(self) -> str:
        """ The BA2 magic of the header.

        .. note:: Should always be ``BTDX`` in bytes.

        :getter: Returns the BA2 magic of the header
        :setter: Does not allow setting
        """

        return self._ba2

    @property
    def version(self) -> int:
        """ The version of the BA2 archive format.

        .. note:: Seems to always be ``1``.

        :getter: Returns the version of the BA2 archive format
        :setter: Does not allow setting
        """

        return self._version

    @property
    def type(self) -> str:
        """ The type of the BA2 archive format.

        .. note:: Should either be ``GNRL`` or ``DX10``.

        :getter: Returns the type of the BA2 archive format
        :setter: Does not allow setting
        """

        return self._type

    @property
    def file_count(self) -> int:
        """ The number of files within the BA2 archive.

        :getter: Returns the number of files within the BA2 archive
        :setter: Does not allow setting
        """

        return self._file_count

    @property
    def names_offset(self) -> int:
        """ The byte offset where the BA2 file names start.

        :getter: Returns the byte offset where the BA2 file names start
        :setter: Does not allow setting
        """

        return self._names_offset


class BA2Archive(AbstractArchive):
    """ Wrapper for a BA2 archive.
    """

    def __init__(self, filepath: str):
        """ Initializes the BA2 archive wrapper.

        :param filepath: The filepath for a given BA2 archive
        :type filepath: str
        :returns: Does not return
        """

        self.filepath = filepath
        with open(self.filepath, 'rb') as fp:
            self._buffer = fp.read()

        # get BA2 header immediately
        self._header = BA2Header(self._buffer)

    def __repr__(self) -> str:
        """ Builds a human readable string to represent the object.

        :returns: A human readable string to represent the object.
        """

        return (
            '<{self.__class__.__name__} "{self.filepath}" '
            '({self.header.file_count} files)>'
        ).format(**locals())

    def __len__(self) -> int:
        """ Returns the number of files in the BA2 archive.

        :returns: The number of fiels in the BA2 archive
        """

        return self.header.file_count

    @property
    def filepath(self) -> str:
        """ The filepath of the BA2 archive.

        :getter: Returns the filepath of the BA2 archive
        :setter: Sets the filepath of the BA2 archive
        """

        return self._filepath

    @filepath.setter
    def filepath(self, path: str) -> None:
        """ Sets the filepath of the BA2 archive.

        :param path: The new filepath of the BA2 archive
        :type path: str
        :returns: Does not return
        """

        if not os.path.isfile(path):
            raise FileNotFoundError((
                "no such file '{path}' exists"
            ).format(**locals()))
        self._filepath = path

    @property
    def header(self) -> BA2Header:
        """ The header of the BA2 archive.

        :getter: Returns the header of the BA2 archive
        :setter: Sets the header of the BA2 archive
        """

        return self._header

    @property
    def files(self) -> List[Union[BA2File, BA2TextureFile]]:
        """ The files within the BA2 archive.

        :getter: Discovers and returns the files within the BA2 archive
        :setter: Does not allow setting
        """

        if not hasattr(self, '_files'):
            self._files = []

            # get the necessary file object based on archive type
            # defaults to basic BA2File, if DX10 BA2TextureFile is used
            file_object = BA2File
            if self.header.type in (b'DX10',):
                file_object = BA2TextureFile

            # handle both buffer and name offsets at the same time
            buffer_offset = self.header._prefix_size
            name_offset = self.header.names_offset

            # iterate over the number of files as defined in the header
            for file_idx in range(self.header.file_count):
                # the length of the filepath is stored in a single byte
                # preceeding the filepath
                filepath_length = ord(self._buffer[
                    name_offset:(name_offset + 1)
                ])
                # account for the filepath length indicator and an
                # accompanying null byte
                name_offset += 2

                # get the filepath for the file object from the table at
                # the byte offset name_offset
                filepath = str(self._buffer[
                    name_offset:(name_offset + filepath_length)
                ], 'utf-8')

                # initialize the file object with both the buffer and the
                # filepath of the file
                file_ = file_object(self._buffer[buffer_offset:], filepath)
                # append the initialized file object to the archive's files
                self._files.append(file_)

                # increment buffer offset by specific count depending on
                # the archive type.
                #
                # GNRL archives should be incremented by the size of their
                # file prefix, otherwise the length of the file object
                # should be used
                buffer_offset += (
                    file_._prefix_size
                    if self.header.type in (b'GNRL',) else
                    len(file_)
                )
                # account for the read filepath in name_offset
                name_offset += filepath_length

        return self._files

    @classmethod
    def can_handle(cls, filepath: str) -> bool:
        """ Determines if a given filepath can be handled by this archive.

        :param filepath: The filepath of a potential BA2 archive
        :type filepath: str
        :returns: True if the archive can handle it, otherwise False
        """

        if not os.path.isfile(filepath):
            raise FileNotFoundError((
                "no such file '{filepath}' exists"
            ).format(**locals()))
        with open(filepath, 'rb') as fp:
            try:
                header = BA2Header(fp.read(
                    struct.calcsize(BA2Header._prefix_struct)
                ))
                # should be able to handle the archive its tagged as a BTDX
                # and is in the supported types GNRL and DX10
                return (
                    (header.ba2 == b'BTDX') and
                    (header.type in (b'GNRL', b'DX10',))
                )
            except struct.error as exc:
                # catch if it can't even unpack the header
                pass
        return False

    def _extract_gnrl(
        self,
        to_dir: str,
        progress_hook: Callable[[int, int, str], None]=None
    ) -> None:
        """ Helper extraction for extracting GNRL archvies.

        :param to_dir: The directory to extract files to
        :type to_dir: str
        :param progress_hook: A progress hook for the extraction process
        :type progress_hook: typing.Callable[[int, int, str], None]
        :returns: Does not return
        """

        total_count = len(self.files)
        for (file_idx, file_) in enumerate(self.files):
            # get the full path the file is going to be saved to
            to_path = os.path.join(to_dir, file_.filepath)
            file_dirpath = os.path.dirname(to_path)

            # if the full path's directory doesn't exist, create it
            if not os.path.isdir(file_dirpath):
                os.makedirs(file_dirpath)

            # if progress hook is enabled, report the progress
            if progress_hook:
                progress_hook((file_idx + 1), total_count, to_path)

            # write the archived file to the full path given the file
            # object's offset and size
            with open(to_path, 'wb') as fp:
                fp.write(self._buffer[
                    file_.offset:(file_.offset + file_.full_size)
                ])

    def _extract_dx10(
        self,
        to_dir: str,
        progress_hook: Callable[[int, int, str], None]=None
    ) -> None:
        """ Helper extraction for extracting DX10 archvies.

        .. tip:: Extraction implementation inspired from `BA2Lib \
            <https://github.com/digitalutopia1/BA2Lib/blob/master/BA2Lib/BA2.cpp>`_

        :param to_dir: The directory to extract files to
        :type to_dir: str
        :param progress_hook: A progress hook for the extraction process
        :type progress_hook: typing.Callable[[int, int, str], None]
        :returns: Does not return
        """

        total_count = len(self.files)
        for (file_idx, file_) in enumerate(self.files):
            # get the full path the file is going to be saved to
            to_path = os.path.join(to_dir, file_.filepath)
            file_dirpath = os.path.dirname(to_path)

            # if the full path's directory doesn't exist, create it
            if not os.path.isdir(file_dirpath):
                os.makedirs(file_dirpath)

            # if progress hook is enabled, report the progress
            if progress_hook:
                progress_hook((file_idx + 1), total_count, to_path)

            # DX10 requires that a DDSHeader is built
            dds_header = DDSHeader()
            # check out this giant mess...
            # intialize DDSHeader with valid flags and sizes
            dds_header.dwSize = ctypes.sizeof(DDSHeader)
            dds_header.dwFlags = (
                DDSFlags.DDS_HEADER_FLAGS_TEXTURE |
                DDSFlags.DDS_HEADER_FLAGS_LINEARSIZE |
                DDSFlags.DDS_HEADER_FLAGS_MIPMAP
            )
            dds_header.dwHeight = file_.height
            dds_header.dwWidth = file_.width
            dds_header.dwMipMapCount = file_.mipmap_count
            # XXX: unknown attribute usage (dwSurfaceFlags)
            # Not documented or anything, but used in BA2Lib... so why not?
            dds_header.dwSurfaceFlags = (
                DDSFlags.DDS_SURFACE_FLAGS_TEXTURE |
                DDSFlags.DDS_SURFACE_FLAGS_MIPMAP
            )
            # initalize the pixel format size before messing with it
            dds_header.ddspf.dwSize = ctypes.sizeof(DDSPixelFormat)

            try:
                # discover the dxgi format from the given file format
                dxgi_format = DXGIFormats(file_.format)

                # header configuration for bc1_unorm formats
                if dxgi_format == DXGIFormats.DXGI_FORMAT_BC1_UNORM:
                    dds_header.ddspf.dwFlags = DDSFlags.DDS_FOURCC
                    dds_header.ddspf.dwFourCC = fourcc(*'DXT1')
                    dds_header.dwPitchOrLinearSize = \
                        (file_.width * file_.height) // 2

                # header configuration for bc2_unorm formats
                elif dxgi_format == DXGIFormats.DXGI_FORMAT_BC2_UNORM:
                    dds_header.ddspf.dwFlags = DDSFlags.DDS_FOURCC
                    dds_header.ddspf.dwFourCC = fourcc(*'DXT3')
                    dds_header.dwPitchOrLinearSize = \
                        (file_.width * file_.height)

                # header configuration for bc3_unorm formats
                elif dxgi_format == DXGIFormats.DXGI_FORMAT_BC3_UNORM:
                    dds_header.ddspf.dwFlags = DDSFlags.DDS_FOURCC
                    dds_header.ddspf.dwFourCC = fourcc(*'DXT5')
                    dds_header.dwPitchOrLinearSize = \
                        (file_.width * file_.height)

                # header configuration for bc5_unorm formats
                elif dxgi_format == DXGIFormats.DXGI_FORMAT_BC5_UNORM:
                    dds_header.ddspf.dwFlags = DDSFlags.DDS_FOURCC
                    dds_header.ddspf.dwFourCC = fourcc(*'ATI2')
                    dds_header.dwPitchOrLinearSize = \
                        (file_.width * file_.height)

                # header configuration for bc7_unorm formats
                elif dxgi_format == DXGIFormats.DXGI_FORMAT_BC7_UNORM:
                    dds_header.ddspf.dwFlags = DDSFlags.DDS_FOURCC
                    dds_header.ddspf.dwFourCC = fourcc(*'BC7\x00')
                    dds_header.dwPitchOrLinearSize = \
                        (file_.width * file_.height)

                # header configuration for b8g8r8a8_unorm formats
                elif dxgi_format == DXGIFormats.DXGI_FORMAT_B8G8R8A8_UNORM:
                    dds_header.ddspf.dwFlags = DDSFlags.DDS_RGBA
                    dds_header.ddspf.dwRGBBitCount = 32
                    dds_header.ddspf.dwRBitMask = 0x00ff0000
                    dds_header.ddspf.dwGBitMask = 0x0000ff00
                    dds_header.ddspf.dwBBitMask = 0x000000ff
                    dds_header.ddspf.dwABitMask = 0xff000000
                    dds_header.dwPitchOrLinearSize = \
                        ((file_.width * file_.height) * 4)

                # header configuration for r8_unorm formats
                elif dxgi_format == DXGIFormats.DXGI_FORMAT_R8_UNORM:
                    dds_header.ddspf.dwFlags = DDSFlags.DDS_RGB
                    dds_header.ddspf.dwRGBBitCount = 8
                    dds_header.ddspf.dwRBitMask = 0x000000ff
                    dds_header.dwPitchOrLinearSize = \
                        (file_.width * file_.height)

                # unsupported formats caught and thrown at your face
                else:
                    raise NotImplementedError((
                        "unsupported dxgi format {dxgi_format}"
                    ).format(**locals()))

            # invalid format numbers detected should just be ignored...
            except ValueError as exc:
                pass

            with open(to_path, 'wb') as fp:
                # write out the DDS_MAGIC and the built header
                fp.write(struct.pack('<L', DDSFlags.DDS_MAGIC.value))
                fp.write(dds_header)

                # iterate over chunks for a given texture file
                for chunk_ in file_.chunks:
                    if chunk_.packed_size > 0:
                        # if the chunk is compressed, decompress up to the
                        # packed_size using zlib
                        fp.write(zlib.decompress(self._buffer[
                            chunk_.offset:(chunk_.offset + chunk_.packed_size)
                        ]))
                    else:
                        # just write the chunk out normally (no compression)
                        fp.write(self._buffer[
                            chunk_.offset:(chunk_.offset + chunk_.full_size)
                        ])

    def extract(
        self,
        to_dir: str,
        progress_hook: Callable[[int, int, str], None]=None
    ) -> None:
        """ Extracts the contents of the archive to a given directory.

        :param to_dir: The directory to extract files to
        :type to_dir: str
        :param progress_hook: A progress hook for the extraction process
        :type progress_hook: typing.Callable[[int, int, str], None]
        :returns: Does not return
        """

        # ensure the parent directory exists before trying to write to it
        if not os.path.isdir(to_dir):
            raise NotADirectoryError((
                "no such directory '{to_dir}' exists"
            ).format(**locals()))

        # handle two different extraction types for different archive types
        {
            b'GNRL': self._extract_gnrl,
            b'DX10': self._extract_dx10
        }[self.header.type](to_dir, progress_hook=progress_hook)
