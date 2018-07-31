# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://opensource.org/licenses/MIT>

import random
from typing import List

import pytest
from construct import Struct
from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import (
    none,
    nothing,
    text,
    one_of,
    lists,
    booleans,
    integers,
    from_type,
    sampled_from,
)

from . import (
    random_base_type,
    subrecord_collection_items,
    subrecord_collection,
    subrecord_collection_definition,
    subrecord_collection_dict,
)
from bethesda_structs import exceptions
from bethesda_structs.plugin._common import Subrecord, SubrecordCollection


def _flatten_subrecords(collection: SubrecordCollection) -> List[str]:
    results = []
    for item in collection.items:
        if isinstance(item, Subrecord):
            results.append(item)
        elif isinstance(item, SubrecordCollection):
            results.extend(_flatten_subrecords(item))
    return results


@given(
    text(min_size=1), subrecord_collection_items(), booleans(), booleans()
)
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_init(name, items, optional, multiple):
    subc = SubrecordCollection(name, items, optional=optional, multiple=multiple)
    assert isinstance(subc, SubrecordCollection)
    assert subc.name == name
    assert subc.items == items
    assert subc.optional == optional
    assert subc.multiple == multiple


@given(
    random_base_type(ignore=[str]),
    subrecord_collection_items(),
    booleans(),
    booleans(),
)
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_invalid_name(name, items, optional, multiple):
    if not isinstance(name, str):
        with pytest.raises(TypeError):
            SubrecordCollection(name, items, optional, multiple)


@given(
    text(min_size=1),
    one_of(random_base_type(ignore=[list]), lists(none())),
    booleans(),
    booleans(),
)
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_invalid_items(name, items, optional, multiple):
    if isinstance(items, list) and len(items) <= 0:
        with pytest.raises(ValueError):
            SubrecordCollection(name, items, optional, multiple)
    else:
        with pytest.raises(TypeError):
            SubrecordCollection(name, items, optional, multiple)


@given(
    text(min_size=1),
    subrecord_collection_items(),
    random_base_type([bool]),
    booleans(),
)
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_invalid_optional(name, items, optional, multiple):
    with pytest.raises(TypeError):
        SubrecordCollection(name, items, optional, multiple)


@given(
    text(min_size=1),
    subrecord_collection_items(),
    booleans(),
    random_base_type([bool]),
)
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_invalid_multiple(name, items, optional, multiple):
    with pytest.raises(TypeError):
        SubrecordCollection(name, items, optional, multiple)


@given(subrecord_collection_definition())
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_from_definition(definition):
    subc = SubrecordCollection.from_definition(*definition)
    assert isinstance(subc, SubrecordCollection)
    assert definition[0].startswith(subc.name)
    assert [item.to_definition() for item in subc.items] == definition[-1]
    if definition[0][-1] in ("*", "+", "?"):
        (optional, multiple) = SubrecordCollection.parse_flag(definition[0][-1])
        assert subc.optional == optional
        assert subc.multiple == multiple
    else:
        assert not subc.optional
        assert not subc.multiple


@given(subrecord_collection_dict())
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_from_dict(dictionary):
    subc = SubrecordCollection.from_dict(dictionary)
    assert isinstance(subc, SubrecordCollection)
    assert subc.name == dictionary["name"]
    assert subc.items == [
        SubrecordCollection.from_dict(item)
        if "items" in item
        else Subrecord.from_dict(item)
        for item in dictionary["items"]
    ]
    assert subc.optional == dictionary["optional"]
    assert subc.multiple == dictionary["multiple"]


@given(subrecord_collection_definition())
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_to_definition(definition):
    subc = SubrecordCollection.from_definition(*definition)
    assert isinstance(subc, SubrecordCollection)
    assert subc.to_definition() == definition


@given(subrecord_collection_dict())
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_to_dict(dictionary):
    subc = SubrecordCollection.from_dict(dictionary)
    assert isinstance(subc, SubrecordCollection)
    assert subc.to_dict() == dictionary


@given(subrecord_collection())
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_build_flag(collection):
    flag = collection._build_flag()
    assert flag in ("+", "?", "*", "")
    if collection.multiple:
        if collection.optional:
            assert flag == "*"
        else:
            assert flag == "+"
    else:
        if collection.optional:
            assert flag == "?"
        else:
            assert flag == ""


@given(subrecord_collection(), sampled_from(["+", "?", "*", ""]))
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_be(collection, flag):
    (optional, multiple) = SubrecordCollection.parse_flag(flag)
    subc = collection.be(flag)
    assert isinstance(subc, SubrecordCollection)
    assert subc.name == collection.name
    assert subc.items == collection.items
    assert subc.optional == optional
    assert subc.multiple == multiple


@given(subrecord_collection())
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_lookahead(collection):
    flat_subr = _flatten_subrecords(collection)
    target_idx = random.randint(0, len(flat_subr) - 1)
    target = flat_subr[target_idx]

    lookahead = collection._lookahead(collection.items, target.name)
    assert isinstance(lookahead, Subrecord)
    assert lookahead.name == target.name


@given(subrecord_collection())
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_parse(collection):
    flat_subr = _flatten_subrecords(collection)
    target_idx = random.randint(0, len(flat_subr) - 1)

    names = [subr.name for subr in flat_subr]
    (parsed, parsed_idx) = collection._parse(names[:target_idx], strict=False)
    assert isinstance(parsed, list)
    assert all([isinstance(subr, (Subrecord, SubrecordCollection)) for subr in parsed])
    assert isinstance(parsed_idx, int)
    assert parsed_idx >= 0


@given(subrecord_collection(min_count=2))
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_discover(collection):
    flat_subr = _flatten_subrecords(collection)
    target_idx = random.randint(0, len(flat_subr) - 2)

    names = [subr.name for subr in flat_subr[:target_idx]]
    target = flat_subr[target_idx]
    discovered = collection.discover(names, target.name, strict=False)
    assert discovered.name == target.name


def test_discover_first():
    definition = ("TEST", [("AAAA", Struct())])
    collection = SubrecordCollection.from_definition(*definition)

    discovered = collection.discover([], "AAAA")
    assert isinstance(discovered, Subrecord)
    assert discovered.name == "AAAA"


def test_discover_required():
    definition = ("TEST", [("AAAA", Struct()), ("BBBB", Struct())])
    collection = SubrecordCollection.from_definition(*definition)

    with pytest.raises(exceptions.UnexpectedSubrecord):
        collection.discover([], "BBBB")


def test_discover_optional():
    definition = ("TEST", [("AAAA?", Struct()), ("BBBB", Struct())])
    collection = SubrecordCollection.from_definition(*definition)

    discovered = collection.discover([], "AAAA")
    assert isinstance(discovered, Subrecord)
    assert discovered.name == "AAAA"

    discovered = collection.discover([], "BBBB")
    assert isinstance(discovered, Subrecord)
    assert discovered.name == "BBBB"


@given(integers(min_value=1, max_value=100))
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_discover_multiple(multiple_scale):
    definition = ("TEST", [("AAAA+", Struct()), ("BBBB", Struct())])
    collection = SubrecordCollection.from_definition(*definition)

    discovered = collection.discover([], "AAAA")
    assert isinstance(discovered, Subrecord)
    assert discovered.name == "AAAA"

    discovered = collection.discover(["AAAA"] * multiple_scale, "AAAA")
    assert isinstance(discovered, Subrecord)
    assert discovered.name == "AAAA"

    with pytest.raises(exceptions.UnexpectedSubrecord):
        collection.discover([], "BBBB")


def test_discover_none():
    definition = ("TEST", [("AAAA", Struct()), ("BBBB", Struct())])
    collection = SubrecordCollection.from_definition(*definition)

    with pytest.raises(exceptions.UnexpectedSubrecord):
        collection.discover(["AAAA", "BBBB"], "AAAA")

    with pytest.raises(exceptions.UnexpectedSubrecord):
        collection.discover(["AAAA", "BBBB"], "BBBB")


def test_discover_nested_first():
    definition = ("TEST", [("AAAA", Struct()), ("BBBB", [("CCCC", Struct())])])
    collection = SubrecordCollection.from_definition(*definition)

    discovered = collection.discover(["AAAA"], "CCCC")
    assert isinstance(discovered, Subrecord)
    assert discovered.name == "CCCC"

    definition = (
        "TEST",
        [("AAAA", Struct() * "0"), ("BBBB", [("AAAA", Struct() * "1")])],
    )
    collection = SubrecordCollection.from_definition(*definition)

    discovered = collection.discover(["AAAA"], "AAAA")
    assert isinstance(discovered, Subrecord)
    assert discovered.name == "AAAA"
    assert discovered.struct.docs == "1"


def test_discover_nested_required():
    definition = (
        "TEST",
        [("AAAA", Struct()), ("BBBB", [("CCCC", Struct()), ("DDDD", Struct())])],
    )
    collection = SubrecordCollection.from_definition(*definition)

    with pytest.raises(exceptions.UnexpectedSubrecord):
        collection.discover(["AAAA"], "DDDD")


def test_discover_nested_optional():
    definition = (
        "TEST",
        [("AAAA", Struct()), ("BBBB", [("CCCC?", Struct()), ("DDDD", Struct())])],
    )
    collection = SubrecordCollection.from_definition(*definition)

    discovered = collection.discover(["AAAA"], "DDDD")
    assert isinstance(discovered, Subrecord)
    assert discovered.name == "DDDD"


@given(integers(min_value=1, max_value=100))
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_discover_nested_multiple(multiple_scale):
    definition = (
        "TEST",
        [("AAAA", Struct()), ("BBBB+", [("CCCC", Struct()), ("DDDD", Struct())])],
    )
    collection = SubrecordCollection.from_definition(*definition)

    discovered = collection.discover(["AAAA"], "CCCC")
    assert isinstance(discovered, Subrecord)
    assert discovered.name == "CCCC"

    discovered = collection.discover(
        ["AAAA"] + (["CCCC", "DDDD"] * multiple_scale), "CCCC"
    )
    assert isinstance(discovered, Subrecord)
    assert discovered.name == "CCCC"

    with pytest.raises(exceptions.UnexpectedSubrecord):
        collection.discover(["AAAA"], "DDDD")


def test_discover_nested_none():
    definition = (
        "TEST",
        [("AAAA", Struct()), ("BBBB", [("CCCC", Struct()), ("DDDD", Struct())])],
    )
    collection = SubrecordCollection.from_definition(*definition)

    with pytest.raises(exceptions.UnexpectedSubrecord):
        collection.discover(["AAAA", "CCCC", "DDDD"], "AAAA")

    with pytest.raises(exceptions.UnexpectedSubrecord):
        collection.discover(["AAAA", "CCCC", "DDDD"], "CCCC")

    with pytest.raises(exceptions.UnexpectedSubrecord):
        collection.discover(["AAAA", "CCCC", "DDDD"], "DDDD")
