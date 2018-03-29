# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import io
import abc
from typing import (Any, Union, List,)

import attr
from construct import (Construct, Container, GreedyBytes,)
from multidict import CIMultiDict


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
            isinstance(entry, str) and entry.upper() == entry
            for entry in value
        ):
            raise ValueError((
                f"forms must be a list of uppercase strings, "
                f"recieved {value!r} which is a {type(value)!r}"
            ))


@attr.s
class SubrecordStructure(object):
    """Defines a the structure of a subrecord.
    """

    name = attr.ib(type=str, converter=str.upper)
    structure = attr.ib(
        type=Construct,
        validator=attr.validators.instance_of(Construct)
    )
    optional = attr.ib(type=bool, default=False)
    multiple = attr.ib(type=bool, default=False)


@attr.s
class SubrecordCollection(object):
    """Defines a collection of subrecord structures.
    """

    subrecords = attr.ib(
        type=List[SubrecordStructure],
        default=attr.Factory(list)
    )
    optional = attr.ib(type=bool, default=False)
    multiple = attr.ib(type=bool, default=False)

    @subrecords.validator
    def validate(self, attribute: str, value: Any):
        """Validates subrecords.

        Args:
            attribute (str): Should always be ``subrecords``
            value (Any): Should be a list of ``SubrecordStructure``
        """

        if not isinstance(value, list) or not all(
            isinstance(entry, SubrecordStructure)
            for entry in value
        ):
            raise ValueError((
                f"subrecords must be a list of SubrecordStructure, "
                f"recieved {value!r} which is a {type(value)!r}"
            ))


@attr.s
class RecordSubrecords(object):
    """Defines a record's subrecord structures.
    """

    subrecords = attr.ib(
        type=List[Union[SubrecordStructure, SubrecordCollection]],
        default=attr.Factory(list)
    )

    @subrecords.validator
    def validate(self, attribute: str, value: Any):
        """Validates subrecords.

        Args:
            attribute (str): Should always be ``subrecords``
            value (Any): Should be a list of ``SubrecordStructure`` or
                ``SubrecordCollection``
        """

        if not isinstance(value, list) or not all(
            isinstance(entry, (SubrecordStructure, SubrecordCollection))
            for entry in value
        ):
            raise ValueError((
                f"subrecords must be a list of SubrecordStructure, "
                f"recieved {value!r} which is a {type(value)!r}"
            ))

    def handle(self, subrecord_type: str, subrecord_data: bytes) -> Container:
        """Handles the parsing of a subrecord's data.

        Args:
            subrecord_type (str): The type of the subrecord
            subrecord_data (bytes): The data of a subrecrod

        Returns:
            Container: The resulting container
                (should contain ``value`` and ``description`` fields at least)
        """

        def handle_collection(
            collection: Any,
            subrecord_type: str
        ) -> Construct:
            """Handles discovery with a sequence of ``SubrecordStructures``.

            Args:
                collection (Any): The collection to use
                    (``RecordSubrecords`` or ``SubrecordCollection``)
                subrecord_type (str): The type of subrecord to discover

            Returns:
                Construct: The structure to use for parsing subrecord data
            """

            for subrecord_structure in collection.subrecords:
                if isinstance(subrecord_structure, SubrecordStructure) and \
                        subrecord_structure.name == subrecord_type:
                    return subrecord_structure.structure
                elif isinstance(subrecord_structure, SubrecordCollection):
                    return handle_collection(
                        subrecord_structure,
                        subrecord_type
                    )

            return (GreedyBytes * 'Not Handled')

        value_structure = handle_collection(self, subrecord_type)
        return Container(
            value=value_structure.parse(subrecord_data),
            description=value_structure.docs
        )


class BasePlugin(abc.ABC, Construct):
    """The base class all Plugins should subclass.
    """

    record_registry = CIMultiDict()

    @abc.abstractproperty
    def plugin_struct(self) -> Construct:
        """The base plugin structure to use for parsing a plugin.

        Returns:
            Construct: The plugin structure
        """

        raise NotImplementedError

    @abc.abstractclassmethod
    def can_handle(cls, filepath: str) -> bool:
        """Determines if a given `filepath` can be handled by the plugin.

        Args:
            filepath (str): The filepath to evaluate

        Raises:
            NotImplementedError: Subclasses must define the logic

        Returns:
            bool: True if the `filepath` can be handled, otherwise False
        """

        raise NotImplementedError

    def _parse(
        self,
        stream: io.BufferedReader,
        context: Container,
        path: str
    ) -> Container:
        """Parses the given stream using the plugin struct.

        Args:
            stream (io.BufferedReader): The stream of bytes to parse
            context (Container): The contextual container to use
            path (str): The construct path

        Returns:
            Container: The resulting parsed container
        """

        return self.plugin_struct._parse(stream, context, path)

    def _build(
        self,
        obj: Construct,
        stream: io.BufferedWriter,
        context: Container,
        path: str
    ) -> bytes:
        """Builds a given `obj` using the given `stream`.

        Args:
            obj (Construct): The construct to build
            stream (io.BufferedWriter): The stream to build the given `obj`
            context (Container): The contextual container to use
            path (str): The construct path

        Raises:
            NotImplementedError: Is not currently supported

        Returns:
            bytes: The resulting built bytes
        """

        raise NotImplementedError(
            f"{self!r} does not currently support building plugins"
        )
