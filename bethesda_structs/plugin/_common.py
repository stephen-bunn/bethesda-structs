# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://choosealicense.com/licenses/mit/>

import re
import abc
from typing import Any, Dict, List, Tuple, Union, Generic, TypeVar, Generator

import attr
from attr.validators import instance_of
from construct import Construct, Container, GreedyBytes
from multidict import CIMultiDict

from .. import exceptions
from .._common import BaseFiletype

T_BasePlugin = TypeVar("BasePlugin")
T_Subrecord = TypeVar("Subrecord")
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

        if not isinstance(value, list) or not all(
            isinstance(entry, str) and entry.upper() == entry for entry in value
        ):
            raise ValueError(
                f"forms must be a list of uppercase strings, recieved {value!r} "
                f"which is a {type(value)!r}"
            )


@attr.s
class Subrecord(object):
    """Defines a subrecord that can be further parsed using the supplied struct.
    """

    name = attr.ib(type=str, validator=instance_of(str))
    struct = attr.ib(type=Construct, repr=False, validator=instance_of(Construct))
    optional = attr.ib(type=bool, default=False, validator=instance_of(bool))
    multiple = attr.ib(type=bool, default=False, validator=instance_of(bool))
    _definition_regex = re.compile(r"\A(?P<name>\w{4})(?P<flag>[*+?]?)\Z")

    @name.validator
    def name_validator(self, attribute: str, value: str):
        """Ensures that the name attribute is valid.

        Args:
            attribute (str): The attribute name
            value (str): The attribute value

        Raises:
            ValueError:
                - When the name is not of length 4
        """

        if len(value) != 4:
            raise ValueError(
                (
                    f"name must be of length 4, recieved {value!r} with length "
                    f"{len(value)!r}"
                )
            )

    @classmethod
    def parse_flag(cls, flag: str) -> Tuple[bool, bool]:
        """Parses a given flag into a tuple for optional and multiple.

        Args:
            flag (str): The flag to parse

        Returns:
            Tuple[bool, bool]: A tuple containing the new (optional, multiple) booleans
        """

        assert flag in ("?", "*", "+", "")
        if flag != "":
            return ((flag in ("?", "*")), (flag in ("+", "*")))
        return (False, False)

    @classmethod
    def from_dict(cls, data: dict) -> T_Subrecord:
        """Builds a subrecord from a given dictionary.

        Args:
            data (dict): The dictionary to use

        Returns:
            T_Subrecord: A new instance of a subrecord
        """

        return cls(**data)

    @classmethod
    def from_definition(cls, definition: str, struct: Construct) -> T_Subrecord:
        """Builds a subrecord from a given definition.

        Args:
            definition (str): The definition to build from
            struct (Construct): The structure of the subrecord

        Returns:
            T_Subrecord: A new instance of a subrecord
        """

        config = cls._definition_regex.match(definition).groupdict()
        (is_optional, is_multiple) = cls.parse_flag(config["flag"])
        return Subrecord(
            config["name"], struct, optional=is_optional, multiple=is_multiple
        )

    def _build_flag(self) -> str:
        """Builds the definition flag for the current subrecord.

        Returns:
            str: The definition flag
        """

        flag = ""
        if self.optional:
            if self.multiple:
                flag = "*"
            else:
                flag = "?"
        else:
            if self.multiple:
                flag = "+"
        return flag

    def to_dict(self) -> dict:
        """Serializes the current subrecord as a dictionary.

        .. note:: Currently not JSON serializable due to structs requiring the use of
            lambda functions and self refrences.

        Returns:
            dict: The resulting dictionary.
        """

        # XXX: cannot serialize Struct instances (typically includes lambda expressions)
        return attr.asdict(self)

    def to_definition(self) -> Tuple[str, Construct]:
        """Returns the definition of the subrecord.

        Returns:
            Tuple[str, Construct]: The definition, a tuple of (definition, struct)
        """

        return (f"{self.name}{self._build_flag()}", self.struct)

    def be(self, flag: str) -> T_Subrecord:
        """Set the optional and multiple arguments.

        Args:
            flag (str): The flag to set for the current collection

        Returns:
            T_Subrecord: The current subrecord
        """

        (self.optional, self.multiple) = self.parse_flag(flag)
        return self


@attr.s
class SubrecordCollection(object):
    """Defines a collection of subrecords.
    """

    name = attr.ib(type=str, validator=instance_of(str))
    items = attr.ib(
        type=list, default=attr.Factory(list), repr=False, validator=instance_of(list)
    )
    optional = attr.ib(type=bool, default=False, validator=instance_of(bool))
    multiple = attr.ib(type=bool, default=False, validator=instance_of(bool))
    _definition_regex = re.compile(r"\A(?P<name>\w+)(?P<flag>[*+?]?)\Z")

    @items.validator
    def items_validator(self, attribute: str, value: list):
        """Ensures that the items attribute is valid.

        Args:
            attribute (str): The attribute name
            value (list): The attribute value

        Raises:
            ValueError:
                - When the length of the items is not greater than 0
            TypeError:
                - When not all of the items within the list are not of instance
                    Subrecord or SubrecordCollection
        """

        if len(value) <= 0:
            raise ValueError(
                (
                    f"items must contain at least one subrecord, "
                    f"recieved {value!r} with length {len(value)!r}"
                )
            )
        if not all(isinstance(item, (Subrecord, self.__class__)) for item in value):
            raise TypeError(
                (
                    f"items can only be instances of {Subrecord!r} or "
                    f"{SubrecordCollection!r}"
                )
            )

    @classmethod
    def parse_flag(cls, flag: str) -> Tuple[bool, bool]:
        """Parses a given flag into a tuple for optional and multiple.

        Args:
            flag (str): The flag to parse

        Returns:
            Tuple[bool, bool]: A tuple containing the new (optional, multiple) booleans
        """

        assert flag in ("?", "*", "+", "")
        if flag != "":
            return ((flag in ("?", "*")), (flag in ("+", "*")))
        return (False, False)

    @classmethod
    def from_dict(cls, data: dict) -> T_SubrecordCollection:
        """Builds a subrecord collection from a given dictionary.

        Args:
            data (dict): The dictionary to use

        Returns:
            T_SubrecordCollection: A new instance of a collection
        """
        # NOTE: PEP-448 dictionary unpacking emulates deepcopy
        data = {**data}
        data["items"] = [
            SubrecordCollection.from_dict(item)
            if "items" in item
            else Subrecord.from_dict(item)
            for item in data.get("items", [])
        ]
        return cls(**data)

    @classmethod
    def from_definition(cls, definition: str, data: list) -> T_SubrecordCollection:
        """Builds a subrecord collection from a given definition.

        Args:
            definition (str): The definition to build from
            data (list): The data of the definition

        Returns:
            T_SubrecordCollection: A new instance of a SubrecordCollection
        """
        config = cls._definition_regex.match(definition).groupdict()
        items = []
        for (sub_definition, value) in data:
            if isinstance(value, Construct):
                items.append(Subrecord.from_definition(sub_definition, value))
            elif isinstance(value, list):
                items.append(cls.from_definition(sub_definition, value))
        (is_optional, is_multiple) = cls.parse_flag(config["flag"])
        return cls(config["name"], items, optional=is_optional, multiple=is_multiple)

    def _build_flag(self) -> str:
        """Builds the definition flag for the current collection.

        Returns:
            str: The definition flag
        """
        flag = ""
        if self.optional:
            if self.multiple:
                flag = "*"
            else:
                flag = "?"
        else:
            if self.multiple:
                flag = "+"
        return flag

    def _lookahead(self, items: list, target: str) -> Subrecord:
        """Returns the first subrecord in a list of items that matches the given target.

        Args:
            items (list): The list of items to use
            target (str): The target to serach for

        Returns:
            Subrecord: The first matching subrecord, or None
        """
        for item in items:
            if isinstance(item, Subrecord):
                if item.name == target:
                    return item
            elif isinstance(item, self.__class__):
                result = self._lookahead(item.items, target)
                if result:
                    return result

    def _parse(  # noqa: C901
        self, names: list, strict: bool = True, level: int = 0
    ) -> Tuple[list, int]:
        """Parses a given list of names to determine what subrecords to expect next.

        Args:
            names (list): A list of names to parse
            strict (bool, optional): Defaults to True. Enables strict parsing
            level (int, optional): Defaults to 0. The recursion level
                (for nested collections)

        Raises:
            exceptions.UnexpectedSubrecord:
                - When item is required but names does not exist
                - When name is unexpected
                - When name repeats but item does not expect multiple occurances

        Returns:
            Tuple[list, int]: A tuple of subrecords and collections to expect and
                name index reached
        """
        (item_idx, name_idx) = (0, 0)
        results = []

        while True:
            try:
                item = self.items[item_idx]
                name = names[name_idx]
            except IndexError:
                return (results + self.items[item_idx:], name_idx)

            if isinstance(item, Subrecord):
                if item.name == name:
                    if not item.multiple:
                        item_idx += 1
                    name_idx += 1
                else:
                    if strict:
                        # raise errors on incorrect ordering
                        previous_name_idx = (abs(name_idx - 1) + (name_idx - 1)) // 2
                        previous_item_idx = (abs(item_idx - 1) + (item_idx - 1)) // 2
                        previous_name = names[previous_name_idx]
                        previous_item = self.items[previous_item_idx]
                        # TODO: rethink some of this error detection logic
                        if name == previous_item.name and not previous_item.multiple:
                            raise exceptions.UnexpectedSubrecord(
                                f"{previous_item!r} cannot repeat for {self!r}"
                            )
                        elif not item.optional and not (
                            item.multiple and previous_name == item.name
                        ):
                            raise exceptions.UnexpectedSubrecord(
                                f"{item!r} is required for {self!r}"
                            )
                        else:
                            if not self._lookahead(self.items[item_idx:], name):
                                raise exceptions.UnexpectedSubrecord(
                                    f"{name!r} is not expected for {self!r}"
                                )
                    item_idx += 1
            elif isinstance(item, self.__class__):
                if item._lookahead(item.items, name):
                    (nested, idx) = item._parse(
                        names[name_idx:], strict=strict, level=(level + 1)
                    )
                    results.extend(nested)
                    if item.multiple:
                        results.append(item)
                    name_idx += idx
                item_idx += 1

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the current collection as a dictionary.

        .. note:: Not JSON serializable due to structs requiring lambda functions
            and self references.

        Returns:
            Dict[str, Any]: The resulting dictionary
        """

        result = attr.asdict(self)
        result["items"] = [item.to_dict() for item in self.items]
        return result

    def to_definition(self) -> Tuple[str, list]:
        """Returns the definition of the collection.

        Returns:
            Tuple[str, list]: The definition instance
        """

        return (
            f"{self.name}{self._build_flag()}",
            [_.to_definition() for _ in self.items],
        )

    def be(self, flag: str) -> T_SubrecordCollection:
        """Set the optional and multiple arguments.

        Args:
            flag (str): Teh flag to set for the current collection

        Returns:
            T_SubrecordCollection: The current subrecord collection
        """

        (self.optional, self.multiple) = self.parse_flag(flag)
        return self

    def discover(self, names: list, target: str, strict: bool = True) -> Subrecord:
        """Discovers the next expected subrecord given a target.

        Args:
            names (list): The previously discovered subrecord names
            target (str): The target to discover next
            strict (bool, optional): Defaults to True. Enforce that required subrecords
                should appear before the target

        Raises:
            exceptions.UnexpectedSubrecord:
                - When nothing is expected next but target requested
                - When requested target does not match next expected subrecord

        Returns:
            Subrecord: The resulting discovered subrecord, or None
        """

        def handle_strict(items: list, target: str):
            if len(items) <= 0:
                raise exceptions.UnexpectedSubrecord(
                    f"nothing is expected next, asked for {target!r}"
                )
            for item in items:
                if isinstance(item, Subrecord):
                    if item.name != target:
                        if not item.optional:
                            if item.multiple and (
                                len(names) > 0 and names[-1] == item.name
                            ):
                                continue
                            raise exceptions.UnexpectedSubrecord(
                                f"{item!r} is expected next, asked for {target!r}"
                            )
                    else:
                        return item
                elif isinstance(item, self.__class__):
                    if not item.optional or self._lookahead(item.items, target):
                        result = handle_strict(item.items, target)
                        if result:
                            return result

        (rest, _) = self._parse(names, strict=strict)
        if strict:
            # apply post-parsing ordering enforcement
            handle_strict(rest, target)
        return self._lookahead(rest, target)

    def handle_working(
        self,
        subrecord_name: str,
        subrecord_data: bytes,
        working_record: list,
        strict: bool = True,
    ) -> Tuple[Container, List[str]]:
        """Handles discovering and parsing a given subrecord using a list of already
            handled subrecord names.

        Note:
            Subrecords that cannot be correctly discovered by the collection's discovery
            process utilize a default ``GreedyBytes * "Not Handled`` struct.
            So any subrecord that cannot be discovered correctly or isn't handled
            correctly with simply be a Container with a ``value`` that matches the
            subrecord's data and a ``description`` of ``Not Handled``.

        Args:
            subrecord_name (str): The name of the subrecord to discover and parse
            subrecord_data (bytes): The data of the subrecord to discover and parse
            working_record (list): The list of names that have already been handled in
                the working record
            strict (bool): Defaults to True, If True, enforce strict discovery

        Returns:
            Tuple[Container, List[str]]: A tuple of
                (parsed container, new handled names to extend the working record with)
        """

        subrecord_name = subrecord_name.upper()
        discovered = self.discover(working_record, subrecord_name, strict=strict)
        subrecord_struct = GreedyBytes * "Not Handled"
        if isinstance(discovered, Subrecord):
            subrecord_struct = discovered.struct
        parsed = Container(
            value=subrecord_struct.parse(subrecord_data),
            description=subrecord_struct.docs,
        )
        return (parsed, [subrecord_name])


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
    def parse(cls, content: bytes, filepath: str = None) -> T_BasePlugin:
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
