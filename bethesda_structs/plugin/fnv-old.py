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


FNV_OBNDStruct = Struct(
    "X1" / Int16sl,
    "Y1" / Int16sl,
    "Z1" / Int16sl,
    "X2" / Int16sl,
    "Y2" / Int16sl,
    "Z2" / Int16sl,
)

FNV_BMDTStruct = Struct(
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
    "unused" / Byte[:]
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


FNV_EffectCollection = {
    'EFID': FNV_FormID(['MGEF']),
    'EFIT': Struct(
        "magnitude" / Int32ul,
        "area" / Int32ul,
        "duration" / Int32ul,
        "type" / Enum(
            Int32ul,
            _self=0,
            touch=1,
            target=2
        ),
        "actor_value" / Enum(
            Int32sl,
            none=-1,
            aggression=0,
            confidence=1,
            energy=2,
            responsibility=3,
            mood=4,
            strength=5,
            perception=6,
            endurance=7,
            charisma=8,
            intelligence=9,
            agility=10,
            luck=11,
            action_points=12,
            carry_weight=13,
            critical_chance=14,
            heal_rate=15,
            health=16,
            melee_damage=17,
            damage_resistance=18,
            poison_resistance=19,
            rad_resistance=20,
            speed_multiplier=21,
            fatigue=22,
            karma=23,
            xp=24,
            perception_condition=25,
            endurance_condition=26,
            left_attack_condition=27,
            right_attack_condition=28,
            left_mobility_condition=29,
            right_mobility_condition=30,
            brain_condition=31,
            barter=32,
            big_guns=33,
            energy_weapons=34,
            explosives=35,
            lockpick=36,
            medicine=37,
            melee_weapons=38,
            repair=39,
            science=40,
            small_guns=41,
            sneak=42,
            speech=43,
            throwing=44,
            unarmed=45,
            inventory_weight=46,
            paralysis=47,
            invisibility=48,
            chameleon=49,
            night_eye=50,
            detect_life_range=51,
            fire_resistance=52,
            water_breathing=53,
            rad_level=54,
            bloody_mess=55,
            unarmed_damage=56,
            assistance=57,
            electric_resistance=58,
            frost_resistance=59,
            energy_resistance=60,
            emp_resistance=61,
            unknown_0=62,
            unknown_1=63,
            unknown_2=64,
            unknown_3=65,
            unknown_4=66,
            unknown_5=67,
            unknown_6=68,
            unknown_7=69,
            unknown_8=70,
            unknown_9=71,
            ignore_negative_effects=72,
        )
    ),
    'CTDA': Struct( # TODO: Finish CTDA subrecord
        "type" / Enum(
            Int8ul,
            combine_next_condition_using_or=0x0001,
            run_on_target=0x0002,
            use_global=0x0004,
            equal_to=0x0000,
            not_equal_to=0x2000,
            greater_than=0x4000,
            greater_than_or_equal_to=0x6000,
            less_than=0x8000,
            less_than_or_equal_to=0xa000
        ),
        "unused" / Bytes(3),
        "comparison_value" / FNV_FormID(['GLOB']), # FIXME: multiple types
        "function" / Enum(
            Int32ul,
            GetDistance=1,
            GetLocked=5,
            GetPos=6,
            GetAngle=8,
            GetStartingPos=10,
            GetStartingAngle=11,
            GetSecondsPassed=12,
            GetActorValue=14,
            GetCurrentTime=18,
            GetScale=24,
            IsMoving=25,
            IsTurning=26,
            GetLineOfSight=27,
            GetInSameCell=32,
            GetDisabled=35,
            MenuMode=36,
            GetDisease=39,
            GetVampire=40,
            GetClothingValue=41,
            SameFaction=42,
            SameRace=43,
            SameSex=44,
            GetDetected=45,
            GetDead=46,
            GetItemCount=47,
            GetGold=48,
            GetSleeping=49,
            GetTalkedToPC=50,
            GetScriptVariable=53,
            GetQuestRunning=56,
            GetStage=58,
            GetStageDone=59,
            GetFactionRankDifference=60,
            GetAlarmed=61,
            IsRaining=62,
            GetAttacked=63,
            GetIsCreature=64,
            GetLockLevel=65,
            GetShouldAttack=66,
            GetInCell=67,
            GetIsClass=68,
            GetIsRace=69,
            GetIsSex=70,
            GetInFaction=71,
            GetIsID=72,
            GetFactionRank=73,
            GetGlobalValue=74,
            IsSnowing=75,
            GetDisposition=76,
            GetRandomPercent=77,
            GetQuestVariable=79,
            GetLevel=80,
            GetArmorRating=81,
            GetDeadCount=84,
            GetIsAlerted=91,
            GetPlayerControlsDisabled=98,
            GetHeadingAngle=99,
            IsWeaponOut=101,
            IsTorchOut=102,
            IsShieldOut=103,
            IsFacingUp=106,
            GetKnockedState=107,
            GetWeaponAnimType=108,
            IsWeaponSkillType=109,
            GetCurrentAIPackage=110,
            IsWaiting=111,
            IsIdlePlaying=112,
            GetMinorCrimeCount=116,
            GetMajorCrimeCount=117,
            GetActorAggroRadiusViolated=118,
            GetCrime=122,
            IsGreetingPlayer=123,
            IsGuard=125,
            HasBeenEaten=127,
            GetFatiguePercentage=128,
            GetPCIsClass=129,
            GetPCIsRace=130,
            GetPCIsSex=131,
            GetPCInFaction=132,
            SameFactionAsPC=133,
            SameRaceAsPC=134,
            SameSexAsPC=135,
            GetIsReference=136,
            IsTalking=141,
            GetWalkSpeed=142,
            GetCurrentAIProcedure=143,
            GetTrespassWarningLevel=144,
            IsTrespassing=145,
            IsInMyOwnedCell=146,
            GetWindSpeed=147,
            GetCurrentWeatherPercent=148,
            GetIsCurrentWeather=149,
            IsContinuingPackagePCNear=150,
            CanHaveFlames=153,
            HasFlames=154,
            GetOpenState=157,
            GetSitting=159,
            GetFurnitureMarkerID=160,
            GetIsCurrentPackage=161,
            IsCurrentFurnitureRef=162,
            IsCurrentFurnitureObj=163,
            GetDayOfWeek=170,
            GetTalkedToPCParam=172,
            IsPCSleeping=175,
            IsPCAMurderer=176,
            GetDetectionLevel=180,
            GetEquipped=182,
            IsSwimming=185,
            GetAmountSoldStolen=190,
            GetIgnoreCrime=192,
            GetPCExpelled=193,
            GetPCFactionMurder=195,
            GetPCEnemyofFaction=197,
            GetPCFactionAttack=199,
            GetDestroyed=203,
            HasMagicEffect=214,
            GetDefaultOpen=215,
            GetAnimAction=219,
            IsSpellTarget=223,
            GetVATSMode=224,
            GetPersuasionNumber=225,
            GetSandman=226,
            GetCannibal=227,
            GetIsClassDefault=228,
            GetClassDefaultMatch=229,
            GetInCellParam=230,
            GetVatsTargetHeight=235,
            GetIsGhost=237,
            GetUnconscious=242,
            GetRestrained=244,
            GetIsUsedItem=246,
            GetIsUsedItemType=247,
            GetIsPlayableRace=254,
            GetOffersServicesNow=255,
            GetUsedItemLevel=258,
            GetUsedItemActivate=259,
            GetBarterGold=264,
            IsTimePassing=265,
            IsPleasant=266,
            IsCloudy=267,
            GetArmorRatingUpperBody=274,
            GetBaseActorValue=277,
            IsOwner=278,
            IsCellOwner=280,
            IsHorseStolen=282,
            IsLeftUp=285,
            IsSneaking=286,
            IsRunning=287,
            GetFriendHit=288,
            IsInCombat=289,
            IsInInterior=300,
            IsWaterObject=304,
            IsActorUsingATorch=306,
            IsXBox=309,
            GetInWorldspace=310,
            GetPCMiscStat=312,
            IsActorEvil=313,
            IsActorAVictim=314,
            GetTotalPersuasionNumber=315,
            GetIdleDoneOnce=318,
            GetNoRumors=320,
            WhichServiceMenu=323,
            IsRidingHorse=327,
            IsInDangerousWater=332,
            GetIgnoreFriendlyHits=338,
            IsPlayersLastRiddenHorse=339,
            IsActor=353,
            IsEssential=354,
            IsPlayerMovingIntoNewSpace=358,
            GetTimeDead=361,
            GetPlayerHasLastRiddenHorse=362,
            IsChild=365,
            GetLastPlayerAction=367,
            IsPlayerActionActive=368,
            IsTalkingActivatorActor=370,
            IsInList=372,
            GetHasNote=382,
            GetHitLocation=391,
            IsPC1stPerson=392,
            GetCauseofDeath=397,
            IsLimbGone=398,
            IsWeaponInList=399,
            HasFriendDisposition=403,
            GetVATSValue=408,
            IsKiller=409,
            IsKillerObject=410,
            GetFactionCombatReaction=411,
            Exists=415,
            GetGroupMemberCount=416,
            GetGroupTargetCount=417,
            GetObjectiveCompleted=420,
            GetObjectiveDisplayed=421,
            GetIsVoiceType=427,
            GetPlantedExplosive=428,
            IsActorTalkingThroughActivator=430,
            GetHealthPercentage=431,
            GetIsObjectType=433,
            GetDialogueEmotion=435,
            GetDialogueEmotionValue=436,
            GetIsCreatureType=438,
            GetInZone=446,
            HasPerk=449,
            GetFactionRelation=450,
            IsLastIdlePlayed=451,
            GetPlayerTeammate=454,
            GetPlayerTeammateCount=455,
            GetActorCrimePlayerEnemy=459,
            GetActorFactionPlayerEnemy=460,
            IsPlayerTagSkill=462,
            IsPlayerGrabbedRef=464,
            GetDestructionStage=471,
            GetIsAlignment=474,
            GetThreatRatio=478,
            GetIsUsedItemEquipType=480,
            GetConcussed=489,
            GetMapMarkerVisible=492,
            GetPermanentActorValue=495,
            GetKillingBlowLimb=496,
            GetWeaponHealthPerc=500,
            GetRadiationLevel=503,
            GetLastHitCritical=510,
            IsCombatTarget=515,
            GetVATSRightAreaFree=518,
            GetVATSLeftAreaFree=519,
            GetVATSBackAreaFree=520,
            GetVATSFrontAreaFree=521,
            GetIsLockBroken=522,
            IsPS3=523,
            IsWin32=524,
            GetVATSRightTargetVisible=525,
            GetVATSLeftTargetVisible=526,
            GetVATSBackTargetVisible=527,
            GetVATSFrontTargetVisible=528,
            IsInCriticalStage=531,
            GetXPForNextLevel=533,
            GetQuestCompleted=546,
            IsGoreDisabled=550,
            GetSpellUsageNum=555,
            GetActorsInHigh=557,
            HasLoaded3D=558,
            GetReputation=573,
            GetReputationPct=574,
            GetReputationThreshold=575,
            IsHardcore=586,
            GetForceHitReaction=601,
            ChallengeLocked=607,
            GetCasinoWinningStage=610,
            PlayerInRegion=612,
            GetChallengeCompleted=614,
            IsAlwaysHardcore=619
        ),
        "parameter_1" / Bytes(4),
        "parameter_2" / Bytes(4),
        "run_on" / Int32ul,
        "reference" / FNV_FormID([
            'PLYR', 'ACHR', 'ACRE', 'REFR', 'PMIS', 'PGRE'
        ])
    )
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
    'SCTX': PaddedString(lambda this: this.data_size, 'utf8') * 'Script Source',
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
""" Script subrecord collection.
"""


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


FNV_Model2Collection = {
    'MOD2': CString('utf8') * 'Model Filename',
    'MO2T': Byte[:] * 'Texture File Hashes',
    'MO2S': Struct(
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
    ) * 'Alternate Textures'
}


FNV_Model3Collection = {
    'MOD3': CString('utf8') * 'Model Filename',
    'MO3T': Byte[:] * 'Texture File Hashes',
    'MO3S': Struct(
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
    'MOSD': FlagsEnum(
        Int8ul,
        head=0x01,
        torso=0x02,
        right_hand=0x04,
        left_hand=0x08
    ) * 'Facegen Model Flags'
}


FNV_Model4Collection = {
    'MOD4': CString('utf8') * 'Model Filename',
    'MO4T': Byte[:] * 'Texture File Hashes',
    'MO4S': Struct(
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
    ) * 'Alternate Textures'
}


FNV_ItemCollection = {
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
}


FNV_DefaultSubrecord = Bytes(lambda this: this.data_size)
""" The default subrecord structure.

Simply returns the data as bytes.
"""

FNV_ACHRSubrecord = Switch(
    lambda this: this.type,
    dict({
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
    default=FNV_DefaultSubrecord
) * 'Placed NPC'

FNV_ACRESubrecord = Switch(
    lambda this: this.type,
    dict({
        'EDID': CString('utf8') * 'Editor ID',
        'NAME': FNV_FormID(['CREA']) * 'Base',
        'XEZN': FNV_FormID(['ECZN']) * 'Encounter Zone',
        'XRGD': Byte[:] * 'Ragdoll Data',
        'XRGB': Byte[:] * 'Ragdoll Biped Data',
        'XPRD': Float32l * 'Idle Time',
        'XPPA': Bytes(0) * 'Patrol Script Marker',
        'INAM': FNV_FormID(['IDLE']) * 'Idle',
        'TNAM': FNV_FormID(['DIAL']) * 'Topic',
        'XLCM': Int32sl * 'Level Modifier',
        'XOWN': FNV_FormID(['FACT', 'ACHR', 'CREA', 'NPC_']) * 'Owner',
        'XRNK': Int32sl * 'Ownership Data',
        'XMRC': FNV_FormID(['REFR']) * 'Merchant Container',
        'XCNT': Int32sl * 'Count',
        'XRDS': Float32l * 'Radius',
        'XHLP': Float32l * 'Health',
        'XDCR': Struct(
            "reference" / FNV_FormID(['REFR']),
            "unknown" / Byte[:]
        ) * 'Decal',
        'XLKR': FNV_FormID([
            'REFR', 'ACRE', 'ACHR', 'PGRE', 'PMIS'
        ]) * 'Linked Reference',
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
    default=FNV_DefaultSubrecord
) * 'Placed Creature'

FNV_ACTISubrecord = Switch(
    lambda this: this.type,
    dict({
        'EDID': CString('utf8') * 'Editor ID',
        'OBND': FNV_OBNDStruct * 'Object Bounds',
        'FULL': CString('utf8') * 'Activator Name',
        'SCRI': FNV_FormID(['SCPT']) * 'Script',
        'SNAM': FNV_FormID(['SOUN']) * 'Sound - Looping',
        'VNAM': FNV_FormID(['SOUN']) * 'Sound - Activation',
        'INAM': FNV_FormID(['SOUN']) * 'Radio Template',
        'RNAM': FNV_FormID(['TACT']) * 'Radio Station',
        'WNAM': FNV_FormID(['WATR']) * 'Water Type',
        'XATO': CString('utf8') * 'Activation Prompt'
    }, **FNV_ModelCollection, **FNV_DestructionCollection),
    default=FNV_DefaultSubrecord
) * 'Activator'

FNV_ADDNSubrecord = Switch(
    lambda this: this.type,
    dict({
        'EDID': CString('utf8') * 'Editor ID',
        'OBND': FNV_OBNDStruct * 'Object Bounds',
        'DATA': Int32sl * 'Node Index',
        'DNAM': Struct(
            "master_particle_system_cap" / Int16ul,
            "unknown" / Bytes(2)
        ) * 'Data'
    }, **FNV_ModelCollection),
    default=FNV_DefaultSubrecord
) * 'Addon Note'

FNV_ALCHSubrecord = Switch(
    lambda this: this.type,
    dict({
        'EDID': CString('utf8') * 'Editor ID',
        'OBND': FNV_OBNDStruct * 'Object Bounds',
        'FULL': CString('utf8') * 'Name',
        'ICON': CString('utf8') * 'Large Icon Filename',
        'MICO': CString('utf8') * 'Small Icon Fielname',
        'SCRI': FNV_FormID(['SCPT']) * 'Script',
        'YNAM': FNV_FormID(['SOUN']) * 'Sound - Pick Up',
        'ZNAM': FNV_FormID(['SOUN']) * 'Sound - Drop',
        'ETYP': FNV_EquipmentTypeEnum * 'Equipment Type',
        'DATA': Float32l * 'Weight',
        'ENIT': Struct(
            "value" / Int32sl,
            "flags" / FlagsEnum(
                Int8ul,
                no_auto_calc=0x01,
                food_item=0x02,
                medicine=0x04
            ),
            "unused" / Bytes(3),
            "withdrawal_effect" / FNV_FormID(['SPEL']),
            "addiction_chance" / Float32l,
            "sound_consume" / FNV_FormID(['SOUN'])
        ),
    }, **FNV_EffectCollection),
    default=FNV_DefaultSubrecord
) * 'Ingestible'

FNV_ALOCSubrecord = Switch(
    lambda this: this.type,
    {
        'EDID': CString('utf8') * 'Editor ID',
        'FULL': CString('utf8') * 'Name',
        'NAM1': Byte[:] * 'Unknown 1',
        'NAM2': Byte[:] * 'Unknown 2',
        'NAM3': Byte[:] * 'Unknown 3',
        'NAM4': Float32l * 'Location Delay',
        'NAM5': Int32ul * 'Day Start',
        'NAM6': Int32ul * 'Night Start',
        'NAM7': Float32l * 'Retrigger Delay',
        'HNAM': FNV_FormID(['MSET']) * 'Neutral Media Set',
        'ZNAM': FNV_FormID(['MSET']) * 'Ally Media Set',
        'XNAM': FNV_FormID(['MSET']) * 'Friend Media Set',
        'YNAM': FNV_FormID(['MSET']) * 'Enemy Media Set',
        'LNAM': FNV_FormID(['MSET']) * 'Location Media Set',
        'GNAM': FNV_FormID(['MSET']) * 'Battle Media Set',
        'RNAM': FNV_FormID(['FACT']) * 'Conditional Faction',
        'FNAM': Byte[:] * 'Unknown 4'
    },
    default=FNV_DefaultSubrecord
) * 'Media Location Controller'

FNV_AMEFSubrecord = Switch(
    lambda this: this.type,
    {
        'EDID': CString('utf8') * 'Editor ID',
        'FULL': CString('utf8') * 'Name',
        'DATA': Struct(
            "type" / Enum(
                Int32ul,
                damage_mod=0,
                dr_mod=1,
                dt_mod=2,
                spread_mod=3,
                weapon_condition_mod=4,
                fatigue_mod=5
            ),
            "operation" / Enum(
                Int32ul,
                add=0,
                multiply=1,
                subtract=2
            ),
            "value" / Float32l
        ) * 'Data'
    },
    default=FNV_DefaultSubrecord
) * 'Ammo Effect'

FNV_AMMOSubrecord = Switch(
    lambda this: this.type,
    dict({
        'EDID': CString('utf8') * 'Editor ID',
        'OBND': FNV_OBNDStruct * 'Object Bounds',
        'FULL': CString('utf8') * 'Name',
        'ICON': CString('utf8') * 'Large Icon Filename',
        'MICO': CString('utf8') * 'Small Icon Filename',
        'SCRI': FNV_FormID(['SCPT']) * 'Script',
        'YNAM': FNV_FormID(['SOUN']) * 'Sound - Pick Up',
        'ZNAM': FNV_FormID(['SOUN']) * 'Sound - Drop',
        'DATA': Struct(
            "speed" / Float32l,
            "flags" / FlagsEnum(
                Int8ul,
                ignores_normal_weapon_resistance=0x1,
                non_playable=0x2
            ),
            "unused" / Bytes(3),
            "value" / Int32sl,
            "clip_rounds" / Int8ul
        ),
        'DAT2': Struct(
            "projectiles_per_shot" / Int32ul,
            "projectile" / FNV_FormID(['PROJ']),
            "weight" / Float32l,
            "consumed_ammo" / FNV_FormID(['AMMO', 'MISC']),
            "consumed_percentage" / Float32l
        ),
        'ONAM': CString('utf8') * 'Short Name',
        'QNAM': CString('utf8') * 'Abbreviation',
        'RCIL': FNV_FormID(['AMEF']) * 'Ammo Effect'
    }, **FNV_ModelCollection, **FNV_DestructionCollection),
    default=FNV_DefaultSubrecord
) * 'Ammunition'

FNV_ANIOSubrecrod = Switch(
    lambda this: this.type,
    dict({
        'EDID': CString('utf8') * 'Editor ID',
        'DATA': FNV_FormID(['IDLE']) * 'Animation'
    }, **FNV_ModelCollection),
    default=FNV_DefaultSubrecord
) * 'Animated Object'

FNV_ARMOSubrecord = Switch(
    lambda this: this.type,
    dict({
        'EDID': CString('utf8') * 'Editor ID',
        'OBND': FNV_OBNDStruct * 'Object Bounds',
        'FULL': CString('utf8') * 'Name',
        'SCRI': FNV_FormID(['SCPT']) * 'Script',
        'EITM': FNV_FormID(['ENCH', 'SPEL']) * 'Object Effect',
        'BMDT': FNV_BMDTStruct * 'Biped Data',
        'ICON': CString('utf8') * 'Male Inventory Icon Filename',
        'MICO': CString('utf8') * 'Male Message Icon Filename',
        'ICO2': CString('utf8') * 'Female Inventory Icon Filename',
        'MIC2': CString('utf8') * 'Female Message Icon Filename',
        'BMCT': CString('utf8') * 'Ragdoll Constraint Template',
        'REPL': FNV_FormID(['FLST']) * 'Repair List',
        'BIPL': FNV_FormID(['FLST']) * 'Biped Model List',
        'ETYP': FNV_EquipmentTypeEnum * 'Equipment Type',
        'YNAM': FNV_FormID(['SOUN']) * 'Sound - Pick Up',
        'ZNAM': FNV_FormID(['SOUN']) * 'Sound - Drop',
        'DATA': Struct(
            "value" / Int32sl,
            "max_condition" / Int32sl,
            "weight" / Float32l
        ) * 'Data',
        'DNAM': Struct(
            "ar" / Int16sl, # FIXME: value is divided by 100
            "flags" / FlagsEnum(
                Int16ul,
                modulates_voice=0x0001
            ),
            "dt" / Float32l,
            "unknown" / Bytes(4)
        ), # FIXME: missing description
        'BNAM': Enum(
            Int32ul,
            no=0,
            yes=1
        ) * 'Overrides Animation Sounds',
        'SNAM': Struct(
            "sound" / FNV_FormID(['SOUN']),
            "chance" / Int8ul,
            "unknown" / Bytes(3),
            "type" / Enum(
                Int32ul,
                run=19,
                run_in_armor=20,
                sneak=21,
                sneak_in_armor=22,
                walk=23,
                walk_in_armor=24
            )
        ) * 'Animation Sound',
        'TNAM': FNV_FormID(['ARMO']) * 'Animation Sound Template'
    }, **FNV_ModelCollection, **FNV_Model2Collection, **FNV_Model3Collection, **FNV_Model4Collection),
    default=FNV_DefaultSubrecord
) * 'Armor'

FNV_ARMASubrecord = Switch(
    lambda this: this.type,
    dict({
        'EDID': CString('utf8') * 'Editor ID',
        'OBND': FNV_OBNDStruct * 'Object Bounds',
        'FULL': CString('utf8') * 'Name',
        'BMDT': FNV_BMDTStruct * 'Biped Data',
        'ICON': CString('utf8') * 'Male Inventory Icon Filename',
        'MICO': CString('utf8') * 'Male Message Icon Filename',
        'ICO2': CString('utf8') * 'Female Inventory Icon Filename',
        'MIC2': CString('utf8') * 'Female Message Icon Filename',
        'ETYP': FNV_EquipmentTypeEnum * 'Equipment Type',
        'DATA': Struct(
            "value" / Int32sl,
            "max_condition" / Int32sl,
            "weight" / Float32l
        ) * 'Data',
        'DNAM': Struct(
            "ar" / Int16sl, # FIXME: value is divided by 100
            "flags" / FlagsEnum(
                Int16ul,
                modulates_voice=0x0001
            ),
            "dt" / Float32l,
            "unknown" / Bytes(4)
        ), # FIXME: missing description
    }, **FNV_ModelCollection, **FNV_Model2Collection, **FNV_Model3Collection, **FNV_Model4Collection),
    default=FNV_DefaultSubrecord
) * 'Armor Addon'

FNV_ASPCSubrecord = Switch(
    lambda this: this.type,
    {
        'EDID': CString('utf8') * 'Editor ID',
        'OBND': FNV_OBNDStruct * 'Object Bounds',
        'SNAM': FNV_FormID(['SOUN']) * 'Sound Loop',
        'WNAM': Int32ul * 'Walla Trigger Count',
        'RDAT': FNV_FormID(['REGN']) * 'Use Sound from Region (interior only)',
        'ANAM': Enum(
            Int32ul,
            none=0,
            default=1,
            generic=2,
            padded_cell=3,
            room=4,
            bathroom=5,
            livingroom=6,
            stone_room=7,
            auditorium=8,
            concert_hall=9,
            cave=10,
            arena=11,
            hangar=12,
            carpeted_hallway=13,
            hallway=14,
            stone_corridor=15,
            alley=16,
            forest=17,
            city=18,
            mountains=19,
            quarry=20,
            plain=21,
            parking_lot=22,
            sewer_pipe=23,
            underwater=24,
            small_room=25,
            medium_room=26,
            large_room=27,
            medium_hall=28,
            large_hall=29,
            plate=30
        ) * 'Environment Type',
        'INAM': Enum(
            Int32ul,
            no=1,
            yes=2
        ) * 'Is Interior'
    },
    default=FNV_DefaultSubrecord
) * 'Acoustic Space'

FNV_AVIFSubrecord = Switch(
    lambda this: this.type,
    {
        'EDID': CString('utf8') * 'Editor ID',
        'FULL': CString('utf8') * 'Name',
        'DESC': CString('utf8') * 'Description',
        'ICON': CString('utf8') * 'Large Icon Filename',
        'MICO': CString('utf8') * 'Small Icon Filename',
        'ANAM': CString('utf8') * 'Short Name',
    },
    default=FNV_DefaultSubrecord
) * 'Actor Value Information'

FNV_BOOKSubrecord = Switch(
    lambda this: this.type,
    dict({
        'EDID': CString('utf8') * 'Editor ID',
        'OBND': FNV_OBNDStruct * 'Object Bounds',
        'FULL': CString('utf8') * 'Name',
        'ICON': CString('utf8') * 'Large Icon Filename',
        'MICO': CString('utf8') * 'Small Icon Filename',
        'SCRI': FNV_FormID(['SCPT']) * 'Script',
        'YNAM': FNV_FormID(['SOUN']) * 'Sound - Pick Up',
        'ZNAM': FNV_FormID(['SOUN']) * 'Sound - Drop',
        'DATA': Struct(
            "flags" / FlagsEnum(
                Int8ul,
                unknown=0x01,
                cant_be_taken=0x02
            ),
            "skill" / FNV_SkillEnum,
            "value" / Int32sl,
            "weight" / Float32l
        )
    }, **FNV_ModelCollection, **FNV_DestructionCollection),
    default=FNV_DefaultSubrecord
) * 'Book'

FNV_CONTSubrecord = Switch(
    lambda this: this.type,
    dict({
        'EDID': CString('utf8') * 'Editor ID',
        'OBND': FNV_OBNDStruct * 'Object Bounds',
        'FULL': CString('utf8') * 'Name',
        'SCRI': FNV_FormID(['SCPT']) * 'Script',
        'DATA': Struct(
            "flags" / FlagsEnum(
                Int8ul,
                unknown=0x1,
                respawns=0x2
            ),
            "weight" / Float32l
        ) * 'Data',
        'SNAM': FNV_FormID(['SOUN']) * 'Sound - Open',
        'QNAM': FNV_FormID(['SOUN']) * 'Sound - Close',
        'RNAM': FNV_FormID(['SOUN']) * 'Sound - Random / Looping'
    }, **FNV_ModelCollection, **FNV_ItemCollection, **FNV_DestructionCollection),
    default=FNV_DefaultSubrecord
) * 'Container'

FNV_DOORSubrecord = Switch(
    lambda this: this.type,
    dict({
        'EDID': CString('utf8') * 'Editor ID',
        'OBND': FNV_OBNDStruct * 'Object Bounds',
        'FULL': CString('utf8') * 'Name',
        'SCRI': FNV_FormID(['SCPT']) * 'Script',
        'SNAM': FNV_FormID(['SOUN']) * 'Sound - Open',
        'ANAM': FNV_FormID(['SOUN']) * 'Sound - Closed',
        'BNAM': FNV_FormID(['SOUN']) * 'Sound - Looping',
        'FNAM': FlagsEnum(
            Int8ul,
            unknown=0x01,
            automatic_door=0x02,
            hidden=0x04,
            minimal_use=0x08,
            sliding_door=0x10
        )
    }, **FNV_ModelCollection, **FNV_DestructionCollection),
    default=FNV_DefaultSubrecord
) * 'Door'

FNV_FACTSubrecord = Switch(
    lambda this: this.type,
    {
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
    default=FNV_DefaultSubrecord
) * 'Faction'

FNV_KEYMSubrecord = Switch(
    lambda this: this.type,
        dict({
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
    default=FNV_DefaultSubrecord
) * 'Key'

FNV_MISCSubrecord = Switch(
    lambda this: this.type,
    dict({
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
        ) * 'Data',
        'RNAM': FNV_FormID(['SOUN']) * 'Sound - Random / Looping'
    }, **FNV_ModelCollection, **FNV_DestructionCollection),
    default=FNV_DefaultSubrecord
) * 'Misc. Item'

FNV_NAVISubrecord = Switch(
    lambda this: this.type,
    {
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
    default=FNV_DefaultSubrecord
) * 'Navigation Mesh Info Map'

FNV_NOTESubrecord = Switch(
    lambda this: this.type,
    dict({
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
    default=FNV_DefaultSubrecord
) * 'Note'

FNV_NPC_Subrecord = Switch(
    lambda this: this.type,
    dict({
        'EDID': CString('utf8') * 'Editor ID',
        'OBND': FNV_OBNDStruct * 'Object Bounds',
        'FULL': CString('utf8') * 'Name',
        'ACBS': Struct(
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
        ) * 'Configuration',
        'SNAM': Struct(
            "faction" / FNV_FormID(['FACT']),
            "rank" / Int8ul,
            "unused" / Bytes(3)
        ) * 'Faction',
        'INAM': FNV_FormID(['LVLI']) * 'Death Item',
        'VTCK': FNV_FormID(['VTCP']) * 'Voice',
        'TPLT': FNV_FormID(['NPC_', 'LVLN']) * 'Template',
        'RNAM': FNV_FormID(['RACE']) * 'Race',
        'SPLO': FNV_FormID(['SPEL']) * 'Actor Effect',
        'EITM': FNV_FormID(['ENCH', 'SPEL']) * 'Unarmed Attack Effect',
        'EAMT': FNV_AttackAnimationsEnum * 'Unarmed Attack Animation',
        'SCRI': FNV_FormID(['SCPT']) * 'Script',
        'AIDT': Struct(
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
        ) * 'AI Data',
        'PKID': FNV_FormID(['PACK']) * 'Package',
        'CNAM': FNV_FormID(['CLAS']) * 'Class',
        'DATA': Struct(
            "base_health" / Int32sl,
            "strength" / Int8ul,
            "perception"  / Int8ul,
            "endurance" / Int8ul,
            "charisma" / Int8ul,
            "intelligence" / Int8ul,
            "agility" / Int8ul,
            "luck" / Int8ul,
            "unused" / Optional(Int8ul[:])
        ) * 'Data',
        'DNAM': Struct(
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
        ) * 'Skills',
        'PNAM': FNV_FormID(['HDPT']) * 'Head Part',
        'HNAM': FNV_FormID(['HAIR']) * 'Hair',
        'LNAM': Float32l * 'Hair Length',
        'ENAM': FNV_FormID(['EYES']) * 'Eyes',
        'HCLR': FNV_RGBAStruct * 'Hair Color',
        'ZNAM': FNV_FormID(['CSTY']),
        'NAM4': FNV_ImpactMaterialEnum * 'Impact Material Type',
        'FGGS': Int8ul[:] * 'Facegen Geometry - Symmetric',
        'FGGA': Int8ul[:] * 'Facegen Geometry - Asymmetric',
        'FGTS': Int8ul[:] * 'Facegen Texture - Symmetric',
        'NAM5': Int16ul * 'Unknown',
        'NAM6': Float32l * 'Height',
        'NAM7': Float32l * 'Weight'
    }, **FNV_ModelCollection, **FNV_ItemCollection, **FNV_DestructionCollection),
    default=FNV_DefaultSubrecord
) * 'Non-Player Character'

FNV_SCPTSubrecord = Switch(
    lambda this: this.type,
    dict({
        'EDID': CString('utf8') * 'Editor ID',
    }, **FNV_ScriptCollection),
    default=FNV_DefaultSubrecord
) * 'Script'

FNV_STATSubrecord = Switch(
    lambda this: this.type,
    dict({
        'EDID': CString('utf8') * 'Editor ID',
        'OBND': FNV_OBNDStruct * 'Object Bounds',
        'BRUS': Enum(
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
        ) * 'Passthrough Sound',
        'RNAM': FNV_FormID(['SOUN']) * 'Sound - Random / Looping'
    }, **FNV_ModelCollection),
    default=FNV_DefaultSubrecord
) * 'Static'

FNV_TACTSubrecord = Switch(
    lambda this: this.type,
    dict({
        'EDID': CString('utf8') * 'Editor ID',
        'OBND': FNV_OBNDStruct * 'Object Bounds',
        'FULL': CString('utf8') * 'Name',
        'SCRI': FNV_FormID(['SCPT']) * 'Script',
        'SNAM': FNV_FormID(['SOUN']) * 'Looping Sound',
        'VNAM': FNV_FormID(['VTYP']) * 'Voice Type',
        'INAM': FNV_FormID(['SOUN']) * 'Radio Template'
    }, **FNV_ModelCollection, **FNV_DestructionCollection),
    default=FNV_DefaultSubrecord
) * 'Talking Activator'

FNV_VTYPSubrecord = Switch(
    lambda this: this.type,
    {
        'EDID': CString('utf8') * 'Editor ID',
        'DNAM': FlagsEnum(
            Int8ul,
            allow_default_dialog=0x01,
            female=0x02
        )
    },
    default=FNV_DefaultSubrecord
) * 'Voice Type'


FNV_SubrecordMap = {
    'ACHR': FNV_ACHRSubrecord,
    'ACRE': FNV_ACRESubrecord,
    'ACTI': FNV_ACTISubrecord,
    'ADDN': FNV_ADDNSubrecord,
    'ALCH': FNV_DefaultSubrecord,
    'ALOC': FNV_ALOCSubrecord,
    'AMEF': FNV_AMEFSubrecord,
    'AMMO': FNV_AMMOSubrecord,
    'ANIO': FNV_ANIOSubrecrod,
    'ARMO': FNV_ARMOSubrecord,
    'ARMA': FNV_ARMASubrecord,
    'ASPC': FNV_ASPCSubrecord,
    'AVIF': FNV_AVIFSubrecord,
    'BOOK': FNV_BOOKSubrecord,
    'BPTD': FNV_DefaultSubrecord,
    'CAMS': FNV_DefaultSubrecord,
    'CCRD': FNV_DefaultSubrecord,
    'CDCK': FNV_DefaultSubrecord,
    'CELL': FNV_DefaultSubrecord,
    'CHAL': FNV_DefaultSubrecord,
    'CHIP': FNV_DefaultSubrecord,
    'CLAS': FNV_DefaultSubrecord,
    'CLMT': FNV_DefaultSubrecord,
    'CMNY': FNV_DefaultSubrecord,
    'COBJ': FNV_DefaultSubrecord,
    'CONT': FNV_CONTSubrecord,
    'CPTH': FNV_DefaultSubrecord,
    'CREA': FNV_DefaultSubrecord,
    'CSNO': FNV_DefaultSubrecord,
    'CSTY': FNV_DefaultSubrecord,
    'DEBR': FNV_DefaultSubrecord,
    'DEHY': FNV_DefaultSubrecord,
    'DIAL': FNV_DefaultSubrecord,
    'DOBJ': FNV_DefaultSubrecord,
    'DOOR': FNV_DOORSubrecord,
    'ECZN': FNV_DefaultSubrecord,
    'EFSH': FNV_DefaultSubrecord,
    'ENCH': FNV_DefaultSubrecord,
    'EXPL': FNV_DefaultSubrecord,
    'EYES': FNV_DefaultSubrecord,
    'FACT': FNV_FACTSubrecord,
    'FLST': FNV_DefaultSubrecord,
    'FURN': FNV_DefaultSubrecord,
    'GLOB': FNV_DefaultSubrecord,
    'GMST': FNV_DefaultSubrecord,
    'GRAS': FNV_DefaultSubrecord,
    'HAIR': FNV_DefaultSubrecord,
    'HDPT': FNV_DefaultSubrecord,
    'HUNG': FNV_DefaultSubrecord,
    'IDLE': FNV_DefaultSubrecord,
    'IDLM': FNV_DefaultSubrecord,
    'IMGS': FNV_DefaultSubrecord,
    'IMAD': FNV_DefaultSubrecord,
    'IMOD': FNV_DefaultSubrecord,
    'INFO': FNV_DefaultSubrecord,
    'INGR': FNV_DefaultSubrecord,
    'IPCT': FNV_DefaultSubrecord,
    'IPDS': FNV_DefaultSubrecord,
    'KEYM': FNV_KEYMSubrecord,
    'LAND': FNV_DefaultSubrecord,
    'LGMT': FNV_DefaultSubrecord,
    'LIGH': FNV_DefaultSubrecord,
    'LSCR': FNV_DefaultSubrecord,
    'LSCT': FNV_DefaultSubrecord,
    'LTEX': FNV_DefaultSubrecord,
    'LVLC': FNV_DefaultSubrecord,
    'LVLI': FNV_DefaultSubrecord,
    'LVLN': FNV_DefaultSubrecord,
    'MESG': FNV_DefaultSubrecord,
    'MGEF': FNV_DefaultSubrecord,
    'MICN': FNV_DefaultSubrecord,
    'MISC': FNV_MISCSubrecord,
    'MSET': FNV_DefaultSubrecord,
    'MSTT': FNV_DefaultSubrecord,
    'MUSC': FNV_DefaultSubrecord,
    'NAVI': FNV_NAVISubrecord,
    'NAVM': FNV_DefaultSubrecord,
    'NOTE': FNV_NOTESubrecord,
    'NPC_': FNV_NPC_Subrecord,
    'PACK': FNV_DefaultSubrecord,
    'PERK': FNV_DefaultSubrecord,
    'PGRE': FNV_DefaultSubrecord,
    'PMIS': FNV_DefaultSubrecord,
    'PROJ': FNV_DefaultSubrecord,
    'PWAT': FNV_DefaultSubrecord,
    'QUST': FNV_DefaultSubrecord,
    'RACE': FNV_DefaultSubrecord,
    'RADS': FNV_DefaultSubrecord,
    'RCCT': FNV_DefaultSubrecord,
    'RCPE': FNV_DefaultSubrecord,
    'REFR': FNV_DefaultSubrecord,
    'REGN': FNV_DefaultSubrecord,
    'REPU': FNV_DefaultSubrecord,
    'RGDL': FNV_DefaultSubrecord,
    'SCOL': FNV_DefaultSubrecord,
    'SCPT': FNV_SCPTSubrecord,
    'SLPD': FNV_DefaultSubrecord,
    'SOUN': FNV_DefaultSubrecord,
    'SPEL': FNV_DefaultSubrecord,
    'STAT': FNV_STATSubrecord,
    'TACT': FNV_TACTSubrecord,
    'TERM': FNV_DefaultSubrecord,
    'TES4': FNV_DefaultSubrecord,
    'TREE': FNV_DefaultSubrecord,
    'TXST': FNV_DefaultSubrecord,
    'VTYP': FNV_VTYPSubrecord,
    'WATR': FNV_DefaultSubrecord,
    'WEAP': FNV_DefaultSubrecord,
    'WRLD': FNV_DefaultSubrecord,
    'WTHR': FNV_DefaultSubrecord,
}


FNV_Subrecord = Struct(
    "type" / PaddedString(4, 'utf8'),
    "data_size" / Int16ul,
    "data" / RawCopy(
        Switch(lambda this: this._.parent,
        FNV_SubrecordMap,
        default=Bytes(lambda this: this.data_size))
    )
)


def _parse_subrecords(record_data: bytes, record_type: str) -> List[Container]:
    while record_data and len(record_data) > 0:
        subrecord = FNV_Subrecord.parse(record_data, parent=record_type)
        record_data = record_data[(subrecord.data_size + 6):]

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
    "id" / Int32ul,
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
