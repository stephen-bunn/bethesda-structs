# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://opensource.org/licenses/MIT>

import pytest
from construct import Struct
from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import none, text, one_of, booleans, from_type, sampled_from

from . import subrecord, subrecord_dict, random_base_type, subrecord_definition
from bethesda_structs.plugin._common import Subrecord


@given(text(min_size=4, max_size=4), from_type(Struct), booleans(), booleans())
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_init(name, struct, optional, multiple):
    subr = Subrecord(name, struct, optional=optional, multiple=multiple)
    assert isinstance(subr, Subrecord)
    assert subr.name == name
    assert subr.struct == struct
    assert subr.optional == optional
    assert subr.multiple == multiple


@given(
    one_of(text().filter(lambda text: len(text) != 4), random_base_type(ignore=[str])),
    from_type(Struct),
    booleans(),
    booleans(),
)
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_invalid_name(name, struct, optional, multiple):
    if isinstance(name, str):
        with pytest.raises(ValueError):
            Subrecord(name, struct, optional, multiple)
    else:
        with pytest.raises(TypeError):
            Subrecord(name, struct, optional, multiple)


@given(text(min_size=4, max_size=4), random_base_type(), booleans(), booleans())
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_invalid_struct(name, struct, optional, multiple):
    with pytest.raises(TypeError):
        Subrecord(name, struct, optional, multiple)


@given(
    text(min_size=4, max_size=4),
    from_type(Struct),
    random_base_type([bool]),
    booleans(),
)
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_invalid_optional(name, struct, optional, multiple):
    with pytest.raises(TypeError):
        Subrecord(name, struct, optional, multiple)


@given(
    text(min_size=4, max_size=4),
    from_type(Struct),
    booleans(),
    random_base_type([bool]),
)
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_invalid_multiple(name, struct, optional, multiple):
    with pytest.raises(TypeError):
        Subrecord(name, struct, optional, multiple)


@given(subrecord_definition())
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_from_definition(definition):
    subr = Subrecord.from_definition(*definition)
    assert isinstance(subr, Subrecord)
    assert subr.name == definition[0][:4]
    assert subr.struct == definition[-1]
    if definition[0][-1] in ("*", "+", "?"):
        (optional, multiple) = Subrecord.parse_flag(definition[0][-1])
        assert subr.optional == optional
        assert subr.multiple == multiple
    else:
        assert not subr.optional
        assert not subr.multiple


@given(subrecord_dict())
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_from_dict(dictionary):
    subr = Subrecord.from_dict(dictionary)
    assert isinstance(subr, Subrecord)
    assert subr.name == dictionary["name"]
    assert subr.struct == dictionary["struct"]
    assert subr.optional == dictionary["optional"]
    assert subr.multiple == dictionary["multiple"]


@given(subrecord_definition())
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_to_definition(definition):
    subr = Subrecord.from_definition(*definition)
    assert isinstance(subr, Subrecord)
    assert subr.to_definition() == definition


@given(subrecord_dict())
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_to_dict(dictionary):
    subr = Subrecord.from_dict(dictionary)
    assert isinstance(subr, Subrecord)
    assert subr.to_dict() == dictionary


@given(subrecord())
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_build_flag(subr):
    flag = subr._build_flag()
    assert flag in ("+", "?", "*", "")
    if subr.multiple:
        if subr.optional:
            assert flag == "*"
        else:
            assert flag == "+"
    else:
        if subr.optional:
            assert flag == "?"
        else:
            assert flag == ""


@given(subrecord(), sampled_from(["+", "?", "*", ""]))
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_be(subrecord_, flag):
    (optional, multiple) = Subrecord.parse_flag(flag)
    subr = subrecord_.be(flag)
    assert isinstance(subr, Subrecord)
    assert subr.name == subrecord_.name
    assert subr.struct == subrecord_.struct
    assert subr.optional == optional
    assert subr.multiple == multiple
