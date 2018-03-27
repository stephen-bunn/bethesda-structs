# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

# flake8: noqa F405

from typing import List

from construct import *
from multidict import CIMultiDict

from .._common import FormID


class FNV_FormID(Adapter):
    """ A Form ID for Fallout: New Vegas.
    """

    def __init__(self, forms: List[str], *args: list, **kwargs: dict):
        super().__init__(Int32ul, *args, **kwargs)
        self.forms = forms

    def _decode(self, obj, context, path):
        return FormID(obj, self.forms)

    def _encode(self, obj, context, path):
        return Int32ul.build(obj.form_id)


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
    _unknown_4=0x00008000,
    recharge=0x00010000,
    repair=0x00020000,
)


FNV_EquipmentTypeEnum = Enum(
    Int32sl,
    none=-1,
    big_guns=0,
    energy_weapons=1,
    small_guns=2,
    melee_weapons=3,
    unarmed_weapons=4,
    thrown_weapons=5,
    mine=6,
    body_wear=7,
    head_wear=8,
    hand_wear=9,
    chems=10,
    stimpack=11,
    food=12,
    alcohol=13
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


FNV_ObjectBoundsStruct = Struct(
    "X1" / Int16sl,
    "Y1" / Int16sl,
    "Z1" / Int16sl,
    "X2" / Int16sl,
    "Y2" / Int16sl,
    "Z2" / Int16sl,
)


FNV_DestructionCollection = CIMultiDict({
    'DEST': Struct(
        "health" / Int32sl,
        "count" / Int8ul,
        "flags" / FlagsEnum(
            Int8ul,
            vats_targetable=0x01
        ),
        "_unknown_0" / Bytes(2)
    ) * 'Header',
    'DSTD': Struct(
        "health_percentage" / Int8ul,
        "index" / Int8ul,
        "damage_stage" / Int8ul,
        "flags" / FlagsEnum(
            Int8ul,
            cap_damage=0x01,
            disable=0x02,
            destroy=0x04
        ),
        "self_damage_per_second" / Int32sl,
        "explosion" / FNV_FormID(['EXPL']),
        "debris" / FNV_FormID(['DEBR']),
        "debris_count" / Int32sl
    ) * 'Stage Data',
    'DMDT': GreedyBytes * 'Stage Model Texture File Hashes',
    'DSTF': Bytes(0) * 'Stage End Marker'
})


FNV_ModelCollection = CIMultiDict({
    'MODL': CString('utf8') * 'Model Filename',
    'MODB': Bytes(4) * 'Unknown',
    'MODT': GreedyBytes * 'Texture File Hashes',
    'MODS': Struct(
        "count" / Int32ul,
        "alternate_texture" / Struct(
            "name_length" / Int32ul,
            "3d_name" / PaddedString(
                lambda this: this.name_length,
                'utf8'
            ),
            "new_texture" / FNV_FormID(['TXST']),
            "3d_index" / Int32sl
        )
    ) * 'Alternate Textures',
    'MODD': FlagsEnum(
        Int8ul,
        head=0x01,
        torso=0x02,
        right_hand=0x04,
        left_hand=0x08
    ) * 'Facegen Model Flags'
})


FNV_Model2Collection = CIMultiDict({
    'MOD2': CString('utf8') * 'Model Filename',
    'MO2T': GreedyBytes * 'Texture File Hashes',
    'MO2S': Struct(
        "count" / Int32ul,
        "alternate_texture" / Struct(
            "name_length" / Int32ul,
            "3d_name" / PaddedString(
                lambda this: this.name_length,
                'utf8'
            ),
            "new_texture" / FNV_FormID(['TXST']),
            "3d_index" / Int32sl
        )
    ) * 'Alternate Textures'
})


FNV_Model3Collection = CIMultiDict({
    'MOD3': CString('utf8') * 'Model Filename',
    'MO3T': GreedyBytes * 'Texture File Hashes',
    'MO3S': Struct(
        "count" / Int32ul,
        "alternate_texture" / Struct(
            "name_length" / Int32ul,
            "3d_name" / PaddedString(
                lambda this: this.name_length,
                'utf8'
            ),
            "new_texture" / FNV_FormID(['TXST']),
            "3d_index" / Int32sl
        )
    ) * 'Alternate Textures',
    'MOSD': FlagsEnum(
        Int8ul,
        head=0x01,
        torso=0x02,
        right_hand=0x04,
        left_hand=0x08
    ) * 'Facegen Model Flags'
})


FNV_Model4Collection = CIMultiDict({
    'MOD4': CString('utf8') * 'Model Filename',
    'MO4T': GreedyBytes * 'Texture File Hashes',
    'MO4S': Struct(
        "count" / Int32ul,
        "alternate_texture" / Struct(
            "name_length" / Int32ul,
            "3d_name" / PaddedString(
                lambda this: this.name_length,
                'utf8'
            ),
            "new_texture" / FNV_FormID(['TXST']),
            "3d_index" / Int32sl
        )
    ) * 'Alternate Textures'
})


FNV_ItemCollection = CIMultiDict({
    'CNTO': Struct(
        "item" / FNV_FormID([
            'AMRO', 'AMMO', 'MISC', 'WEAP', 'BOOK', 'LVLI', 'KEYM', 'ALCH',
            'NOTE', 'IMOD', 'CMNY', 'CCRD', 'LIGH', 'CHIP', 'MSTT', 'STAT'
        ]),
        "count" / Int32sl
    ) * 'Item',
    'COED': Struct(
        "owner" / FNV_FormID(['NPC_', 'FACT']),
        "global_variable" / FNV_FormID(['GLOB']), # FIXME: various types,
        "item_condition" / Float32l
    ) * 'Extra Data'
})


FNV_ScriptCollection = CIMultiDict({
    'SCHR': Struct(
        "unused" / Byte[4],
        "ref_count" / Int32ul,
        "compiled_size" / Int32ul,
        "variable_count" / Int32ul,
        "type" / FlagsEnum(
            Int16ul,
            object=0x000,
            quest=0x001,
            effect=0x100
        ),
        "flags" / FlagsEnum(
            Int16ul,
            enabled=0x0001
        )
    ) * 'Basic Script Data',
    'SCDA': GreedyBytes * 'Commpiled Script Source',
    'SCTX': GreedyString('utf8') * 'Script Source',
    'SLSD': Struct(
        "index" / Int32ul,
        "_unknown_0" / Bytes(12),
        "flags" / FlagsEnum(
            Int8ul,
            is_long_or_short=0x01
        ),
        "_unknown_1" / Bytes(7)
    ) * 'Local Variable Data',
    'SCVR': CString('utf8') * 'Local Variable Name',
    'SCRO': FNV_FormID([
        'ACTI', 'DOOR', 'STAT', 'FURN', 'CREA', 'SPEL', 'NPC_', 'CONT', 'ARMO',
        'AMMO', 'MISC', 'WEAP', 'IMAD', 'BOOK', 'KEYM', 'ALCH', 'LIGH', 'QUST',
        'PLYR', 'PACK', 'LVLI', 'ECZN', 'EXPL', 'FLST', 'IDLM', 'PMIS', 'FACT',
        'ACHR', 'REFR', 'ACRE', 'GLOB', 'DIAL', 'CELL', 'SOUN', 'MGEF', 'WTHR',
        'CLAS', 'EFSH', 'RACE', 'LVLC', 'CSTY', 'WRLD', 'SCPT', 'IMGS', 'MESG',
        'MSTT', 'MUSC', 'NOTE', 'PERK', 'PGRE', 'PROJ', 'LVLN', 'WATR', 'ENCH',
        'TREE', 'REPU', 'REGN', 'CSNO', 'CHAL', 'IMOD', 'RCCT', 'CMNY', 'CDCK',
        'CHIP', 'CCRD', 'TERM', 'HAIR', 'EYES', 'ADDN', 'NULL'
    ]) * 'Reference'
})
