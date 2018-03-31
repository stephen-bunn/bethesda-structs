# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import io
import abc
from typing import (TypeVar, Generic, Union, Any, Dict, List, Tuple,)

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
class Subrecord(object):
    """Defines a the structure of a subrecord.
    """

    name = attr.ib(type=str, converter=str.upper)
    structure = attr.ib(
        type=Construct,
        validator=attr.validators.instance_of(Construct)
    )
    optional = attr.ib(type=bool, default=False)
    multiple = attr.ib(type=bool, default=False)


T_SubrecordCollection = TypeVar('SubrecordCollection')


@attr.s
class SubrecordCollection(Generic[T_SubrecordCollection]):
    """Defines a collection of subrecord structures.
    """

    subrecords = attr.ib(
        type=List[Union[Subrecord, T_SubrecordCollection]],
        default=attr.Factory(list)
    )
    optional = attr.ib(type=bool, default=False)
    multiple = attr.ib(type=bool, default=False)

    def _flatten_collection(
        self,
        collection: T_SubrecordCollection
    ) -> CIMultiDict:
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

    def be(
        self,
        optional: bool=None,
        multiple: bool=None
    ) -> T_SubrecordCollection:
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
        working_record: Dict[str, int]=None
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
        value_structure = GreedyBytes * 'Not Handled'
        try:
            subrecord_structure = flat_collection[(
                working_record.get(subrecord_name, 0) % len(flat_collection)
            )]
            if subrecord_name not in working_record:
                working_record[subrecord_name] = 0
            working_record[subrecord_name] += 1

            value_structure = subrecord_structure.structure
        except IndexError:
            pass

        parsed_container = Container(
            value=value_structure.parse(subrecord_data),
            description=value_structure.docs
        )

        return (parsed_container, working_record)


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
