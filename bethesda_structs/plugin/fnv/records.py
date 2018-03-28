# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

# flake8: noqa F405

from construct import *
from multidict import CIMultiDict

from ._common import *


ACTI_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('SNAM', FNV_FormID(['SOUN']) * 'Sound - Looping'),
    ('VNAM', FNV_FormID(['SOUN']) * 'Sound - Activation'),
    ('INAM', FNV_FormID(['SOUN']) * 'Radio Template'),
    ('RNAM', FNV_FormID(['TACT']) * 'Radio Station'),
    ('WNAM', FNV_FormID(['WATR']) * 'Water Type'),
    ('XATO', CString('utf8') * 'Activation Prompt'),
],
    **ModelCollection,
    **DestructionCollection
)


AMMO_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('ICON', CString('utf8') * 'Large Icon Filename'),
    ('MICO', CString('utf8') * 'Small Icon Filename'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('YNAM', FNV_FormID(['SOUN']) * 'Sound - Pick Up'),
    ('ZNAM', FNV_FormID(['SOUN']) * 'Sound - Drop'),
    ('DATA', Struct(
        "speed" / Float32l,
        "flags" / FlagsEnum(
            Int8ul,
            ignores_normal_weapon_resistance=0x1,
            non_playable=0x2
        ),
        "unused" / Bytes(3),
        "value" / Int32sl,
        "clip_rounds" / Int8ul
    )),
    ('DAT2', Struct(
        "projectiles_per_shot" / Int32ul,
        "projectile" / FNV_FormID(['PROJ']),
        "weight" / Float32l,
        "consumed_ammo" / FNV_FormID(['AMMO', 'MISC']),
        "consumed_percentage" / Float32l
    )),
    ('ONAM', CString('utf8') * 'Short Name'),
    ('QNAM', CString('utf8') * 'Abbreviation'),
    ('RCIL', FNV_FormID(['AMEF']) * 'Ammo Effect'),
],
    **ModelCollection,
    **DestructionCollection
)


ARMO_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('EITM', FNV_FormID(['ENCH', 'SPEL']) * 'Object Effect'),
    ('BMDT', Struct(
        "biped_flags" / FlagsEnum(
            Int32ul,
            head=0x00000001,
            hair=0x00000002,
            upper_body=0x00000004,
            left_hand=0x00000008,
            right_hand=0x00000010,
            weapon=0x00000020,
            pipboy=0x00000040,
            backpack=0x00000080,
            necklace=0x00000100,
            headband=0x00000200,
            hat=0x00000400,
            eye_glasses=0x00000800,
            nose_ring=0x00001000,
            earrings=0x00002000,
            mask=0x00004000,
            choker=0x00008000,
            mouth_object=0x00010000,
            body_addon_1=0x00020000,
            body_addon_2=0x00040000,
            body_addon_3=0x00080000
        ),
        "general_flags" / FlagsEnum(
            Int8ul,
            unknown_1=0x01,
            unknown_2=0x02,
            has_backpack=0x04,
            medium=0x08,
            unknown_3=0x10,
            power_armor=0x20,
            non_playable=0x40,
            heavy=0x80
        ),
        "unused" / GreedyBytes
    ) * 'Biped Data'),
    ('ICON', CString('utf8') * 'Male Inventory Icon Filename'),
    ('MICO', CString('utf8') * 'Male Message Icon Filename'),
    ('ICO2', CString('utf8') * 'Female Inventory Icon Filename'),
    ('MIC2', CString('utf8') * 'Female Message Icon Filename'),
    ('BMCT', CString('utf8') * 'Ragdoll Constraint Template'),
    ('REPL', FNV_FormID(['FLST']) * 'Repair List'),
    ('BIPL', FNV_FormID(['FLST']) * 'Biped Model List'),
    ('ETYP', EquipmentTypeEnum * 'Equipment Type'),
    ('YNAM', FNV_FormID(['SOUN']) * 'Sound - Pick Up'),
    ('ZNAM', FNV_FormID(['SOUN']) * 'Sound - Drop'),
    ('DATA', Struct(
        "value" / Int32sl,
        "max_condition" / Int32sl,
        "weight" / Float32l
    ) * 'Data'),
    ('DNAM', Struct(
        "ar" / ExprAdapter(Int16sl, (obj_ / 100), (obj_ * 100)), # NOTE: value is divided by 100
        "flags" / FlagsEnum(
            Int16ul,
            modulates_voice=0x0001
        ),
        "dt" / Float32l,
        "_unknown_0" / Bytes(4)
    ) * 'Unknown'), # FIXME: missing description
    ('BNAM', Enum(
        Int32ul,
        no=0,
        yes=1
    ) * 'Overrides Animation Sounds'),
    ('SNAM', Struct(
        "sound" / FNV_FormID(['SOUN']),
        "chance" / Int8ul,
        "_unknown_0" / Bytes(3),
        "type" / Enum(
            Int32ul,
            run=19,
            run_in_armor=20,
            sneak=21,
            sneak_in_armor=22,
            walk=23,
            walk_in_armor=24
        )
    ) * 'Animation Sound'),
    ('TNAM', FNV_FormID(['ARMO']) * 'Animation Sound Template')
],
    **ModelCollection,
    **Model2Collection,
    **Model3Collection,
    **Model4Collection
)


AVIF_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('FULL', CString('utf8') * 'Name'),
    ('DESC', CString('utf8') * 'Description'),
    ('ICON', CString('utf8') * 'Large Icon Filename'),
    ('MICO', CString('utf8') * 'Small Icon Filename'),
    ('ANAM', CString('utf8') * 'Short Name')
])


BOOK_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('ICON', CString('utf8') * 'Large Icon Filename'),
    ('MICO', CString('utf8') * 'Small Icon Filename'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('DESC', CString('utf8') * 'Description'),
    ('YNAM', FNV_FormID(['SOUN']) * 'Sound - Pick Up'),
    ('ZNAM', FNV_FormID(['SOUN']) * 'Sound - Drop'),
    ('DATA', Struct(
        "flags" / FlagsEnum(
            Int8ul,
            _unknown_0=0x01,
            cant_be_taken=0x02
        ),
        "skill" / SkillEnum,
        "value" / Int32sl,
        "weight" / Float32l
    ) * 'Data')
],
    **ModelCollection,
    **DestructionCollection
)


CONT_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('DATA', Struct(
        "flags" / FlagsEnum(
            Int8ul,
            _unknown_0=0x1,
            respawns=0x2
        ),
        "weight" / Float32l
    ) * 'Data'),
    ('SNAM', FNV_FormID(['SOUN']) * 'Sound - Open'),
    ('QNAM', FNV_FormID(['SOUN']) * 'Sound - Close'),
    ('RNAM', FNV_FormID(['SOUN']) * 'Sound - Random / Looping'),
],
    **ModelCollection,
    **ItemCollection,
    **DestructionCollection
)


DOOR_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('SNAM', FNV_FormID(['SOUN']) * 'Sound - Open'),
    ('ANAM', FNV_FormID(['SOUN']) * 'Sound - Close'),
    ('BNAM', FNV_FormID(['SOUN']) * 'Sound - Looping'),
    ('FNAM', FlagsEnum(
        Int8ul,
        _unknown_0=0x01,
        automatic_door=0x02,
        hidden=0x04,
        minimal_use=0x08,
        sliding_door=0x10
    ) * 'Flags'),
],
    **ModelCollection,
    **DestructionCollection
)


FACT_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('FULL', CString('utf8') * 'Name'),
    ('XNAM', Struct(
        "faction" / FNV_FormID(['FACT', 'RACE']),
        "modifier" / Int32sl,
        "group_combat_reaction" / Enum(
            Int32ul,
            neutral=0,
            enemy=1,
            ally=2,
            friend=3
        )
    ) * 'Relation'),
    ('DATA', Struct(
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
    ) * 'Data'),
    ('CNAM', Float32l * 'Unused'),
    ('RNAM', Int32sl * 'Rank Number'),
    ('MNAM', CString('utf8') * 'Male'),
    ('FNAM', CString('utf8') * 'Female'),
    ('INAM', CString('utf8') * 'Insignia (unused)'),
    ('WMI1', FNV_FormID(['REPU']) * 'Reputation')
])


KEYM_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('ICON', CString('utf8') * 'Large Icon Filename'),
    ('MICO', CString('utf8') * 'Small Icon Filename'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('YNAM', FNV_FormID(['SOUN']) * 'Sound - Pick Up'),
    ('ZNAM', FNV_FormID(['SOUN']) * 'Sound - Drop'),
    ('DATA', Struct(
        "value" / Int32sl,
        "weight" / Float32l
    ) * 'Data'),
    ('RNAM', FNV_FormID(['SOUN']) * 'Sound - Random/Looping')
],
    **ModelCollection,
    **DestructionCollection
)


MISC_Subrecords = KEYM_Subrecords


NAVI_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('NVER', Int32ul * 'Version'),
    ('NVMI', Struct(
        "_unknown_0" / Bytes(4),
        "navigation_mesh" / FNV_FormID(['NAVM']),
        "location" / FNV_FormID(['CELL', 'WRLD']),
        "grid_x" / Int16sl,
        "grid_y" / Int16sl,
        "_unknown_1" / GreedyBytes
    ) * 'Navigation Map Info'),
    ('NVCI', Struct(
        "_unknown_0" / FNV_FormID(['NAVM']),
        "_unknown_1" / FNV_FormID(['NAVM']),
        "_unknown_2" / FNV_FormID(['NAVM']),
        "door" / FNV_FormID(['REFR']),
    ) * 'Unknown')
])


NOTE_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('ICON', CString('utf8') * 'Large Icon Filename'),
    ('MICO', CString('utf8') * 'Small Icon Filename'),
    ('YNAM', FNV_FormID(['SOUN']) * 'Sound - Pick Up'),
    ('ZNAM', FNV_FormID(['SOUN']) * 'Sound - Drop'),
    ('DATA', Enum(
        Int8ul,
        sound=0,
        text=1,
        image=2,
        voice=3
    ) * 'Type'),
    ('XNAM', CString('utf8') * 'Texture'),
    ('TNAM', CString('utf8') * 'Text / Topic'),
    ('SNAM', FNV_FormID(['SOUN', 'NPC_', 'CREA']) * 'Sound / Actor'),
],
    **ModelCollection
)


NPC__Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('ACBS', Struct(
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
    ) * 'Configuration'),
    ('SNAM', Struct(
        "faction" / FNV_FormID(['FACT']),
        "rank" / Int8ul,
        "unused" / Bytes(3)
    ) * 'Faction'),
    ('INAM', FNV_FormID(['LVLI']) * 'Death Item'),
    ('VTCK', FNV_FormID(['VTCP']) * 'Voice'),
    ('TPLT', FNV_FormID(['NPC_', 'LVLN']) * 'Template'),
    ('RNAM', FNV_FormID(['RACE']) * 'Race'),
    ('SPLO', FNV_FormID(['SPEL']) * 'Actor Effect'),
    ('EITM', FNV_FormID(['ENCH', 'SPEL']) * 'Unarmed Attack Effect'),
    ('EAMT', AttackAnimationsEnum * 'Unarmed Attack Animation'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('AIDT', Struct(
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
        "services" / ServiceFlags,
        "teaches" / SkillEnum,
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
    ) * 'AI Data'),
    ('PKID', FNV_FormID(['PACK']) * 'Package'),
    ('CNAM', FNV_FormID(['CLAS']) * 'Class'),
    ('DATA', Struct(
        "base_health" / Int32sl,
        "strength" / Int8ul,
        "perception"  / Int8ul,
        "endurance" / Int8ul,
        "charisma" / Int8ul,
        "intelligence" / Int8ul,
        "agility" / Int8ul,
        "luck" / Int8ul,
        "unused" / Optional(GreedyBytes)
    ) * 'Data'),
    ('DNAM', Struct(
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
    ) * 'Skills'),
    ('PNAM', FNV_FormID(['HDPT']) * 'Head Part'),
    ('HNAM', FNV_FormID(['HAIR']) * 'Hair'),
    ('LNAM', Float32l * 'Hair Length'),
    ('ENAM', FNV_FormID(['EYES']) * 'Eyes'),
    ('HCLR', RGBAStruct * 'Hair Color'),
    ('ZNAM', FNV_FormID(['CSTY'])),
    ('NAM4', ImpactMaterialEnum * 'Impact Material Type'),
    ('FGGS', GreedyBytes * 'Facegen Geometry - Symmetric'),
    ('FGGA', GreedyBytes * 'Facegen Geometry - Asymmetric'),
    ('FGTS', GreedyBytes * 'Facegen Texture - Symmetric'),
    ('NAM5', Int16ul * 'Unknown'),
    ('NAM6', Float32l * 'Height'),
    ('NAM7', Float32l * 'Weight'),
],
    **ModelCollection,
    **ItemCollection,
    **DestructionCollection
)


SCPT_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID')
],
    **ScriptCollection
)


STAT_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', ObjectBoundsStruct * 'Object Bounds'),
    ('BRUS', Enum(
        Int8sl,
        none=-1,
        bush_a=0,
        bush_b=1,
        bush_c=2,
        bush_d=3,
        bush_e=4,
        bush_f=5,
        bush_g=6,
        bush_h=7,
        bush_i=8,
        bush_j=9
    ) * 'Passthrough Sound'),
    ('RNAM', FNV_FormID(['SOUN']) * 'Sound - Random / Looping')
],
    **ModelCollection
)


TACT_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('SNAM', FNV_FormID(['SOUN']) * 'Looping Sound'),
    ('VNAM', FNV_FormID(['VTYP']) * 'Voice Type'),
    ('INAM', FNV_FormID(['SOUN']) * 'Radio Template'),
],
    **ModelCollection,
    **DestructionCollection
)


TES4_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OFST', GreedyBytes * 'Unknown'),
    ('DELE', GreedyBytes * 'Unknown'),
    ('HEDR', Struct(
        "version" / Float32l,
        "num_records" / Int32ul,
        "next_object_id" / Int32ul
    ) * 'Header'),
    ('CNAM', CString('utf8') * 'Author'),
    ('SNAM', CString('utf8') * 'Description'),
    ('MAST', CString('utf8') * 'Master'),
    ('DATA', Int64ul * 'File Size'),
    ('ONAM', GreedyRange(Int32ul) * 'Overridden Records'), # FIXME: Greedy FNV_FormID([REFR, ACHR, ACRE, PMIS, PBEA, PGRE, LAND, NAVM])
    ('SCRN', GreedyBytes * 'Screenshot')
])


WEAP_Subrecords = CIMultiDict([
    ('EDID', CString('utf8') * 'Editor ID'),
    ('OBND', ObjectBoundsStruct * 'Object Bounds'),
    ('FULL', CString('utf8') * 'Name'),
    ('ICON', CString('utf8') * 'Large Icon Filename'),
    ('MICO', CString('utf8') * 'Small Icon Filename'),
    ('SCRI', FNV_FormID(['SCPT']) * 'Script'),
    ('EITM', FNV_FormID(['ENCH', 'SPEL']) * 'Object Effect'),
    ('EAMT', Int16sl * 'Enchantment Charge Amount'),
    ('NAM0', FNV_FormID(['AMMO', 'FLST']) * 'Ammo'),
    ('REPL', FNV_FormID(['FLST']) * 'Repair List'),
    ('ETYP', EquipmentTypeEnum * 'Equipment Type'),
    ('BIPL', FNV_FormID(['FLST']) * 'Biped Model List'),
    ('YNAM', FNV_FormID(['SOUN']) * 'Sound - Pick Up'),
    ('ZNAM', FNV_FormID(['SOUN']) * 'Sound - Drop'),
    ('EFSD', FNV_FormID(['EFSH']) * 'Scope Effect'),
    ('MWD1', CString('utf8') * 'Model with Mod 1'),
    ('MWD2', CString('utf8') * 'Model with Mod 2'),
    ('MWD3', CString('utf8') * 'Model with Mods 1 and 2'),
    ('MWD4', CString('utf8') * 'Model with Mod 3'),
    ('MWD5', CString('utf8') * 'Model with Mods 1 and 3'),
    ('MWD6', CString('utf8') * 'Model with Mods 2 and 3'),
    ('MWD7', CString('utf8') * 'Model with Mods 1, 2, and 3'),
    ('VNAM', CString('utf8') * 'VATS Attack Name'),
    ('NNAM', CString('utf8') * 'Embedded Weapon Node'),
    ('INAM', FNV_FormID(['IPDS']) * 'Impact Dataset'),
    ('WNAM', FNV_FormID(['STAT']) * 'First Person Model'),
    ('WNM1', FNV_FormID(['STAT']) * 'First Person Model with Mod 1'),
    ('WNM2', FNV_FormID(['STAT']) * 'First Person Model with Mod 2'),
    ('WNM3', FNV_FormID(['STAT']) * 'First Person Model with Mods 1 and 2'),
    ('WNM4', FNV_FormID(['STAT']) * 'First Person Model with Mod 3'),
    ('WNM5', FNV_FormID(['STAT']) * 'First Person Model with Mods 1 and 3'),
    ('WNM6', FNV_FormID(['STAT']) * 'First Person Model with Mods 2 and 3'),
    ('WNM7', FNV_FormID(['STAT']) * 'First Person Model with Mods 1, 2, and 3'),
    ('WMI1', FNV_FormID(['IMOD']) * 'Weapon Mod 1'),
    ('WMI1', FNV_FormID(['IMOD']) * 'Weapon Mod 2'),
    ('WMI1', FNV_FormID(['IMOD']) * 'Weapon Mod 3'),
    ('SNAM', FNV_FormID(['SOUN']) * 'Sound - Gun - Shoot 3D'),
    ('SNAM', FNV_FormID(['SOUN']) * 'Sound - Gun - Shoot Distant'),
    ('XNAM', FNV_FormID(['SOUN']) * 'Sound - Gun - Shoot 2D'),
    ('NAM7', FNV_FormID(['SOUN']) * 'Sound - Gun - Shoot 3D Looping'),
    ('TNAM', FNV_FormID(['SOUN']) * 'Sound - Melee - Swing / Gun - No Ammo'),
    ('NAM6', FNV_FormID(['SOUN']) * 'Sound - Block'),
    ('UNAM', FNV_FormID(['SOUN']) * 'Sound - Idle'),
    ('NAM9', FNV_FormID(['SOUN']) * 'Sound - Equip'),
    ('NAM8', FNV_FormID(['SOUN']) * 'Sound - Unequip'),
    ('WMS1', FNV_FormID(['SOUN']) * 'Sound - Mod 1 - Shoot 3D'),
    ('WMS1', FNV_FormID(['SOUN']) * 'Sound - Mod 1 - Shoot Distant'),
    ('WMS2', FNV_FormID(['SOUN']) * 'Sound - Mod 1 - Shoot 2D'),
    ('DATA', Struct(
        "value" / Int32sl,
        "health" / Int32sl,
        "weight" / Float32l,
        "base_damage" / Int16sl,
        "clip_size" / Int8ul
    ) * 'Data'),
    ('DNAM', Struct(
        "animation_type" / WeaponAnimationEnum,
        "animation_multiplier" / Float32l,
        "reach" / Float32l,
        "flags_1" / FlagsEnum(
            Int8ul,
            ignores_normal_weapon_resistance=0x01,
            is_automatic=0x02,
            has_scope=0x04,
            cant_drop=0x08,
            hide_backpack=0x10,
            embedded_weapon=0x20,
            dont_use_first_person_animations=0x40,
            non_playable=0x80
        ),
        "grip_animation" / Enum(
            Int8ul,
            handgrip_1=230,
            handgrip_2=231,
            handgrip_3=232,
            handgrip_4=233,
            handgrip_5=234,
            handgrip_6=235,
            default=255
        ),
        "ammo_use" / Int8ul,
        "reload_animation" / ReloadAnimationEnum,
        "min_spread" / Float32l,
        "spread" / Float32l,
        "_unknown_0" / Bytes(4),
        "sight_fov" / Float32l,
        "_unknown_1" / Float32l,
        "projectile" / FNV_FormID(['PROJ']),
        "base_vats_to_hit_chance" / Int8ul,
        "attack_animation" / Enum(
            Int8ul,
            attack_left=26,
            attack_right=32,
            attack_3=38,
            attack_4=44,
            attack_5=50,
            attack_6=56,
            attack_7=62,
            attack_8=68,
            attack_loop=74,
            attack_spin=80,
            attack_spin_2=86,
            place_mine=102,
            place_mine_2=108,
            attack_throw=114,
            attack_throw_2=120,
            attack_throw_3=126,
            attack_throw_4=132,
            attack_throw_5=138,
            attack_9=144,
            attack_throw_6=150,
            attack_throw_7=156,
            attack_throw_8=162,
            default=255
        ),
        "projectile_cound" / Int8ul,
        "embedded_weapon_actor_value" / Enum(
            Int8ul,
            perception=0,
            endurance=1,
            left_attack=2,
            right_attack=3,
            left_mobility=4,
            right_mobility=5,
            brain=6
        ),
        "min_range" / Float32l,
        "max_range" / Float32l,
        "on_hit" / Enum(
            Int32ul,
            normal_formula_behavior=0,
            dismember_only=1,
            explode_only=2,
            no_dismember_explode=3
        ),
        "flags_2" / FlagsEnum(
            Int32ul,
            player_only=0x00000001,
            npcs_use_ammo=0x00000002,
            no_jam_after_reload=0x00000004,
            override_action_points=0x00000008,
            minor_crime=0x00000010,
            range_fixed=0x00000020,
            not_used_in_normal_combat=0x00000040,
            override_damage_to_weapon_multiplier=0x00000080,
            dont_use_3d_person_animations=0x00000100,
            short_burst=0x00000200,
            rumble_alternate=0x00000400,
            long_burst=0x00000800,
            scope_has_night_vision=0x00001000,
            scope_from_mod=0x00002000
        ),
        "animation_attack_multiplier" / Float32l,
        "fire_rate" / Float32l,
        "override_action_points" / Float32l,
        "rumble_left_motor_strength" / Float32l,
        "rumble_right_motor_strength" / Float32l,
        "rumble_duration" / Float32l,
        "override_damage_to_weapon_mult" / Float32l,
        "attack_shots_per_second" / Float32l,
        "reload_time" / Float32l,
        "jam_time" / Float32l,
        "aim_arc" / Float32l,
        "skill" / ActorValuesEnum,
        "rumble_pattern" / Enum(
            Int32ul,
            constant=0,
            square=1,
            triangle=2,
            sawtooth=3
        ),
        "rumble_wavelength" / Float32l,
        "limb_damage_multiplier" / Float32l,
        "reistance_type" / ActorValuesEnum,
        "sight_usage" / Float32l,
        "semi_automatic_fire_delay_min" / Float32l,
        "semi_automatic_fire_delay_max" / Float32l,
        "_unknown_2" / Float32l,
        "effect_mod_1" / ModEffectEnum,
        "effect_mod_2" / ModEffectEnum,
        "effect_mod_3" / ModEffectEnum,
        "value_a_mod_1" / Float32l,
        "value_a_mod_2" / Float32l,
        "value_a_mod_3" / Float32l,
        "override_power_attack_animation" / Enum(
            Int32ul,
            _unknown_0=0,
            attack_custom_1_power=97,
            attack_custom_2_power=98,
            attack_custom_3_power=99,
            attack_custom_4_power=100,
            attack_custom_5_power=101,
            default=255
        ),
        "strength_requirement" / Int32ul,
        "_unknown_3" / Byte,
        "reload_animation_mod" / ReloadAnimationEnum,
        "_unknown_4" / Bytes(2),
        "regen_rate" / Float32l,
        "kill_impulse" / Float32l,
        "value_b_mod_1" / Float32l,
        "value_b_mod_2" / Float32l,
        "value_b_mod_3" / Float32l,
        "impulse_distance" / Float32l,
        "skill_requirement" / Int32ul
    ) * 'Configuration'),
    ('CRDT', Struct(
        "critical_damage" / Int16ul,
        "_unused_0" / Bytes(2),
        "critical_percentage_multiplier" / Float32l,
        "flags" / FlagsEnum(
            Int8ul,
            on_death=0x01
        ),
        "_unused_1" / Bytes(3),
        "effect" / FNV_FormID(['SPEL'])
    ) * 'Critical Data'),
    ('VATS', Struct(
        "effect" / FNV_FormID(['SPEL']),
        "skill" / Float32l,
        "damage_multiplier" / Float32l,
        "ap" / Float32l,
        "silent" / Enum(
            Int8ul,
            no=0,
            yes=1
        ),
        "mod_required" / Enum(
            Int8ul,
            no=0,
            yes=1
        ),
        "_unused_0" / Bytes(2)
    ) * 'VATS'),
    ('VNAM', SoundLevelEnum * 'Sound Level')
],
    **ModelCollection,
    **DestructionCollection,
    **Model2Collection,
    **Model3Collection,
    **Model4Collection
)


RecordMap = CIMultiDict({
    'ACHR': None,
    'ACRE': None,
    'ACTI': ACTI_Subrecords,
    'ADDN': None,
    'ALCH': None,
    'ALOC': None,
    'AMEF': None,
    'AMMO': AMMO_Subrecords,
    'ANIO': None,
    'ARMO': ARMO_Subrecords,
    'ARMA': None,
    'ASPC': None,
    'AVIF': AVIF_Subrecords,
    'BOOK': BOOK_Subrecords,
    'BPTD': None,
    'CAMS': None,
    'CCRD': None,
    'CDCK': None,
    'CELL': None,
    'CHAL': None,
    'CHIP': None,
    'CLAS': None,
    'CLMT': None,
    'CMNY': None,
    'COBJ': None,
    'CONT': CONT_Subrecords,
    'CPTH': None,
    'CREA': None,
    'CSNO': None,
    'CSTY': None,
    'DEBR': None,
    'DEHY': None,
    'DIAL': None,
    'DOBJ': None,
    'DOOR': DOOR_Subrecords,
    'ECZN': None,
    'EFSH': None,
    'ENCH': None,
    'EXPL': None,
    'EYES': None,
    'FACT': FACT_Subrecords,
    'FLST': None,
    'FURN': None,
    'GLOB': None,
    'GMST': None,
    'GRAS': None,
    'HAIR': None,
    'HDPT': None,
    'HUNG': None,
    'IDLE': None,
    'IDLM': None,
    'IMGS': None,
    'IMAD': None,
    'IMOD': None,
    'INFO': None,
    'INGR': None,
    'IPCT': None,
    'IPDS': None,
    'KEYM': KEYM_Subrecords,
    'LAND': None,
    'LGMT': None,
    'LIGH': None,
    'LSCR': None,
    'LSCT': None,
    'LTEX': None,
    'LVLC': None,
    'LVLI': None,
    'LVLN': None,
    'MESG': None,
    'MGEF': None,
    'MICN': None,
    'MISC': MISC_Subrecords,
    'MSET': None,
    'MSTT': None,
    'MUSC': None,
    'NAVI': NAVI_Subrecords,
    'NAVM': None,
    'NOTE': NOTE_Subrecords,
    'NPC_': NPC__Subrecords,
    'PACK': None,
    'PERK': None,
    'PGRE': None,
    'PMIS': None,
    'PROJ': None,
    'PWAT': None,
    'QUST': None,
    'RACE': None,
    'RADS': None,
    'RCCT': None,
    'RCPE': None,
    'REFR': None,
    'REGN': None,
    'REPU': None,
    'RGDL': None,
    'SCOL': None,
    'SCPT': SCPT_Subrecords,
    'SLPD': None,
    'SOUN': None,
    'SPEL': None,
    'STAT': STAT_Subrecords,
    'TACT': TACT_Subrecords,
    'TERM': None,
    'TES4': TES4_Subrecords,
    'TREE': None,
    'TXST': None,
    'VTYP': None,
    'WATR': None,
    'WEAP': WEAP_Subrecords,
    'WRLD': None,
    'WTHR': None,
})
