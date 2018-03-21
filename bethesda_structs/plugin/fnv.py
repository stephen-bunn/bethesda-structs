# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

# flake8: noqa F405

import os
from typing import (List,)

from construct import *

from ._common import (BasePlugin,)


class FNV_FormID(Adapter):

    def __init__(self, backrefs, *args, **kwargs):
        super().__init__(Int32ul, *args, **kwargs)
        self.backrefs = backrefs

    def _decode(self, obj, context, path):
        return obj

    def _encode(self, obj, context, path):
        return obj


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


FNV_DestructionCollection = {
    'DEST': Struct(
        "health" / Int32sl,
        "count" / Int8ul,
        "flags" / FlagsEnum(
            Int8ul,
            vats_targetable=0x01
        ),
        "unknown_0" / Bytes(2)
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
    'DMDT': Byte[:] * 'Stage Model Texture File Hashes',
    'DSTF': Bytes(0) * 'Stage End Marker'
}

FNV_ScriptCollection = {
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
    'SCDA': Int8ul[:] * 'Commpiled Script Source',
    'SCTX': GreedyString('utf8') * 'Script Source',
    'SLSD': Struct(
        "index" / Int32ul,
        "unknown_0" / Bytes(12),
        "flags" / FlagsEnum(
            Int8ul,
            is_long_or_short=0x01
        ),
        "unknown_1" / Bytes(7)
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
}

FNV_ModelCollection = {
    'MODL': CString('utf8') * 'Model Filename',
    'MODB': Bytes(4) * 'Unknown',
    'MODT': Byte[:] * 'Texture File Hashes',
    'MODS': Struct(
        "count" / Int32ul * 'Alternate Textures Count',
        "alternate_texture" / Struct(
            "name_length" / Int32ul * 'Alternate Texture Data',
            "3d_name" / PaddedString(
                lambda this: this.name_length,
                'utf8'
            ) * 'Alternate Texture Data',
            "new_texture" / FNV_FormID(['TXST']) * 'Alternate Texture Data',
            "3d_index" / Int32sl * 'Alternate Texture Data'
        )
    ) * 'Alternate Textures',
    'MODD': FlagsEnum(
        Int8ul,
        head=0x01,
        torso=0x02,
        right_hand=0x04,
        left_hand=0x08
    ) * 'Facegen Model Flags'
}


FNV_MAP = {
    'ACHR': dict({
        'EDID': CString('utf8') * 'Editor ID',
        'NAME': FNV_FormID(['NPC_']) * 'Base',
        'XEZN': FNV_FormID(['ECZN']) * 'Encounter Zone',
        'XRGD': Byte[:] * 'Ragdoll Data',
        'XRGB': Byte[:] * 'Ragdol Biped Data',
        'XPRD': Float32l * 'Patrol Data',
        'XPPA': Bytes(0) * 'Patrol Script Marker',
        'INAM': FNV_FormID(['IDLE']) * 'Idle',
        'TNAM': FNV_FormID(['DIAL']) * 'Topic',
        'XLCM': Int32sl * 'Level Modifier',
        'XMRC': FNV_FormID(['REFR']) * 'Merchant Container',
        'XCNT': Int32sl * 'Count',
        'XRDS': Float32l * 'Radius',
        'XHLP': Float32l * 'Health',
        'XLKR': FNV_FormID([
            'REFR', 'ACRE', 'ACHR', 'PGRE', 'PMIS'
        ]) * 'Linked Reference',
        'XDCR': Struct(
            "reference" / FNV_FormID(['REFR']),
            "unknown" / Byte[:]
        ) * 'Decal',
        'XCLP': Struct(
            "link_start_color" / FNV_RGBAStruct,
            "link_end_color" / FNV_RGBAStruct
        ) * 'Linked Reference Color',
        'XAPD': FlagsEnum(
            Int8ul,
            parent_activate_only=0x01
        ) * 'Flags',
        'XAPR': Struct(
            "reference" / FNV_FormID(['REFR', 'ACRE', 'ACHR', 'PGRE', 'PMIS']),
            "delay" / Float32l
        ) * 'Active Parent Reference',
        'XATO': CString('utf8') * 'Activation Prompt',
        'XESP': Struct(
            "reference" / FNV_FormID([
                'PLYR', 'REFR', 'ACRE', 'ACHR', 'PGRE', 'PMIS'
            ]),
            "flags" / FlagsEnum(
                Int8ul,
                set_enable_state_to_opposite_of_parent=0x01,
                pop_in=0x02
            ),
            "unknown" / Byte[3]
        ) * 'Enable Parent',
        'XEMI': FNV_FormID(['LIGH', 'REGN']) * 'Emittance',
        'XMBR': FNV_FormID(['REFR']) * 'MultiBound Reference',
        'XIBS': Bytes(0) * 'Ignored by Sandbox',
        'XSCL': Float32l * 'Scale',
        'DATA': Struct(
            "x_position" / Float32l,
            "y_position" / Float32l,
            "z_position" / Float32l,
            "x_rotation" / Float32l,
            "y_rotation" / Float32l,
            "z_rotation" / Float32l
        ) * 'Postion / Rotation'

    }, **FNV_ScriptCollection),
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
    'FACT': {
        'EDID': CString('utf8') * 'Editor ID',
        'FULL': CString('utf8') * 'Name',
        'XNAM': Struct(
            "faction" / FNV_FormID(['FACT', 'RACE']),
            "modifier" / Int32sl,
            "group_combat_reaction" / Enum(
                Int32ul,
                neutral=0,
                enemy=1,
                ally=2,
                friend=3
            )
        ) * 'Relation',
        'DATA': Struct(
            "flags_1" / FlagsEnum(
                Int8ul,
                hidden_from_pc=0x01,
                evil=0x02,
                special_combat=0x04
            ),
            "flags_2" / FlagsEnum(
                Int8ul,
                track_crime=0x01,
                allow_sell=0x02
            ),
            "unused" / Byte[2]
        ) * 'Data',
        'CNAM': Float32l * 'Unused',
        'RNAM': Int32sl * 'Rank Number',
        'MNAM': CString('utf8') * 'Male',
        'FNAM': CString('utf8') * 'Female',
        'INAM': CString('utf8') * 'Insignia (unused)',
        'WMI1': FNV_FormID(['REPU']) * 'Reputation'
    },
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
    'KEYM': dict({
        'EDID': CString('utf8') * 'Editor ID',
        'OBND': FNV_OBNDStruct * 'Object Bounds',
        'FULL': CString('utf8') * 'Name',
        'ICON': CString('utf8') * 'Large Icon Filename',
        'MICO': CString('utf8') * 'Small Icon Filename',
        'SCRI': FNV_FormID(['SCPT']) * 'Script',
        'YNAM': FNV_FormID(['SOUN']) * 'Sound - Pick Up',
        'ZNAM': FNV_FormID(['SOUN']) * 'Sound - Drop',
        'DATA': Struct(
            "value" / Int32sl,
            "weight" / Float32l
        ),
        'RNAM': FNV_FormID(['SOUN']) * 'Sound - Random/Looping'
    }, **FNV_ModelCollection, **FNV_DestructionCollection),
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
    'NAVI': {
        'EDID': CString('utf8') * 'Editor ID',
        'NVER': Int32ul * 'Version',
        'NVMI': Struct(
            "unknown_0" / Bytes(4),
            "navigation_mesh" / FNV_FormID(['NAVM']),
            "location" / FNV_FormID(['CELL', 'WRLD']),
            "grid_x" / Int16sl,
            "grid_y" / Int16sl,
            "unknown_1" / Int8ul[:]
        ) * 'Navigation Map Info',
        'NVCI': Struct(
            "unknown_0" / FNV_FormID(['NAVM']),
            "unknown_1" / FNV_FormID(['NAVM']),
            "unknown_2" / FNV_FormID(['NAVM']),
            "door" / FNV_FormID(['REFR']),
        ) * 'Unknown'
    },
    'NAVM': {},
    'NOTE': dict({
        'EDID': CString('utf8') * 'Editor ID',
        'OBND': FNV_OBNDStruct * 'Object Bounds',
        'FULL': CString('utf8') * 'Name',
        'ICON': CString('utf8') * 'Large Icon Filename',
        'MICO': CString('utf8') * 'Small Icon Filename',
        'YNAM': FNV_FormID(['SOUN']) * 'Sound - Pick Up',
        'ZNAM': FNV_FormID(['SOUN']) * 'Sound - Drop',
        'DATA': Enum(
            Int8ul,
            sound=0,
            text=1,
            image=2,
            voice=3
        ) * 'Type',
        'XNAM': CString('utf8') * 'Texture',
        'TNAM': CString('utf8') * 'Text / Topic',
        'SNAM': FNV_FormID(['SOUN', 'NPC_', 'CREA']) * 'Sound / Actor'
    }, **FNV_ModelCollection),
    'NPC_': {
        # 'EDID': {
        #     'description': 'Editor ID',
        #     'structure': CString('utf8')
        # },
        # 'OBND': {
        #     'description': 'Object Bounds',
        #     'structure': FNV_OBNDStruct
        # },
        # 'FULL': {
        #     'description': 'NPC Name',
        #     'structure': CString('utf8')
        # },
        # 'MODL': {
        #     'description': 'Model Filename',
        #     'structure': CString('utf8')
        # },
        # 'MODB': {
        #     'description': 'Model Texture Unknown',
        #     'structure': Bytes(4)
        # },
        # 'MODT': {
        #     'description': 'Model Texture File Hashes',
        #     'structure': Byte[:]
        # },
        # 'MODS': {
        #     'description': 'Alternate Textures',
        #     'structure': Struct(
        #         "count" / Int32ul,
        #         "alternate_texture" / Struct(
        #             "name_length" / Int32ul,
        #             "3d_name" / PaddedString(
        #                 lambda this: this.name_length,
        #                 'utf8'
        #             ),
        #             "new_texture" / FNV_FormID(['TXST']),
        #             "3d_index" / Int32sl
        #         )
        #     )
        # },
        # 'MODD': {
        #     'description': 'FaceGen Model Flags',
        #     'structure': FlagsEnum(
        #         Int8ul,
        #         head=0x01,
        #         torso=0x02,
        #         right_hand=0x04,
        #         left_hand=0x08
        #     )
        # },
        # 'ACBS': {
        #     'description': 'NPC Configuration',
        #     'structure': Struct(
        #         "flags" / FlagsEnum(
        #             Int32ul,
        #             biped=0x00000001,
        #             essential=0x00000002,
        #             is_chargen_face_preset=0x00000004,
        #             respawn=0x00000008,
        #             auto_calc_stats=0x00000010,
        #             _unknown_0=0x00000020,
        #             _unknown_1=0x00000040,
        #             level_mult=0x00000080,
        #             use_template=0x00000100,
        #             low_level_processing=0x00000200,
        #             _unknown_2=0x00000400,
        #             no_blood_spray=0x00000800,
        #             no_blood_decal=0x00001000,
        #             _unknown_3=0x00002000,
        #             _unknown_4=0x00004000,
        #             _unknown_5=0x00008000,
        #             _unknown_6=0x00010000,
        #             _unknown_7=0x00020000,
        #             _unknown_8=0x00040000,
        #             _unknown_9=0x00080000,
        #             no_vats_melee=0x00100000,
        #             _unknown_10=0x00200000,
        #             can_be_all_races=0x00400000,
        #             auto_calc_services=0x00800000,
        #             _unknown_11=0x01000000,
        #             _unknown_12=0x02000000,
        #             no_knockdowns=0x03000000,
        #             not_pushable=0x08000000,
        #             _unknown_13=0x10000000,
        #             _unknown_14=0x20000000,
        #             not_rotating_to_headtrack=0x40000000,
        #             _unknown_15=0x80000000
        #         ),
        #         "fatigue" / Int16ul,
        #         "barter_gold" / Int16ul,
        #         "level" / Int16sl,
        #         "calc_min" / Int16ul,
        #         "calc_max" / Int16ul,
        #         "speed_multiplier" / Int16ul,
        #         "karma" / Float32l,
        #         "disposition_base" / Int16sl,
        #         "template_flags" / FlagsEnum(
        #             Int16ul,
        #             use_traits=0x0001,
        #             use_stats=0x0002,
        #             use_factions=0x0004,
        #             use_actor_effect_list=0x0008,
        #             use_ai_data=0x0010,
        #             use_ai_packages=0x0020,
        #             use_model=0x0040,
        #             use_base_data=0x0080,
        #             use_inventory=0x0100,
        #             use_script=0x0200,
        #         ),
        #     )
        # },
        # 'SNAM': {
        #     'description': 'NPC Faction',
        #     'structure': Struct(
        #         "faction" / FNV_FormID(['FACT']),
        #         "rank" / Int8ul,
        #         "unused" / Bytes(3)
        #     )
        # },
        # 'INAM': {
        #     'description': 'Death Item',
        #     'structure': FNV_FormID(['LVL1'])
        # },
        # 'VTCK': {
        #     'description': 'NPC Voice',
        #     'structure': FNV_FormID(['VTCP'])
        # },
        # 'TPLT': {
        #     'description': 'NPC Template',
        #     'structure': FNV_FormID(['NPC_', 'LVLN'])
        # },
        # 'RNAM': {
        #     'description': 'NPC Race',
        #     'structure': FNV_FormID(['RACE'])
        # },
        # 'SPLO': {
        #     'description': 'Actor Effect',
        #     'structure': FNV_FormID(['SPEL'])
        # },
        # 'EITM': {
        #     'description': 'Unarmed Attack Effect',
        #     'structure': FNV_FormID(['ENCH', 'SPEL'])
        # },
        # 'EAMT': {
        #     'description': 'Unarmed Attack Animation',
        #     'structure': FNV_AttackAnimationsEnum
        # },
        # 'DEST': {
        #     'description': 'Destruction Data',
        #     'structure': Struct(
        #         "health" / Int32sl,
        #         "count" / Int8ul,
        #         "flags" / FlagsEnum(
        #             Int8ul,
        #             vats_targetable=0x01
        #         ),
        #         "unknown" / Bytes(2)
        #     )
        # },
        # 'DSTD': {
        #     'description': 'Destruction Stage Data',
        #     'structure': Struct(
        #         "health_percentage" / Int8ul,
        #         "index" / Int8ul,
        #         "damage_stage" / Int8ul,
        #         "flags" / FlagsEnum(
        #             Int8ul,
        #             cap_damage=0x1,
        #             disable=0x2,
        #             destroy=0x4
        #         ),
        #         "self_damage_per_second" / Int32sl,
        #         "explosion" / FNV_FormID(['EXPL']),
        #         "debris" / FNV_FormID(['DEBR']),
        #         "debris_count" / Int32sl
        #     )
        # },
        # 'SCRI': {
        #     'description': 'NPC Script',
        #     'structure': FNV_FormID(['SCPT'])
        # },
        # 'CNTO': {
        #     'description': 'Item Data',
        #     'structure': Struct(
        #         "item" / FNV_FormID([
        #             'AMRO', 'AMMO', 'MISC', 'WEAP', 'BOOK', 'LVL1', 'KEYM',
        #             'ALCH', 'NOTE', 'IMOD', 'CMNY', 'CCRD', 'LIGH', 'CHIP',
        #             'MSTT', 'STAT'
        #         ]),
        #         "count" / Int32sl
        #     )
        # },
        # 'COED': {
        #     'description': 'Extra Item Data',
        #     'structure': Struct(
        #         "owner" / FNV_FormID(['NPC_', 'FACT']),
        #         "global_variable" / FNV_FormID(['GLOB']),
        #         "item_condition" / Float32l
        #     )
        # },
        # 'AIDT': {
        #     'description': 'NPC AI Data',
        #     'structure': FNV_AIDTStruct
        # },
        # 'PKID': {
        #     'description': 'NPC Package',
        #     'structure': FNV_FormID(['PACK'])
        # },
        # 'CNAM': {
        #     'description': 'NPC Class',
        #     'structure': FNV_FormID(['CLAS'])
        # },
        # 'DATA': {
        #     'description': 'NPC Data',
        #     'structure': Struct(
        #         "base_health" / Int32sl,
        #         "strength" / Int8ul,
        #         "perception"  / Int8ul,
        #         "endurance" / Int8ul,
        #         "charisma" / Int8ul,
        #         "intelligence" / Int8ul,
        #         "agility" / Int8ul,
        #         "luck" / Int8ul,
        #         "unused" / Optional(Int8ul[:])
        #     )
        # },
        # 'DNAM': {
        #     'description': 'NPC Skills',
        #     'structure': Struct(
        #         "barter_value" / Int8ul,
        #         "big_guns_value" / Int8ul,
        #         "energy_weapons_value" / Int8ul,
        #         "explosives_value" / Int8ul,
        #         "lockpick_value" / Int8ul,
        #         "medicine_value" / Int8ul,
        #         "melee_weapons_value" / Int8ul,
        #         "repair_value" / Int8ul,
        #         "science_value" / Int8ul,
        #         "guns_value" / Int8ul,
        #         "sneak_value" / Int8ul,
        #         "speech_value" / Int8ul,
        #         "survival_value" / Int8ul,
        #         "unarmed_value" / Int8ul,
        #         "barter_offset" / Int8ul,
        #         "big_guns_offset" / Int8ul,
        #         "energy_weapons_offset" / Int8ul,
        #         "explosives_offset" / Int8ul,
        #         "lockpick_offset" / Int8ul,
        #         "medicine_offset" / Int8ul,
        #         "melee_weapons_offset" / Int8ul,
        #         "repair_offset" / Int8ul,
        #         "science_offset" / Int8ul,
        #         "guns_offset" / Int8ul,
        #         "sneak_offset" / Int8ul,
        #         "speech_offset" / Int8ul,
        #         "survival_offset" / Int8ul,
        #         "unarmed_offset" / Int8ul,
        #     )
        # },
        # 'PNAM': {
        #     'description': 'NPC Head Part',
        #     'structure': FNV_FormID(['HDPT'])
        # },
        # 'HNAM': {
        #     'description': 'NPC Hair',
        #     'structure': FNV_FormID(['HAIR'])
        # },
        # 'LNAM': {
        #     'description': 'NPC Hair Length',
        #     'structure': Float32l
        # },
        # 'ENAM': {
        #     'description': 'NPC Eyes',
        #     'structure': FNV_FormID(['EYES'])
        # },
        # 'HCLR': {
        #     'description': 'NPC Hair Color',
        #     'structure': FNV_RGBAStruct
        # },
        # 'ZNAM': {
        #     'description': 'NPC Combat Style',
        #     'structure': FNV_FormID(['CSTY'])
        # },
        # 'NAM4': {
        #     'description': 'Impact Material Type',
        #     'structure': FNV_ImpactMaterialEnum
        # },
        # 'FGGS': {
        #     'description': 'NPC Facegen Geometry - Symmetric',
        #     'structure': Int8ul[:]
        # },
        # 'FGGA': {
        #     'description': 'NPC Facegen Geometry - Asymmetric',
        #     'structure': Int8ul[:]
        # },
        # 'FGTS': {
        #     'description': 'NPC Facegen Texture - Symmetric',
        #     'structure': Int8ul[:]
        # },
        # 'NAM5': {
        #     'description': 'Unknown',
        #     'structure': Int16ul
        # },
        # 'NAM6': {
        #     'description': 'NPC Height',
        #     'structure': Float32l
        # },
        # 'NAM7': {
        #     'description': 'NPC Weight',
        #     'structure': Float32l
        # },
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
    'SCPT': dict({
        'EDID': CString('utf8') * 'Editor ID',
    }, **FNV_ScriptCollection),
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
    "type" / PaddedString(4, 'utf8'),
    "data_size" / Int16ul,
    "data" / Bytes(lambda this: this.data_size),
)


def _parse_subrecords(record_data: bytes, record_type: str) -> List[Container]:
    while record_data and len(record_data) > 0:
        subrecord = FNV_Subrecord.parse(record_data)
        record_data = record_data[(subrecord.data_size + 6):]

        if record_type in FNV_MAP:
            if subrecord.type in FNV_MAP[record_type]:
                subrecord_struct = FNV_MAP[record_type][subrecord.type]
                (subrecord.parsed, subrecord.description,) = (
                    subrecord_struct.parse(subrecord.data),
                    getattr(subrecord_struct, 'docs', None),
                )

        yield subrecord


FNV_Record = Struct(
    "type" / PaddedString(4, 'utf8'),
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
