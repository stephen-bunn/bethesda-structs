# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://choosealicense.com/licenses/mit/>

from construct import (
    Enum,
    Bytes,
    Int8sl,
    Int8ul,
    Struct,
    CString,
    Int16sl,
    Int16ul,
    Int32sl,
    Int32ul,
    Int64ul,
    Float32l,
    Optional,
    FlagsEnum,
    ExprAdapter,
    GreedyBytes,
    GreedyRange,
)

from ._common import (
    FNVFormID,
    SkillEnum,
    CTDAStruct,
    RGBAStruct,
    ServiceFlags,
    ModEffectEnum,
    ItemCollection,
    SoundLevelEnum,
    ActorValuesEnum,
    ModelCollection,
    EffectCollection,
    Model2Collection,
    Model3Collection,
    Model4Collection,
    ScriptCollection,
    EquipmentTypeEnum,
    ImpactMaterialEnum,
    ObjectBoundsStruct,
    ReloadAnimationEnum,
    WeaponAnimationEnum,
    AttackAnimationsEnum,
    DestructionCollection,
)
from .._common import Subrecord, SubrecordCollection

ACTI_Subrecords = SubrecordCollection(
    [
        Subrecord("EDID", CString("utf8") * "Editor ID"),
        Subrecord("OBND", ObjectBoundsStruct * "Object Bounds"),
        Subrecord("FULL", CString("utf8") * "Name", optional=True),
        ModelCollection.be(optional=True),
        Subrecord("SCRI", FNVFormID(["SCPT"]) * "Script", optional=True),
        DestructionCollection.be(optional=True),
        Subrecord("SNAM", FNVFormID(["SOUN"]) * "Sound - Looping", optional=True),
        Subrecord("VNAM", FNVFormID(["SOUN"]) * "Sound - Activation", optional=True),
        Subrecord("INAM", FNVFormID(["SOUN"]) * "Radio Template", optional=True),
        Subrecord("RNAM", FNVFormID(["TACT"]) * "Radio Station", optional=True),
        Subrecord("WNAM", FNVFormID(["WATR"]) * "Water Type", optional=True),
        Subrecord("XATO", CString("utf8") * "Activation Prompt", optional=True),
    ]
)


AMMO_Subrecords = SubrecordCollection(
    [
        Subrecord("EDID", CString("utf8") * "Editor ID"),
        Subrecord("OBND", ObjectBoundsStruct * "Object Bounds"),
        Subrecord("FULL", CString("utf8") * "Name"),
        ModelCollection.be(optional=True),
        Subrecord("ICON", CString("utf8") * "Large Icon Filename", optional=True),
        Subrecord("MICO", CString("utf8") * "Small Icon Filename", optional=True),
        Subrecord("SCRI", FNVFormID(["SCPT"]) * "Script", optional=True),
        DestructionCollection.be(optional=True),
        Subrecord("YNAM", FNVFormID(["SOUN"]) * "Sound - Pick Up", optional=True),
        Subrecord("ZNAM", FNVFormID(["SOUN"]) * "Sound - Drop", optional=True),
        Subrecord(
            "DATA",
            Struct(
                "speed" / Float32l,
                "flags"
                / FlagsEnum(
                    Int8ul, ignores_normal_weapon_resistance=0x1, non_playable=0x2
                ),
                "unused" / Bytes(3),
                "value" / Int32sl,
                "clip_rounds" / Int8ul,
            ),
        ),
        Subrecord(
            "DAT2",
            Struct(
                "projectiles_per_shot" / Int32ul,
                "projectile" / FNVFormID(["PROJ"]),
                "weight" / Float32l,
                "consumed_ammo" / FNVFormID(["AMMO", "MISC"]),
                "consumed_percentage" / Float32l,
            ),
            optional=True,
        ),
        Subrecord("ONAM", CString("utf8") * "Short Name", optional=True),
        Subrecord("QNAM", CString("utf8") * "Abbreviation", optional=True),
        Subrecord(
            "RCIL", FNVFormID(["AMEF"]) * "Ammo Effect", optional=True, multiple=True
        ),
    ]
)


ARMO_Subrecords = SubrecordCollection(
    [
        Subrecord("EDID", CString("utf8") * "Editor ID"),
        Subrecord("OBND", ObjectBoundsStruct * "Object Bounds"),
        Subrecord("FULL", CString("utf8") * "Name", optional=True),
        Subrecord("SCRI", FNVFormID(["SCPT"]) * "Script", optional=True),
        Subrecord("EITM", FNVFormID(["ENCH", "SPEL"]) * "Object Effect", optional=True),
        Subrecord(
            "BMDT",
            Struct(
                "biped_flags"
                / FlagsEnum(
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
                    body_addon_3=0x00080000,
                ),
                "general_flags"
                / FlagsEnum(
                    Int8ul,
                    unknown_1=0x01,
                    unknown_2=0x02,
                    has_backpack=0x04,
                    medium=0x08,
                    unknown_3=0x10,
                    power_armor=0x20,
                    non_playable=0x40,
                    heavy=0x80,
                ),
                "unused" / GreedyBytes,
            )
            * "Biped Data"
        ),
        ModelCollection,
        Model2Collection,
        Subrecord(
            "ICON", CString("utf8") * "Male Inventory Icon Filename", optional=True
        ),
        Subrecord(
            "MICO", CString("utf8") * "Male Message Icon Filename", optional=True
        ),
        Model3Collection,
        Model4Collection,
        Subrecord(
            "ICO2", CString("utf8") * "Female Inventory Icon Filename", optional=True
        ),
        Subrecord(
            "MIC2", CString("utf8") * "Female Message Icon Filename", optional=True
        ),
        Subrecord(
            "BMCT", CString("utf8") * "Ragdoll Constraint Template", optional=True
        ),
        Subrecord("REPL", FNVFormID(["FLST"]) * "Repair List", optional=True),
        Subrecord("BIPL", FNVFormID(["FLST"]) * "Biped Model List", optional=True),
        Subrecord("ETYP", EquipmentTypeEnum * "Equipment Type"),
        Subrecord("YNAM", FNVFormID(["SOUN"]) * "Sound - Pick Up", optional=True),
        Subrecord("ZNAM", FNVFormID(["SOUN"]) * "Sound - Drop", optional=True),
        Subrecord(
            "DATA",
            Struct("value" / Int32sl, "max_condition" / Int32sl, "weight" / Float32l)
            * "Data"
        ),
        Subrecord(
            "DNAM",
            Struct(
                "ar"
                / ExprAdapter(
                    Int16sl, lambda obj_: (obj_ / 100), lambda obj_: (obj_ * 100)
                ),  # NOTE: value is divided by 100
                "flags" / FlagsEnum(Int16ul, modulates_voice=0x0001),
                "dt" / Float32l,
                "_unknown_0" / Bytes(4),
            )
            * "Unknown"
        ),  # FIXME: missing description
        Subrecord(
            "BNAM",
            Enum(Int32ul, no=0, yes=1) * "Overrides Animation Sounds",
            optional=True
        ),
        Subrecord(
            "SNAM",
            Struct(
                "sound" / FNVFormID(["SOUN"]),
                "chance" / Int8ul,
                "_unknown_0" / Bytes(3),
                "type"
                / Enum(
                    Int32ul,
                    run=19,
                    run_in_armor=20,
                    sneak=21,
                    sneak_in_armor=22,
                    walk=23,
                    walk_in_armor=24,
                ),
            )
            * "Animation Sound",
            optional=True,
            multiple=True
        ),
        Subrecord(
            "TNAM", FNVFormID(["ARMO"]) * "Animation Sound Template", optional=True
        ),
    ]
)


AVIF_Subrecords = SubrecordCollection(
    [
        Subrecord("EDID", CString("utf8") * "Editor ID"),
        Subrecord("FULL", CString("utf8") * "Name", optional=True),
        Subrecord("DESC", CString("utf8") * "Description"),
        Subrecord("ICON", CString("utf8") * "Large Icon Filename", optional=True),
        Subrecord("MICO", CString("utf8") * "Small Icon Filename", optional=True),
        Subrecord("ANAM", CString("utf8") * "Short Name", optional=True),
    ]
)


CONT_Subrecords = SubrecordCollection(
    [
        Subrecord("EDID", CString("utf8") * "Editor ID"),
        Subrecord("OBND", ObjectBoundsStruct * "Object Bounds"),
        Subrecord("FULL", CString("utf8") * "Name", optional=True),
        ModelCollection,
        Subrecord("SCRI", FNVFormID(["SCPT"]) * "Script", optional=True),
        ItemCollection.be(optional=True, multiple=True),
        DestructionCollection.be(optional=True),
        Subrecord(
            "DATA",
            Struct(
                "flags" / FlagsEnum(Int8ul, _unknown_0=0x1, respawns=0x2),
                "weight" / Float32l,
            )
            * "Data",
            optional=True
        ),
        Subrecord("SNAM", FNVFormID(["SOUN"]) * "Sound - Open", optional=True),
        Subrecord("QNAM", FNVFormID(["SOUN"]) * "Sound - Close", optional=True),
        Subrecord(
            "RNAM", FNVFormID(["SOUN"]) * "Sound - Random / Looping", optional=True
        ),
    ]
)


DIAL_Subrecords = SubrecordCollection(
    [
        Subrecord("EDID", CString("utf8") * "Editor ID"),
        SubrecordCollection(
            [
                Subrecord("QSTI", FNVFormID(["QUST"]) * "Quest", optional=True),
                SubrecordCollection(
                    [
                        Subrecord(
                            "INFC",
                            FNVFormID(["INFO"]) * "Info Connection",
                            optional=True
                        ),
                        Subrecord("INFX", Int32sl * "Info Index", optional=True),
                    ],
                    optional=True,
                    multiple=True,
                ),
            ],
            optional=True,
            multiple=True,
        ),
        Subrecord(
            "QSTR", FNVFormID(["QUST"]) * "Removed Quest", optional=True, multiple=True
        ),
        SubrecordCollection(
            [
                Subrecord("INFC", GreedyBytes * "Unused", optional=True),
                Subrecord("INFX", GreedyBytes * "Unused", optional=True),
            ],
            optional=True,
            multiple=True,
        ),
        Subrecord("FULL", CString("utf8") * "Name"),
        Subrecord("PNAM", Float32l * "Priority"),
        Subrecord("TDUM", CString("utf8"), optional=True),
        Subrecord(
            "DATA",
            Struct(
                "type"
                / Enum(
                    Int8ul,
                    topic=0,
                    conversation=1,
                    combat=2,
                    persuasion=3,
                    detection=4,
                    service=5,
                    miscellaneous=6,
                    radio=7,
                ),
                "flags" / FlagsEnum(Int8ul, rumors=0x01, top_level=0x02),
            )
            * "Data"
        ),
    ]
)


DOOR_Subrecords = SubrecordCollection(
    [
        Subrecord("EDID", CString("utf8") * "Editor ID"),
        Subrecord("OBND", ObjectBoundsStruct * "Object Bounds"),
        Subrecord("FULL", CString("utf8") * "Name", optional=True),
        ModelCollection,
        Subrecord("SCRI", FNVFormID(["SCPT"]) * "Script", optional=True),
        DestructionCollection.be(optional=True),
        Subrecord("SNAM", FNVFormID(["SOUN"]) * "Sound - Open", optional=True),
        Subrecord("ANAM", FNVFormID(["SOUN"]) * "Sound - Close", optional=True),
        Subrecord("BNAM", FNVFormID(["SOUN"]) * "Sound - Looping", optional=True),
        Subrecord(
            "FNAM",
            FlagsEnum(
                Int8ul,
                _unknown_0=0x01,
                automatic_door=0x02,
                hidden=0x04,
                minimal_use=0x08,
                sliding_door=0x10,
            )
            * "Flags"
        ),
    ]
)


FACT_Subrecords = SubrecordCollection(
    [
        Subrecord("EDID", CString("utf8") * "Editor ID"),
        Subrecord("FULL", CString("utf8") * "Name", optional=True),
        Subrecord(
            "XNAM",
            Struct(
                "faction" / FNVFormID(["FACT", "RACE"]),
                "modifier" / Int32sl,
                "group_combat_reaction"
                / Enum(Int32ul, neutral=0, enemy=1, ally=2, friend=3),
            )
            * "Relation",
            optional=True,
            multiple=True
        ),
        Subrecord(
            "DATA",
            Struct(
                "flags_1"
                / FlagsEnum(
                    Int8ul, hidden_from_pc=0x01, evil=0x02, special_combat=0x04
                ),
                "flags_2" / FlagsEnum(Int8ul, track_crime=0x01, allow_sell=0x02),
                "unused" / Bytes(2),
            )
            * "Data",
            optional=True
        ),
        Subrecord("CNAM", Float32l * "Unused", optional=True),
        SubrecordCollection(
            [
                Subrecord("RNAM", Int32sl * "Rank Number", optional=True),
                Subrecord("MNAM", CString("utf8") * "Male", optional=True),
                Subrecord("FNAM", CString("utf8") * "Female", optional=True),
                Subrecord("INAM", CString("utf8") * "Insignia (unused)", optional=True),
            ],
            optional=True,
            multiple=True,
        ),
        Subrecord("WMI1", FNVFormID(["REPU"]) * "Reputation", optional=True),
    ]
)


KEYM_Subrecords = SubrecordCollection(
    [
        Subrecord("EDID", CString("utf8") * "Editor ID"),
        Subrecord("OBND", ObjectBoundsStruct * "Object Bounds"),
        Subrecord("FULL", CString("utf8") * "Name"),
        ModelCollection.be(optional=True),
        Subrecord("ICON", CString("utf8") * "Large Icon Filename"),
        Subrecord("MICO", CString("utf8") * "Small Icon Filename"),
        Subrecord("SCRI", FNVFormID(["SCPT"]) * "Script", optional=True),
        DestructionCollection.be(optional=True),
        Subrecord("YNAM", FNVFormID(["SOUN"]) * "Sound - Pick Up", optional=True),
        Subrecord("ZNAM", FNVFormID(["SOUN"]) * "Sound - Drop", optional=True),
        Subrecord(
            "DATA",
            Struct("value" / Int32sl, "weight" / Float32l) * "Data",
            optional=True
        ),
        Subrecord(
            "RNAM", FNVFormID(["SOUN"]) * "Sound - Random/Looping", optional=True
        ),
    ]
)


MISC_Subrecords = KEYM_Subrecords


MESG_Subrecords = SubrecordCollection(
    [
        Subrecord("EDID", CString("utf8") * "Editor ID"),
        Subrecord("DESC", CString("utf8") * "Description"),
        Subrecord("FULL", CString("utf8") * "Name", optional=True),
        Subrecord("INAM", FNVFormID(["MICN"]) * "Icon"),
        Subrecord("NAM1", GreedyBytes * "Unknown", optional=True),
        Subrecord("NAM2", GreedyBytes * "Unknown", optional=True),
        Subrecord("NAM3", GreedyBytes * "Unknown", optional=True),
        Subrecord("NAM4", GreedyBytes * "Unknown", optional=True),
        Subrecord("NAM5", GreedyBytes * "Unknown", optional=True),
        Subrecord("NAM6", GreedyBytes * "Unknown", optional=True),
        Subrecord("NAM7", GreedyBytes * "Unknown", optional=True),
        Subrecord("NAM8", GreedyBytes * "Unknown", optional=True),
        Subrecord("NAM9", GreedyBytes * "Unknown", optional=True),
        Subrecord(
            "DNAM",
            FlagsEnum(Int32ul, message_box=0x00000001, auto_display=0x00000002)
            * "Flags"
        ),
        Subrecord("TNAM", Int32ul * "Display Time", optional=True),
        SubrecordCollection(
            [
                Subrecord("ITXT", CString("utf8") * "Button Text", optional=True),
                Subrecord(
                    "CTDA", CTDAStruct * "Condition", optional=True, multiple=True
                ),
            ]
        ),
    ]
)


NAVI_Subrecords = SubrecordCollection(
    [
        Subrecord("EDID", CString("utf8") * "Editor ID", optional=True),
        Subrecord("NVER", Int32ul * "Version", optional=True),
        Subrecord(
            "NVMI",
            Struct(
                "_unknown_0" / Bytes(4),
                "navigation_mesh" / FNVFormID(["NAVM"]),
                "location" / FNVFormID(["CELL", "WRLD"]),
                "grid_x" / Int16sl,
                "grid_y" / Int16sl,
                "_unknown_1" / GreedyBytes,
            )
            * "Navigation Map Info",
            optional=True,
            multiple=True
        ),
        Subrecord(
            "NVCI",
            Struct(
                "_unknown_0" / FNVFormID(["NAVM"]),
                "_unknown_1" / FNVFormID(["NAVM"]),
                "_unknown_2" / FNVFormID(["NAVM"]),
                "door" / FNVFormID(["REFR"]),
            )
            * "Unknown",
            optional=True,
            multiple=True
        ),
    ]
)


NOTE_Subrecords = SubrecordCollection(
    [
        Subrecord("EDID", CString("utf8") * "Editor ID"),
        Subrecord("OBND", ObjectBoundsStruct * "Object Bounds"),
        Subrecord("FULL", CString("utf8") * "Name"),
        ModelCollection.be(optional=True),
        Subrecord("ICON", CString("utf8") * "Large Icon Filename", optional=True),
        Subrecord("MICO", CString("utf8") * "Small Icon Filename", optional=True),
        Subrecord("YNAM", FNVFormID(["SOUN"]) * "Sound - Pick Up", optional=True),
        Subrecord("ZNAM", FNVFormID(["SOUN"]) * "Sound - Drop", optional=True),
        Subrecord(
            "DATA",
            Enum(Int8ul, sound=0, text=1, image=2, voice=3) * "Type",
            optional=True
        ),
        Subrecord("ONAM", FNVFormID(["QUST"]) * "Quest", optional=True, multiple=True),
        Subrecord("XNAM", CString("utf8") * "Texture", optional=True),
        Subrecord("TNAM", CString("utf8") * "Text / Topic", optional=True),
        Subrecord(
            "SNAM", FNVFormID(["SOUN", "NPC_", "CREA"]) * "Sound / Actor", optional=True
        ),
    ]
)


NPC__Subrecords = SubrecordCollection(
    [
        Subrecord("EDID", CString("utf8") * "Editor ID"),
        Subrecord("OBND", ObjectBoundsStruct * "Object Bounds"),
        Subrecord("FULL", CString("utf8") * "Name", optional=True),
        ModelCollection.be(optional=True),
        Subrecord(
            "ACBS",
            Struct(
                "flags"
                / FlagsEnum(
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
                    _unknown_15=0x80000000,
                ),
                "fatigue" / Int16ul,
                "barter_gold" / Int16ul,
                "level" / Int16sl,
                "calc_min" / Int16ul,
                "calc_max" / Int16ul,
                "speed_multiplier" / Int16ul,
                "karma" / Float32l,
                "disposition_base" / Int16sl,
                "template_flags"
                / FlagsEnum(
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
            * "Configuration"
        ),
        Subrecord(
            "SNAM",
            Struct(
                "faction" / FNVFormID(["FACT"]), "rank" / Int8ul, "unused" / Bytes(3)
            )
            * "Faction",
            optional=True,
            multiple=True
        ),
        Subrecord("INAM", FNVFormID(["LVLI"]) * "Death Item", optional=True),
        Subrecord("VTCK", FNVFormID(["VTCP"]) * "Voice"),
        Subrecord("TPLT", FNVFormID(["NPC_", "LVLN"]) * "Template", optional=True),
        Subrecord("RNAM", FNVFormID(["RACE"]) * "Race"),
        Subrecord(
            "SPLO", FNVFormID(["SPEL"]) * "Actor Effect", optional=True, multiple=True
        ),
        Subrecord(
            "EITM", FNVFormID(["ENCH", "SPEL"]) * "Unarmed Attack Effect", optional=True
        ),
        Subrecord("EAMT", AttackAnimationsEnum * "Unarmed Attack Animation"),
        DestructionCollection.be(optional=True),
        Subrecord("SCRI", FNVFormID(["SCPT"]) * "Script", optional=True),
        ItemCollection.be(optional=True, multiple=True),
        Subrecord(
            "AIDT",
            Struct(
                "aggression"
                / Enum(
                    Int8ul, unaggressive=0, aggressive=1, very_aggressive=2, frenzied=3
                ),
                "confidence"
                / Enum(Int8ul, cowardly=0, cautious=1, average=2, brave=3, foolhardy=4),
                "energy_level" / Int8ul,
                "responsibility" / Int8ul,
                "mood"
                / Enum(
                    Int8ul,
                    neutral=0,
                    afraid=1,
                    annoyed=2,
                    cocky=3,
                    drugged=4,
                    pleasant=5,
                    angry=6,
                    sad=7,
                ),
                "services" / ServiceFlags,
                "teaches" / SkillEnum,
                "maximum_training_level" / Int8ul,
                "assistance"
                / Enum(
                    Int8sl, helps_nobody=0, helps_allies=1, helps_friends_and_allies=2
                ),
                "aggro_radius_behavior" / FlagsEnum(Int8ul, aggro_radius_behavior=0x01),
                "aggro_radius" / Int32sl,
            )
            * "AI Data",
            optional=True
        ),
        Subrecord(
            "PKID", FNVFormID(["PACK"]) * "Package", optional=True, multiple=True
        ),
        Subrecord("CNAM", FNVFormID(["CLAS"]) * "Class"),
        Subrecord(
            "DATA",
            Struct(
                "base_health" / Int32sl,
                "strength" / Int8ul,
                "perception" / Int8ul,
                "endurance" / Int8ul,
                "charisma" / Int8ul,
                "intelligence" / Int8ul,
                "agility" / Int8ul,
                "luck" / Int8ul,
                "unused" / Optional(GreedyBytes),
            )
            * "Data"
        ),
        Subrecord(
            "DNAM",
            Struct(
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
            * "Skills",
            optional=True
        ),
        Subrecord(
            "PNAM", FNVFormID(["HDPT"]) * "Head Part", optional=True, multiple=True
        ),
        Subrecord("HNAM", FNVFormID(["HAIR"]) * "Hair", optional=True),
        Subrecord("LNAM", Float32l * "Hair Length", optional=True),
        Subrecord("ENAM", FNVFormID(["EYES"]) * "Eyes", optional=True),
        Subrecord("HCLR", RGBAStruct * "Hair Color"),
        Subrecord("ZNAM", FNVFormID(["CSTY"]), optional=True),
        Subrecord("NAM4", ImpactMaterialEnum * "Impact Material Type"),
        Subrecord("FGGS", GreedyBytes * "Facegen Geometry - Symmetric"),
        Subrecord("FGGA", GreedyBytes * "Facegen Geometry - Asymmetric"),
        Subrecord("FGTS", GreedyBytes * "Facegen Texture - Symmetric"),
        Subrecord("NAM5", Int16ul * "Unknown"),
        Subrecord("NAM6", Float32l * "Height"),
        Subrecord("NAM7", Float32l * "Weight"),
    ]
)

SCPT_Subrecords = SubrecordCollection(
    [Subrecord("EDID", CString("utf8") * "Editor ID"), ScriptCollection]
)


SPEL_Subrecords = SubrecordCollection(
    [
        Subrecord("EDID", CString("utf8") * "Editor ID"),
        Subrecord("FULL", CString("utf8") * "Name", optional=True),
        Subrecord(
            "SPIT",
            Struct(
                "type"
                / Enum(
                    Int32ul,
                    actor_effect=0,
                    disease=1,
                    power=2,
                    lesser_power=3,
                    ability=4,
                    poison=5,
                    _unknown_0=6,
                    _unknown_1=7,
                    _unknown_2=8,
                    _unknown_3=9,
                    addiction=10,
                ),
                "cost" / Int32ul,
                "level" / Int32ul,
                "flags"
                / FlagsEnum(
                    Int8ul,
                    no_auto_calc=0x01,
                    immune_to_silence_1=0x02,
                    pc_start_effect=0x04,
                    immune_to_silence_2=0x08,
                    area_effect_ignores_los=0x10,
                    script_effect_always_applies=0x20,
                    disable_absorb_reflect=0x40,
                    force_touch_explode=0x80,
                ),
                "_unknown_0" / Bytes(3),
            )
            * "Effect Configuration"
        ),
        EffectCollection.be(multiple=True),
    ]
)


STAT_Subrecords = SubrecordCollection(
    [
        Subrecord("EDID", CString("utf8") * "Editor ID"),
        Subrecord("OBND", ObjectBoundsStruct * "Object Bounds"),
        ModelCollection.be(optional=True),
        Subrecord(
            "BRUS",
            Enum(
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
                bush_j=9,
            )
            * "Passthrough Sound",
            optional=True
        ),
        Subrecord(
            "RNAM", FNVFormID(["SOUN"]) * "Sound - Random / Looping", optional=True
        ),
    ]
)


TACT_Subrecords = SubrecordCollection(
    [
        Subrecord("EDID", CString("utf8") * "Editor ID"),
        Subrecord("OBND", ObjectBoundsStruct * "Object Bounds"),
        Subrecord("FULL", CString("utf8") * "Name", optional=True),
        ModelCollection,
        Subrecord("SCRI", FNVFormID(["SCPT"]) * "Script", optional=True),
        DestructionCollection.be(optional=True),
        Subrecord("SNAM", FNVFormID(["SOUN"]) * "Looping Sound", optional=True),
        Subrecord("VNAM", FNVFormID(["VTYP"]) * "Voice Type", optional=True),
        Subrecord("INAM", FNVFormID(["SOUN"]) * "Radio Template", optional=True),
    ]
)


TES4_Subrecords = SubrecordCollection(
    [
        Subrecord(
            "HEDR",
            Struct(
                "version" / Float32l,
                "num_records" / Int32ul,
                "next_object_id" / Int32ul,
            )
            * "Header"
        ),
        Subrecord("OFST", GreedyBytes * "Unknown", optional=True),
        Subrecord("DELE", GreedyBytes * "Unknown", optional=True),
        Subrecord("CNAM", CString("utf8") * "Author"),
        Subrecord("SNAM", CString("utf8") * "Description", optional=True),
        SubrecordCollection(
            [
                Subrecord("MAST", CString("utf8") * "Master Plugin"),
                Subrecord("DATA", Int64ul * "File Size"),
            ],
            optional=True,
            multiple=True,
        ),
        Subrecord(
            "ONAM", GreedyRange(Int32ul) * "Overridden Records", optional=True
        ),  # FIXME: reedy FNV_FormID([REFR, ACHR, ACRE, PMIS, PBEA, PGRE, LAND, NAVM]),
        Subrecord("SCRN", GreedyBytes * "Screenshot", optional=True),
    ]
)


WEAP_Subrecords = SubrecordCollection(
    [
        Subrecord("EDID", CString("utf8") * "Editor ID"),
        Subrecord("OBND", ObjectBoundsStruct * "Object Bounds"),
        Subrecord("FULL", CString("utf8") * "Name", optional=True),
        ModelCollection,
        Subrecord("ICON", CString("utf8") * "Large Icon Filename", optional=True),
        Subrecord("MICO", CString("utf8") * "Small Icon Filename", optional=True),
        Subrecord("SCRI", FNVFormID(["SCPT"]) * "Script", optional=True),
        Subrecord("EITM", FNVFormID(["ENCH", "SPEL"]) * "Object Effect", optional=True),
        Subrecord("EAMT", Int16sl * "Enchantment Charge Amount", optional=True),
        Subrecord("NAM0", FNVFormID(["AMMO", "FLST"]) * "Ammo", optional=True),
        DestructionCollection.be(optional=True),
        Subrecord("REPL", FNVFormID(["FLST"]) * "Repair List", optional=True),
        Subrecord("ETYP", EquipmentTypeEnum * "Equipment Type"),
        Subrecord("BIPL", FNVFormID(["FLST"]) * "Biped Model List", optional=True),
        Subrecord("YNAM", FNVFormID(["SOUN"]) * "Sound - Pick Up", optional=True),
        Subrecord("ZNAM", FNVFormID(["SOUN"]) * "Sound - Drop", optional=True),
        Model2Collection.be(optional=True),
        Model3Collection.be(optional=True),
        Subrecord("EFSD", FNVFormID(["EFSH"]) * "Scope Effect", optional=True),
        Model4Collection.be(optional=True),
        Subrecord("MWD1", CString("utf8") * "Model with Mod 1", optional=True),
        Subrecord("MWD2", CString("utf8") * "Model with Mod 2", optional=True),
        Subrecord("MWD3", CString("utf8") * "Model with Mods 1 and 2", optional=True),
        Subrecord("MWD4", CString("utf8") * "Model with Mod 3", optional=True),
        Subrecord("MWD5", CString("utf8") * "Model with Mods 1 and 3", optional=True),
        Subrecord("MWD6", CString("utf8") * "Model with Mods 2 and 3", optional=True),
        Subrecord(
            "MWD7", CString("utf8") * "Model with Mods 1, 2, and 3", optional=True
        ),
        Subrecord("VNAM", CString("utf8") * "VATS Attack Name", optional=True),
        Subrecord("NNAM", CString("utf8") * "Embedded Weapon Node", optional=True),
        Subrecord("INAM", FNVFormID(["IPDS"]) * "Impact Dataset", optional=True),
        Subrecord("WNAM", FNVFormID(["STAT"]) * "First Person Model", optional=True),
        Subrecord(
            "WNM1", FNVFormID(["STAT"]) * "First Person Model with Mod 1", optional=True
        ),
        Subrecord(
            "WNM2", FNVFormID(["STAT"]) * "First Person Model with Mod 2", optional=True
        ),
        Subrecord(
            "WNM3",
            FNVFormID(["STAT"]) * "First Person Model with Mods 1 and 2",
            optional=True
        ),
        Subrecord(
            "WNM4", FNVFormID(["STAT"]) * "First Person Model with Mod 3", optional=True
        ),
        Subrecord(
            "WNM5",
            FNVFormID(["STAT"]) * "First Person Model with Mods 1 and 3",
            optional=True
        ),
        Subrecord(
            "WNM6",
            FNVFormID(["STAT"]) * "First Person Model with Mods 2 and 3",
            optional=True
        ),
        Subrecord(
            "WNM7",
            FNVFormID(["STAT"]) * "First Person Model with Mods 1, 2, and 3",
            optional=True
        ),
        Subrecord("WMI1", FNVFormID(["IMOD"]) * "Weapon Mod 1", optional=True),
        Subrecord("WMI1", FNVFormID(["IMOD"]) * "Weapon Mod 2", optional=True),
        Subrecord("WMI1", FNVFormID(["IMOD"]) * "Weapon Mod 3", optional=True),
        Subrecord(
            "SNAM", FNVFormID(["SOUN"]) * "Sound - Gun - Shoot 3D", optional=True
        ),
        Subrecord(
            "SNAM", FNVFormID(["SOUN"]) * "Sound - Gun - Shoot Distant", optional=True
        ),
        Subrecord(
            "XNAM", FNVFormID(["SOUN"]) * "Sound - Gun - Shoot 2D", optional=True
        ),
        Subrecord(
            "NAM7",
            FNVFormID(["SOUN"]) * "Sound - Gun - Shoot 3D Looping",
            optional=True
        ),
        Subrecord(
            "TNAM",
            FNVFormID(["SOUN"]) * "Sound - Melee - Swing / Gun - No Ammo",
            optional=True
        ),
        Subrecord("NAM6", FNVFormID(["SOUN"]) * "Sound - Block", optional=True),
        Subrecord("UNAM", FNVFormID(["SOUN"]) * "Sound - Idle", optional=True),
        Subrecord("NAM9", FNVFormID(["SOUN"]) * "Sound - Equip", optional=True),
        Subrecord("NAM8", FNVFormID(["SOUN"]) * "Sound - Unequip", optional=True),
        Subrecord(
            "WMS1", FNVFormID(["SOUN"]) * "Sound - Mod 1 - Shoot 3D", optional=True
        ),
        Subrecord(
            "WMS1", FNVFormID(["SOUN"]) * "Sound - Mod 1 - Shoot Distant", optional=True
        ),
        Subrecord(
            "WMS2", FNVFormID(["SOUN"]) * "Sound - Mod 1 - Shoot 2D", optional=True
        ),
        Subrecord(
            "DATA",
            Struct(
                "value" / Int32sl,
                "health" / Int32sl,
                "weight" / Float32l,
                "base_damage" / Int16sl,
                "clip_size" / Int8ul,
            )
            * "Data"
        ),
        Subrecord(
            "DNAM",
            Struct(
                "animation_type" / WeaponAnimationEnum,
                "animation_multiplier" / Float32l,
                "reach" / Float32l,
                "flags_1"
                / FlagsEnum(
                    Int8ul,
                    ignores_normal_weapon_resistance=0x01,
                    is_automatic=0x02,
                    has_scope=0x04,
                    cant_drop=0x08,
                    hide_backpack=0x10,
                    embedded_weapon=0x20,
                    dont_use_first_person_animations=0x40,
                    non_playable=0x80,
                ),
                "grip_animation"
                / Enum(
                    Int8ul,
                    handgrip_1=230,
                    handgrip_2=231,
                    handgrip_3=232,
                    handgrip_4=233,
                    handgrip_5=234,
                    handgrip_6=235,
                    default=255,
                ),
                "ammo_use" / Int8ul,
                "reload_animation" / ReloadAnimationEnum,
                "min_spread" / Float32l,
                "spread" / Float32l,
                "_unknown_0" / Bytes(4),
                "sight_fov" / Float32l,
                "_unknown_1" / Float32l,
                "projectile" / FNVFormID(["PROJ"]),
                "base_vats_to_hit_chance" / Int8ul,
                "attack_animation"
                / Enum(
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
                    default=255,
                ),
                "projectile_cound" / Int8ul,
                "embedded_weapon_actor_value"
                / Enum(
                    Int8ul,
                    perception=0,
                    endurance=1,
                    left_attack=2,
                    right_attack=3,
                    left_mobility=4,
                    right_mobility=5,
                    brain=6,
                ),
                "min_range" / Float32l,
                "max_range" / Float32l,
                "on_hit"
                / Enum(
                    Int32ul,
                    normal_formula_behavior=0,
                    dismember_only=1,
                    explode_only=2,
                    no_dismember_explode=3,
                ),
                "flags_2"
                / FlagsEnum(
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
                    scope_from_mod=0x00002000,
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
                "rumble_pattern"
                / Enum(Int32ul, constant=0, square=1, triangle=2, sawtooth=3),
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
                "override_power_attack_animation"
                / Enum(
                    Int32ul,
                    _unknown_0=0,
                    attack_custom_1_power=97,
                    attack_custom_2_power=98,
                    attack_custom_3_power=99,
                    attack_custom_4_power=100,
                    attack_custom_5_power=101,
                    default=255,
                ),
                "strength_requirement" / Int32ul,
                "_unknown_3" / Bytes(1),
                "reload_animation_mod" / ReloadAnimationEnum,
                "_unknown_4" / Bytes(2),
                "regen_rate" / Float32l,
                "kill_impulse" / Float32l,
                "value_b_mod_1" / Float32l,
                "value_b_mod_2" / Float32l,
                "value_b_mod_3" / Float32l,
                "impulse_distance" / Float32l,
                "skill_requirement" / Int32ul,
            )
            * "Configuration"
        ),
        Subrecord(
            "CRDT",
            Struct(
                "critical_damage" / Int16ul,
                "_unused_0" / Bytes(2),
                "critical_percentage_multiplier" / Float32l,
                "flags" / FlagsEnum(Int8ul, on_death=0x01),
                "_unused_1" / Bytes(3),
                "effect" / FNVFormID(["SPEL"]),
            )
            * "Critical Data"
        ),
        Subrecord(
            "VATS",
            Struct(
                "effect" / FNVFormID(["SPEL"]),
                "skill" / Float32l,
                "damage_multiplier" / Float32l,
                "ap" / Float32l,
                "silent" / Enum(Int8ul, no=0, yes=1),
                "mod_required" / Enum(Int8ul, no=0, yes=1),
                "_unused_0" / Bytes(2),
            )
            * "VATS",
            optional=True
        ),
        Subrecord("VNAM", SoundLevelEnum * "Sound Level"),
    ]
)


RecordMapping = {
    "ACTI": ACTI_Subrecords,
    "AMMO": AMMO_Subrecords,
    "ARMO": ARMO_Subrecords,
    "AVIF": AVIF_Subrecords,
    "CONT": CONT_Subrecords,
    "DIAL": DIAL_Subrecords,
    "DOOR": DOOR_Subrecords,
    "FACT": FACT_Subrecords,
    "KEYM": KEYM_Subrecords,
    "MESG": MESG_Subrecords,
    "MISC": MISC_Subrecords,
    "NAVI": NAVI_Subrecords,
    "NOTE": NOTE_Subrecords,
    "NPC_": NPC__Subrecords,
    "SCPT": SCPT_Subrecords,
    "SPEL": SPEL_Subrecords,
    "STAT": STAT_Subrecords,
    "TACT": TACT_Subrecords,
    "TES4": TES4_Subrecords,
    "WEAP": WEAP_Subrecords,
}
