# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://opensource.org/licenses/MIT>

from construct import Struct
from hypothesis.strategies import (
    none,
    sets,
    text,
    dates,
    lists,
    times,
    uuids,
    binary,
    builds,
    floats,
    one_of,
    tuples,
    nothing,
    booleans,
    decimals,
    integers,
    composite,
    datetimes,
    fractions,
    from_type,
    iterables,
    characters,
    from_regex,
    frozensets,
    timedeltas,
    complex_numbers,
)

from bethesda_structs.plugin._common import Subrecord, SubrecordCollection

COLLECTION_MIN_COUNT = 1
COLLECTION_MAX_COUNT = 5
COLLECTION_LEVEL_LIMIT = 3


@composite
def random_base_type(draw, ignore: list = []):
    ignore = tuple(ignore)
    return draw(
        one_of(
            none(),
            builds(set),
            text(),
            dates(),
            builds(list),
            times(),
            uuids(),
            binary(),
            floats(),
            tuples(),
            booleans(),
            decimals(),
            integers(),
            datetimes(),
            fractions(),
            iterables(nothing()),
            characters(),
            builds(frozenset),
            timedeltas(),
            complex_numbers(),
        ).filter(lambda x: not isinstance(x, ignore))
    )


@composite
def subrecord_dict(draw):
    return dict(
        name=draw(text(min_size=4, max_size=4)),
        struct=draw(from_type(Struct)),
        optional=draw(booleans()),
        multiple=draw(booleans()),
    )


@composite
def subrecord_collection_dict(
    draw,
    min_count: int = COLLECTION_MIN_COUNT,
    max_count: int = COLLECTION_MAX_COUNT,
    level_limit: int = COLLECTION_LEVEL_LIMIT,
    current_level: int = 0,
):
    if current_level <= level_limit:
        return dict(
            name=draw(text(min_size=4, max_size=4)),
            items=[
                draw(
                    one_of(
                        subrecord_dict(),
                        subrecord_collection_dict(
                            min_count=min_count,
                            max_count=max_count,
                            level_limit=level_limit,
                            current_level=(current_level + 1),
                        ).filter(lambda x: isinstance(x, dict)),
                    )
                )
                for _ in range(draw(integers(min_value=min_count, max_value=max_count)))
            ],
            optional=draw(booleans()),
            multiple=draw(booleans()),
        )


@composite
def subrecord_definition(draw):
    return (draw(from_regex(Subrecord._definition_regex)), draw(from_type(Struct)))


@composite
def subrecord_collection_definition(
    draw,
    min_count: int = COLLECTION_MIN_COUNT,
    max_count: int = COLLECTION_MAX_COUNT,
    level_limit: int = COLLECTION_LEVEL_LIMIT,
    current_level: int = 0,
):
    if current_level <= level_limit:
        return (
            draw(from_regex(SubrecordCollection._definition_regex)),
            [
                draw(
                    one_of(
                        subrecord_definition(),
                        subrecord_collection_definition(
                            min_count=min_count,
                            max_count=max_count,
                            level_limit=level_limit,
                            current_level=(current_level + 1),
                        ).filter(lambda x: isinstance(x, tuple)),
                    )
                )
                for _ in range(draw(integers(min_value=min_count, max_value=max_count)))
            ],
        )


@composite
def subrecord(draw):
    return Subrecord.from_definition(*draw(subrecord_definition()))


@composite
def subrecord_collection(
    draw,
    min_count: int = COLLECTION_MIN_COUNT,
    max_count: int = COLLECTION_MAX_COUNT,
    level_limit: int = COLLECTION_LEVEL_LIMIT,
):
    return SubrecordCollection.from_definition(
        *draw(
            subrecord_collection_definition(
                min_count=min_count, max_count=max_count, level_limit=level_limit
            )
        )
    )


@composite
def subrecord_collection_items(
    draw,
    min_count: int = COLLECTION_MIN_COUNT,
    max_count: int = COLLECTION_MAX_COUNT,
    level_limit: int = COLLECTION_LEVEL_LIMIT,
):
    return [
        draw(
            one_of(
                subrecord(),
                subrecord_collection(
                    min_count=min_count, max_count=max_count, level_limit=level_limit
                ),
            )
        )
        for _ in range(draw(integers(min_value=min_count, max_value=max_count)))
    ]
