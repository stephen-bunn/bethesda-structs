# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://choosealicense.com/licenses/mit/>

import io
import os
import abc
from typing import Any, Dict, List, Tuple, Union, Generic, TypeVar, Generator

import attr
from construct import Construct, Container, GreedyBytes
from multidict import CIMultiDict

from .._common import BaseFiletype

T_BasePlugin = TypeVar("BasePlugin")
T_SubrecordCollection = TypeVar("SubrecordCollection")


@attr.s
class FormID(object):
    """The standardized form id object.

    Raises:
        ValueError: If forms is not a list of uppercase strings
    """

    form_id = attr.ib(type=int)
    forms = attr.ib(type=List[str], default=attr.Factory(list))

    @forms.validator
    def validate(self, attribute: str, value: Any):
        """Validates forms.

        Args:
            attribute (str): Should always be ``forms``
            value (Any): Should be a list of uppercase strings

        Raises:
            ValueError: If `value` is not a list
            ValueError: If all entries in `value` are not uppercase strings
        """

        if (
            not isinstance(value, list)
            or not all(
                isinstance(entry, str) and entry.upper() == entry for entry in value
            )
        ):
            raise ValueError(
                f"forms must be a list of uppercase strings, recieved {value!r} "
                f"which is a {type(value)!r}"
            )


@attr.s
class Subrecord(object):
    """Defines a the structure of a subrecord.
    """

    name = attr.ib(type=str, converter=str.upper)
    structure = attr.ib(
        type=Construct, validator=attr.validators.instance_of(Construct)
    )
    optional = attr.ib(type=bool, default=False)
    multiple = attr.ib(type=bool, default=False)


@attr.s
class SubrecordCollection(Generic[T_SubrecordCollection]):
    """Defines a collection of subrecord structures.
    """

    subrecords = attr.ib(
        type=List[Union[Subrecord, T_SubrecordCollection]], default=attr.Factory(list)
    )
    optional = attr.ib(type=bool, default=False)
    multiple = attr.ib(type=bool, default=False)

    def _flatten_collection(self, collection: T_SubrecordCollection) -> CIMultiDict:
        """Flattens the collection to a case insensitive multidict.

        Args:
            collection (T_SubrecordCollection): The collection to flatten

        Returns:
            CIMultiDict: The resulting multidict
        """

        flat = CIMultiDict()
        for entry in collection.subrecords:
            if isinstance(entry, Subrecord):
                flat.add(entry.name, entry)
            elif isinstance(entry, SubrecordCollection):
                flat.extend(self._flatten_collection(entry))
        return flat

    def be(self, optional: bool = None, multiple: bool = None) -> T_SubrecordCollection:
        """Modifies the operation of a collection in place.

        Args:
            optional (bool, optional): Defaults to None. Modifies the
                optional field
            multiple (bool, optional): Defaults to None. Updates the
                multiple field

        Returns:
            T_SubrecordCollection: The collection the updates were applied to
        """

        if isinstance(optional, bool):
            self.optional = optional
        if isinstance(multiple, bool):
            self.multiple = multiple
        return self

    def handle_subrecord(
        self,
        subrecord_name: str,
        subrecord_data: bytes,
        working_record: Dict[str, int] = None,
    ) -> Tuple[Dict[str, int], Container]:
        """Handles the desconstruction of a given subrecord.

        Args:
            subrecord_name (str): The type of the subrecord
            subrecord_data (bytes): The data of the subrecord
            working_record (Dict[str, int], optional): Defaults to None. The
                working record dictionary (used for better determination of
                what structure to use)

        Returns:
            Tuple[Dict[str, int], Container]: A tuple of the updated
                `working_record` context and the deconstructed ``Collection``
        """

        subrecord_name = subrecord_name.upper()
        if working_record is None:
            working_record = {}

        # FIXME: currently this is a VERY naive way of determining which
        # subrecord structure to use. This should be updated to also take
        # advantage of the `optional` and `multiple` fields given to the
        # Subrecord and SubrecordCollection instances
        flat_collection = self._flatten_collection(self).getall(subrecord_name)
        value_structure = GreedyBytes * "Not Handled"
        try:
            subrecord_structure = flat_collection[
                (working_record.get(subrecord_name, 0) % len(flat_collection))
            ]
            if subrecord_name not in working_record:
                working_record[subrecord_name] = 0
            working_record[subrecord_name] += 1

            value_structure = subrecord_structure.structure
        except IndexError:
            pass

        parsed_container = Container(
            value=value_structure.parse(subrecord_data),
            description=value_structure.docs,
        )

        return (parsed_container, working_record)


@attr.s
class BasePlugin(BaseFiletype, abc.ABC, Generic[T_BasePlugin]):
    """The base class all Plugins should subclass.
    """

    content = attr.ib(type=bytes, repr=False)
    filepath = attr.ib(type=str, default=None)
    record_registry = attr.ib(type=CIMultiDict, default=CIMultiDict(), repr=False)

    @abc.abstractproperty
    def plugin_struct(self) -> Construct:
        """The base plugin structure to use for parsing a plugin.

        Returns:
            Construct: The plugin structure
        """
        raise NotImplementedError

    @property
    def container(self) -> Container:
        if not hasattr(self, "_container"):
            self._container = self.plugin_struct.parse(self.content)
        return self._container

    @classmethod
    def parse_bytes(cls, content: bytes, filepath: str = None) -> T_BasePlugin:
        """Create a `BasePlugin` from a byte array.

        Args:
            content (bytes): The byte content of the archive
            filepath (str, optional): Defaults to None. Sets the filepath attribute for
                user's reference

        Raises:
            ValueError: If the given content is not of bytes

        Returns:
            T_BasePlugin: A created `BasePlugin`
        """
        if not isinstance(content, bytes):
            raise ValueError(
                f"given content must be of bytes, recieved {type(content)!r}"
            )

        return cls(content, filepath=filepath)

    @classmethod
    def parse_stream(
        cls, stream: io.BufferedReader, filepath: str = None
    ) -> T_BasePlugin:
        """Create a `BasePlugin` from a file stream.

        Args:
            stream (io.BufferedReader): A file stream to read from.
            filepath (str, optional): Defaults to None. Sets the filepath attribute for
                user's reference.

        Raises:
            ValueError: If the given stream is not of ``bytes``

        Returns:
            T_BasePlugin: A created `BasePlugin`
        """
        if not isinstance(stream.peek(1), bytes):
            raise ValueError(
                f"stream {stream!r} is not a stream of bytes, recieved {type(stream)!r}"
            )

        return cls.parse_bytes(stream.read(), filepath=filepath)

    @classmethod
    def parse_file(cls, filepath: str) -> T_BasePlugin:
        """Create a `BasePlugin` from a given filepath.

        Args:
            filepath (str): The filepath to read from

        Raises:
            FileNotFoundError: If the given filepath does not exist

        Returns:
            T_BasePlugin: A created `BasePlugin`
        """
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"no such file '{filepath!r}' exists")

        with open(filepath, "rb") as stream:
            return cls.parse_stream(stream, filepath)

    def iter_records(
        self, record_type: str = None, include_header: bool = False
    ) -> Generator[Container, None, None]:
        """Iterates over the container's records.

            record_type (str, optional): Defaults to None. Filters the record types to
                yield
            include_header (bool, optional): Defaults to False. Includes the header
                record (regardless of ``record_type``)

        Yields:
            Container: A record's container
        """

        def iter_group_records(
            group: Container, record_type: str = None
        ) -> Generator[Container, None, None]:
            """Iterates over a group's records.

            Args:
                group (Container): The group to iterate the records of
                record_type (str, optional): Defaults to None. Filters the record types
                    to yield

            Yields:
                Container: A record's container
            """

            if group.records is not None:
                for record in group.records:
                    if (
                        isinstance(record_type, str)
                        and record_type != record.type.upper()
                    ):
                        continue

                    yield record

            elif group.subgroups is not None:
                for subgroup in group.subgroups:
                    for record in iter_group_records(subgroup, record_type=record_type):
                        yield record

        if isinstance(record_type, str):
            record_type = record_type.upper()

        if include_header:
            # NOTE: yields header regardless of ``record_type`` value
            yield self.container.header

        for group in self.container.groups:
            for record in iter_group_records(group, record_type=record_type):
                yield record

    def iter_subrecords(
        self,
        subrecord_type: str = None,
        record_type: str = None,
        include_header: bool = False,
    ) -> Generator[Container, None, None]:
        """Iterates over the container's subrecords.

            subrecord_type (str, optional): Defaults to None. Filters the subrecord
                types to yield
            record_type (str, optional): Defaults to None. Filters the record types to
                look for subrecords in
            include_header (bool, optional): Defaults to False. Includes the header
                record in the filter (regardless of ``record_type``)

        Yields:
            Container: A subrecord's container
        """

        if isinstance(subrecord_type, str):
            subrecord_type = subrecord_type.upper()
        for record in self.iter_records(record_type, include_header=include_header):
            for subrecord in record.subrecords:
                if (
                    isinstance(subrecord_type, str)
                    and subrecord_type != subrecord.type.upper()
                ):
                    continue

                yield subrecord
