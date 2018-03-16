# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

# flake8: noqa F405

import os
from typing import (List,)

from construct import *

from ._common import (BasePlugin,)


FNV_ServiceFlags = FlagsEnum(
    Int32ul,
    weapons=0x00000001,
    armor=0x00000002,
    alcohol=0x00000004,
    books=0x00000008,
    food=0x00000010,
    chems=0x00000020,
    stimpacks=0x00000040,
    lights=0x00000080,
    _unknown_0=0x00000100,
    _unknown_1=0x00000200,
    miscellaneous=0x00000400,
    _unknown_2=0x00000800,
    _unknown_3=0x00001000,
    potions=0x00002000,
    training=0x00004000,
    _unknown=0x00008000,
    recharge=0x00010000,
    repair=0x00020000,
)


FNV_ImpactMaterialEnum = Enum(
    Int32ul,
    stone=0,
    dirt=1,
    grass=2,
    glass=3,
    metal=4,
    wood=5,
    organic=6,
    cloth=7,
    water=8,
    hollow_metal=9,
    organic_bug=10,
    organic_glow=11
)


FNV_SkillEnum = Enum(
    Int8sl,
    none=-1,
    barter=0,
    big_guns=1,
    energy_weapons=2,
    explosives=3,
    lockpick=4,
    medicine=5,
    melee_weapons=6,
    repair=7,
    science=8,
    guns=9,
    sneak=10,
    speech=11,
    survival=12,
    unarmed=13
)


FNV_AttackAnimationsEnum = Enum(
    Int16ul,
    attack_left=26,
    attack_left_up=27,
    attack_left_down=28,
    attack_left_is=29,
    attack_left_is_up=30,
    attack_left_is_down=31,
    attack_right=32,
    attack_right_up=33,
    attack_right_down=34,
    attack_right_is=35,
    attack_right_is_up=36,
    attack_right_is_down=37,
    attack_3=38,
    attack_3_up=39,
    attack_3_down=40,
    attack_3_is=41,
    attack_3_is_up=42,
    attack_3_is_down=43,
    attack_4=44,
    attack_4_up=45,
    attack_4_down=46,
    attack_4_is=47,
    attack_4_is_up=48,
    attack_4_is_down=49,
    attack_5=50,
    attack_5_up=51,
    attack_5_down=52,
    attack_5_is=53,
    attack_5_is_up=54,
    attack_5_is_down=55,
    attack_6=56,
    attack_6_up=57,
    attack_6_down=58,
    attack_6_is=59,
    attack_6_is_up=60,
    attack_6_is_down=61,
    attack_7=62,
    attack_7_up=63,
    attack_7_down=64,
    attack_7_is=65,
    attack_7_is_up=66,
    attack_7_is_down=67,
    attack_8=68,
    attack_8_up=69,
    attack_8_down=70,
    attack_8_is=71,
    attack_8_is_up=72,
    attack_8_is_down=73,
    attack_loop=74,
    attack_loop_up=75,
    attack_loop_down=76,
    attack_loop_is=77,
    attack_loop_is_up=78,
    attack_loop_is_down=79,
    attack_spin=80,
    attack_spin_up=81,
    attack_spin_down=82,
    attack_spin_is=83,
    attack_spin_is_up=84,
    attack_spin_is_down=85,
    attack_spin_2=86,
    attack_spin_2_up=87,
    attack_spin_2_down=88,
    attack_spin_2_is=89,
    attack_spin_2_is_up=90,
    attack_spin_2_is_down=91,
    attack_power=92,
    attack_forward_power=93,
    attack_back_power=94,
    attack_left_power=95,
    attack_right_power=96,
    place_mine=97,
    place_mine_up=98,
    place_mine_down=99,
    place_mine_is=100,
    place_mine_is_up=101,
    place_mine_is_down=102,
    place_mine_2=103,
    place_mine_2_up=104,
    place_mine_2_down=105,
    place_mine_2_is=106,
    place_mine_2_is_up=107,
    place_mine_2_is_down=108,
    attack_throw=109,
    attack_throw_up=110,
    attack_throw_down=111,
    attack_throw_is=112,
    attack_throw_is_up=113,
    attack_throw_is_down=114,
    attack_throw_2=115,
    attack_throw_2_up=116,
    attack_throw_2_down=117,
    attack_throw_2_is=118,
    attack_throw_2_is_up=119,
    attack_throw_2_is_down=120,
    attack_throw_3=121,
    attack_throw_3_up=122,
    attack_throw_3_down=123,
    attack_throw_3_is=124,
    attack_throw_3_is_up=125,
    attack_throw_3_is_down=126,
    attack_throw_4=127,
    attack_throw_4_up=128,
    attack_throw_4_down=129,
    attack_throw_4_is=130,
    attack_throw_4_is_up=131,
    attack_throw_4_is_down=132,
    attack_throw_5=133,
    attack_throw_5_up=134,
    attack_throw_5_down=135,
    attack_throw_5_is=136,
    attack_throw_5_is_up=137,
    attack_throw_5_is_down=138,
    pipboy=167,
    pipboy_child=178,
    any=255
)


FNV_RGBAStruct = Struct(
    "red" / Int8ul,
    "green" / Int8ul,
    "blue" / Int8ul,
    "alpha" / Int8ul,
)


FNV_OBNDStruct = Struct(
    "X1" / Int16sl,
    "Y1" / Int16sl,
    "Z1" / Int16sl,
    "X2" / Int16sl,
    "Y2" / Int16sl,
    "Z2" / Int16sl,
)


FNV_AIDTStruct = Struct(
    "aggression" / Enum(
        Int8ul,
        unaggressive=0,
        aggressive=1,
        very_aggressive=2,
        frenzied=3
    ),
    "confidence" / Enum(
        Int8ul,
        cowardly=0,
        cautious=1,
        average=2,
        brave=3,
        foolhardy=4
    ),
    "energy_level" / Int8ul,
    "responsibility" / Int8ul,
    "mood" / Enum(
        Int8ul,
        neutral=0,
        afraid=1,
        annoyed=2,
        cocky=3,
        drugged=4,
        pleasant=5,
        angry=6,
        sad=7
    ),
    "services" / FNV_ServiceFlags,
    "teaches" / FNV_SkillEnum,
    "maximum_training_level" / Int8ul,
    "assistance" / Enum(
        Int8sl,
        helps_nobody=0,
        helps_allies=1,
        helps_friends_and_allies=2
    ),
    "aggro_radius_behavior" / FlagsEnum(
        Int8ul,
        aggro_radius_behavior=0x01
    ),
    "aggro_radius" / Int32sl,
)


FNV_MAP = {
    'ACHR': {},
    'ACRE': {},
    'ACTI': {},
    'ADDN': {},
    'ALCH': {},
    'ALOC': {},
    'AMEF': {},
    'AMMO': {},
    'ANIO': {},
    'ARMO': {},
    'ARMA': {},
    'ASPC': {},
    'AVIF': {},
    'BOOK': {},
    'BPTD': {},
    'CAMS': {},
    'CCRD': {},
    'CDCK': {},
    'CELL': {},
    'CHAL': {},
    'CHIP': {},
    'CLAS': {},
    'CLMT': {},
    'CMNY': {},
    'COBJ': {},
    'CONT': {},
    'CPTH': {},
    'CREA': {},
    'CSNO': {},
    'CSTY': {},
    'DEBR': {},
    'DEHY': {},
    'DIAL': {},
    'DOBJ': {},
    'DOOR': {},
    'ECZN': {},
    'EFSH': {},
    'ENCH': {},
    'EXPL': {},
    'EYES': {},
    'FACT': {},
    'FLST': {},
    'FURN': {},
    'GLOB': {},
    'GMST': {},
    'GRAS': {},
    'HAIR': {},
    'HDPT': {},
    'HUNG': {},
    'IDLE': {},
    'IDLM': {},
    'IMGS': {},
    'IMAD': {},
    'IMOD': {},
    'INFO': {},
    'INGR': {},
    'IPCT': {},
    'IPDS': {},
    'KEYM': {},
    'LAND': {},
    'LGMT': {},
    'LIGH': {},
    'LSCR': {},
    'LSCT': {},
    'LTEX': {},
    'LVLC': {},
    'LVLI': {},
    'LVLN': {},
    'MESG': {},
    'MGEF': {},
    'MICN': {},
    'MISC': {},
    'MSET': {},
    'MSTT': {},
    'MUSC': {},
    'NAVI': {},
    'NAVM': {},
    'NOTE': {},
    'NPC_': { # TODO: Model Data, Destruction Data, Item collections...
        'EDID': {'description': 'Editor ID', 'structure': CString('utf8')},
        'OBND': {'description': 'Object Bounds', 'structure': FNV_OBNDStruct},
        'FULL': {'description': 'NPC Name', 'structure': CString('utf8')},
        'ACBS': {
            'description': 'NPC Configuration',
            'structure': Struct(
                "flags" / FlagsEnum(
                    Int32ul,
                    biped=0x00000001,
                    essential=0x00000002,
                    is_chargen_face_preset=0x00000004,
                    respawn=0x00000008,
                    auto_calc_stats=0x00000010,
                    _unknown_0=0x00000020,
                    _unknown_1=0x00000040,
                    level_mult=0x00000080,
                    use_template=0x00000100,
                    low_level_processing=0x00000200,
                    _unknown_2=0x00000400,
                    no_blood_spray=0x00000800,
                    no_blood_decal=0x00001000,
                    _unknown_3=0x00002000,
                    _unknown_4=0x00004000,
                    _unknown_5=0x00008000,
                    _unknown_6=0x00010000,
                    _unknown_7=0x00020000,
                    _unknown_8=0x00040000,
                    _unknown_9=0x00080000,
                    no_vats_melee=0x00100000,
                    _unknown_10=0x00200000,
                    can_be_all_races=0x00400000,
                    auto_calc_services=0x00800000,
                    _unknown_11=0x01000000,
                    _unknown_12=0x02000000,
                    no_knockdowns=0x03000000,
                    not_pushable=0x08000000,
                    _unknown_13=0x10000000,
                    _unknown_14=0x20000000,
                    not_rotating_to_headtrack=0x40000000,
                    _unknown_15=0x80000000
                ),
                "fatigue" / Int16ul,
                "barter_gold" / Int16ul,
                "level" / Int16sl,
                "calc_min" / Int16ul,
                "calc_max" / Int16ul,
                "speed_multiplier" / Int16ul,
                "karma" / Float32l,
                "disposition_base" / Int16sl,
                "template_flags" / FlagsEnum(
                    Int16ul,
                    use_traits=0x0001,
                    use_stats=0x0002,
                    use_factions=0x0004,
                    use_actor_effect_list=0x0008,
                    use_ai_data=0x0010,
                    use_ai_packages=0x0020,
                    use_model=0x0040,
                    use_base_data=0x0080,
                    use_inventory=0x0100,
                    use_script=0x0200,
                ),
            )
        },
        'INAM': {'description': 'Death Item', 'structure': Int32ul},
        'VTCK': {'description': 'NPC Voice', 'structure': Int32ul},
        'TPLT': {'description': 'NPC Template', 'structure': Int32ul},
        'RNAM': {'description': 'NPC Race', 'structure': Int32ul},
        'EITM': {'description': 'Unarmed Attack Effect', 'structure': Int32ul},
        'EAMT': {
            'description': 'Unarmed Attack Animation',
            'structure': FNV_AttackAnimationsEnum
        },
        'SCRI': {'description': 'NPC Script', 'structure': Int32ul},
        'AIDT': {'description': 'NPC AI Data', 'structure': FNV_AIDTStruct},
        'PKID': {'description': 'NPC Package', 'structure': Int32ul},
        'CNAM': {'description': 'NPC Class', 'structure': Int32ul},
        'DATA': {
            'description': 'NPC Data',
            'structure': Struct(
                "base_health" / Int32sl,
                "strength" / Int8ul,
                "perception"  / Int8ul,
                "endurance" / Int8ul,
                "charisma" / Int8ul,
                "intelligence" / Int8ul,
                "agility" / Int8ul,
                "luck" / Int8ul,
                "unused" / Optional(Int8ul[:])
            )
        },
        'DNAM': {
            'description': 'NPC Skills',
            'structure': Struct(
                "barter_value" / Int8ul,
                "big_guns_value" / Int8ul,
                "energy_weapons_value" / Int8ul,
                "explosives_value" / Int8ul,
                "lockpick_value" / Int8ul,
                "medicine_value" / Int8ul,
                "melee_weapons_value" / Int8ul,
                "repair_value" / Int8ul,
                "science_value" / Int8ul,
                "guns_value" / Int8ul,
                "sneak_value" / Int8ul,
                "speech_value" / Int8ul,
                "survival_value" / Int8ul,
                "unarmed_value" / Int8ul,
                "barter_offset" / Int8ul,
                "big_guns_offset" / Int8ul,
                "energy_weapons_offset" / Int8ul,
                "explosives_offset" / Int8ul,
                "lockpick_offset" / Int8ul,
                "medicine_offset" / Int8ul,
                "melee_weapons_offset" / Int8ul,
                "repair_offset" / Int8ul,
                "science_offset" / Int8ul,
                "guns_offset" / Int8ul,
                "sneak_offset" / Int8ul,
                "speech_offset" / Int8ul,
                "survival_offset" / Int8ul,
                "unarmed_offset" / Int8ul,
            )
        },
        'PNAM': {'description': 'NPC Head Part', 'structure': Int32ul},
        'HNAM': {'description': 'NPC Hair', 'structure': Int32ul},
        'LNAM': {'description': 'NPC Hair Length', 'structure': Int32ul},
        'ENAM': {'description': 'NPC Eyes', 'structure': Int32ul},
        'HCLR': {'description': 'NPC Hair Color', 'structure': FNV_RGBAStruct},
        'ZNAM': {'description': 'NPC Combat Style', 'structure': Int32ul},
        'NAM4': {
            'description': 'Impact Material Type',
            'structure': FNV_ImpactMaterialEnum
        },
        'FGGS': {
            'description': 'NPC Facegen Geometry - Symmetric',
            'structure': Int8ul[:]
        },
        'FGGA': {
            'description': 'NPC Facegen Geometry - Asymmetric',
            'structure': Int8ul[:]
        },
        'FGTS': {
            'description': 'NPC Facegen Texture - Symmetric',
            'structure': Int8ul[:]
        },
        'NAM5': {
            'description': 'Unknown',
            'structure': Int16ul
        },
        'NAM6': {
            'description': 'NPC Height',
            'structure': Float32l
        },
        'NAM7': {
            'description': 'NPC Weight',
            'structure': Float32l
        },
    },
    'PACK': {},
    'PERK': {},
    'PGRE': {},
    'PMIS': {},
    'PROJ': {},
    'PWAT': {},
    'QUST': {},
    'RACE': {},
    'RADS': {},
    'RCCT': {},
    'RCPE': {},
    'REFR': {},
    'REGN': {},
    'REPU': {},
    'RGDL': {},
    'SCOL': {},
    'SCPT': {},
    'SLPD': {},
    'SOUN': {},
    'SPEL': {},
    'STAT': {},
    'TACT': {},
    'TERM': {},
    'TES4': {},
    'TREE': {},
    'TXST': {},
    'VTYP': {},
    'WATR': {},
    'WEAP': {},
    'WRLD': {},
    'WTHR': {},
}


FNV_Subrecord = Struct(
    "type" / String(4, 'utf8'),
    "data_size" / Int16ul,
    "data" / Bytes(lambda this: this.data_size),
)


def _parse_subrecords(record_data: bytes, record_type: str) -> List[Container]:
    while record_data and len(record_data) > 0:
        subrecord = FNV_Subrecord.parse(record_data)
        record_data = record_data[(subrecord.data_size + 6):]
        if record_type in FNV_MAP:
            if subrecord.type in FNV_MAP[record_type]:
                subrecord.description = (
                    FNV_MAP[record_type][subrecord.type]
                    .get('description', None)
                )
                subrecord.parsed = \
                    FNV_MAP[record_type][subrecord.type]['structure'].parse(
                        subrecord.data
                    )
        yield subrecord


FNV_Record = Struct(
    "type" / String(4, 'utf8'),
    "data_size" / Int32ul,
    "flags" / FlagsEnum(  # FIXME: find better names for these flags
        Int32ul,
        master=0x00000001,
        _unknown_0=0x00000002,  # NOTE: unknown flag
        _unknown_1=0x00000004,  # NOTE: unknown flag
        _unknown_2=0x00000008,  # NOTE: unknown flag
        form_initialized=0x00000010,
        deleted=0x00000020,
        constant=0x00000040,
        fire_disabled=0x00000080,
        inaccessible=0x00000100,
        casts_shadows=0x00000200,
        persistent=0x00000400,
        initially_disabled=0x00000800,
        ignored=0x00001000,
        no_voice_filter=0x00002000,
        cannot_save=0x00004000,
        visible_when_distant=0x00008000,
        random_anim_start=0x00010000,
        dangerous=0x00020000,
        compressed=0x00040000,
        cant_wait=0x00080000,
        _unknown_3=0x00100000,  # NOTE: unknown flag
        _unknown_4=0x00200000,  # NOTE: unknown flag
        _unknown_5=0x00400000,  # NOTE: unknown flag
        _unknown_6=0x00800000,  # NOTE: unknown flag
        destructible=0x01000000,
        obstacle=0x02000000,
        navmesh_filter=0x04000000,
        navmesh_box=0x08000000,
        non_pipboy=0x10000000,
        child_can_use=0x20000000,
        navmesh_ground=0x40000000,
        _unknown_7=0x80000000,  # NOTE: unknown flag
    ),
    "id" / Bytes(4),
    "revision" / Int32ul,
    "version" / Int16ul,
    "unknown" / Int16ul,
    If(lambda this: this.flags.compressed, Padding(Int32ul.sizeof())),
    "data" / IfThenElse(
        lambda this: this.flags.compressed,
        Compressed(GreedyBytes, 'zlib'),
        Bytes(lambda this: this.data_size)
    ),
    "subrecords" / Computed(
        lambda this: list(_parse_subrecords(this.data, this.type))
    ),
)


def _parse_records(group_data: bytes) -> List[Container]:
    while group_data and len(group_data) > 0:
        record = FNV_Record.parse(group_data)
        group_data = group_data[(record.data_size + 24):]
        yield record


FNV_Group = Struct(
    "type" / Const(b'GRUP'),
    "group_size" / Int32ul,
    "label" / Bytes(4),
    "group_type" / Int32sl,
    "stamp" / Int16ul,
    "unknown" / Bytes(6),
    "data" / Bytes(lambda this: this.group_size - 24),
    "records" / Computed(lambda this: list(_parse_records(this.data)))
)


class FNV_Plugin(BasePlugin):

    @property
    def plugin_structure(self) -> Struct:
        if not hasattr(self, '_plugin_structure'):
            self._plugin_structure = Struct(
                "header" / FNV_Record,
                "groups" / FNV_Group[:],
            )
        return self._plugin_structure

    @classmethod
    def can_handle(cls, filepath: str) -> bool:
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"no such file {filepath!r} exists")
        with open(filepath, 'rb') as stream:
            header = FNV_Record.parse_stream(stream)
            return header.type == 'TES4' and header.version == 15
