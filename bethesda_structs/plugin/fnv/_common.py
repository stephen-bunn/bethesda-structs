# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# MIT License <https://choosealicense.com/licenses/mit/>

from typing import List

from construct import (
    Enum,
    Bytes,
    Int8sl,
    Int8ul,
    Struct,
    Adapter,
    CString,
    Int16sl,
    Int16ul,
    Int32sl,
    Int32ul,
    Float32l,
    Construct,
    Container,
    FlagsEnum,
    GreedyBytes,
    GreedyString,
    PaddedString,
)

from .._common import FormID, Subrecord, SubrecordCollection


class FNVFormID(Adapter):
    """ Adapts a Fallout: New Vegas field to a FormID.
    """

    def __init__(self, forms: List[str], *args: list, **kwargs: dict):
        """Initializes the form id.

        Args:
            forms (List[str]): A list of uppercase strings as potential forms.
        """

        super().__init__(Int32ul, *args, **kwargs)
        self.forms = forms

    def _decode(self, obj: Construct, context: Container, path: str) -> FormID:
        """Decodes a given `obj` to a ``FormID``.

        Args:
            obj (Construct): The construct to decode
            context (Container): The contextual container to use
            path (str): The costruct path

        Returns:
            FormID: The resulting form id
        """

        return FormID(obj, self.forms)

    def _encode(self, obj: Construct, context: Container, path: str) -> bytes:
        """Encodes a ``FormID`` back to bytes.

        Args:
            obj (Construct): The construct to encode
            context (Container): The contextual container to use
            path (str): The construct path

        Returns:
            bytes: The resulting encoded bytes
        """

        return Int32ul.build(obj.form_id)


ServiceFlags = FlagsEnum(
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


EquipmentTypeEnum = Enum(
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
    alcohol=13,
)


ImpactMaterialEnum = Enum(
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
    organic_glow=11,
)


SkillEnum = Enum(
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
    unarmed=13,
)


ModEffectEnum = Enum(
    Int32ul,
    none=0,
    increase_weapon_damage=1,
    imcrease_clip_capacity=2,
    decrease_spread=3,
    decrease_weight=4,
    regenerate_ammo_shots=5,
    regenerate_ammo_seconds=6,
    decrease_equip_time_1=7,
    increase_rate_of_fire=8,
    increase_projectile_speed=9,
    increase_max_condition=10,
    silence=11,
    split_beam=12,
    vats_bonus=13,
    increase_zoom=14,
    decrease_equip_time_2=15,
    suppressor=16,
)


SoundLevelEnum = Enum(Int32ul, loud=0, normal=1, silent=2)


ReloadAnimationEnum = Enum(
    Int8ul,
    reload_a=0,
    reload_b=1,
    reload_c=2,
    reload_d=3,
    reload_f=5,
    reload_g=6,
    reload_h=7,
    reload_i=8,
    reload_j=9,
    reload_k=10,
    reload_l=11,
    reload_m=12,
    reload_n=13,
    reload_o=14,
    reload_p=15,
    reload_q=16,
    reload_r=17,
    reload_s=18,
    reload_w=19,
    reload_x=20,
    reload_y=21,
    reload_z=22,
)


ActorValuesEnum = Enum(
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
    guns=41,
    sneak=42,
    speech=43,
    survival=44,
    unarmed=45,
    inventory_weight=46,
    paralysis=47,
    invisibility=48,
    chameleon=49,
    night_eye=50,
    turbo=51,
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
    _unknown_0=62,
    _unknown_1=63,
    _unknown_2=64,
    _unknown_3=65,
    _unknown_4=66,
    _unknown_5=67,
    _unknown_6=68,
    _unknown_7=79,
    _unknown_8=70,
    _unknown_9=71,
    ignore_crippled_limbs=72,
    dehydration=73,
    hunger=74,
    sleep_deprivation=75,
    damage=76,
)


DefaultHairColorsEnum = Enum(
    Int8ul,
    bleached=0,
    brown=1,
    chocolate=2,
    platinum=3,
    cornsilk=4,
    suede=5,
    pecan=6,
    auburn=7,
    ginger=8,
    honey=9,
    gold=10,
    rosewood=11,
    black=12,
    chestnut=13,
    steel=14,
    champagne=15,
)


AttackAnimationsEnum = Enum(
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
    any=255,
)


WeaponAnimationEnum = Enum(
    Int32ul,
    hand_to_hand=0,
    melee_1_hand=1,
    melee_2_hand=2,
    pistol_ballistic=3,
    pistol_energy=4,
    rifle_ballistic=5,
    rifle_automatic=6,
    rifle_energy=7,
    handle=8,
    launcher=9,
    grenade=10,
    land_mine=11,
    mine_drop=12,
    thrown=13,
)


FunctionIndexEnum = Enum(
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
    IsAlwaysHardcore=619,
)


RGBAStruct = Struct("red" / Int8ul, "green" / Int8ul, "blue" / Int8ul, "alpha" / Int8ul)


ObjectBoundsStruct = Struct(
    "X1" / Int16sl,
    "Y1" / Int16sl,
    "Z1" / Int16sl,
    "X2" / Int16sl,
    "Y2" / Int16sl,
    "Z2" / Int16sl,
)


# TODO: Various parameter structures for parameter_1, parameter_2
# (large and annoying)
CTDAStruct = Struct(
    "type"
    / Enum(
        Int8ul,
        use_or=0x0001,
        run_on_target=0x0002,
        use_global=0x0004,
        equal_to=0x0000,
        not_equal_to=0x2000,
        greater_than=0x4000,
        greater_than_or_equal_to=0x6000,
        less_than=0x8000,
        less_than_or_equal_to=0xa000,
    ),
    "_unknown_0" / Bytes(3),
    "comparison_value" / FNVFormID(["GLOB"]),
    "function" / FunctionIndexEnum,
    "parameter_1" / Bytes(4),
    "parameter_2" / Bytes(4),
    "run_on"
    / Enum(
        Int32ul, subject=0, target=1, reference=2, combat_target=3, linked_reference=4
    ),
    "reference" / FNVFormID(["PLYR", "ACHR", "ACRE", "REFR", "PMIS", "PGRE"]),
)


SkillBoostStruct = Struct(
    "skill"
    / Enum(
        Int8sl,
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
        guns=41,
        sneak=42,
        speech=43,
        survival=44,
        unarmed=45,
        inventory_weight=46,
        paralysis=47,
        invisibility=48,
        chameleon=49,
        night_eye=50,
        turbo=51,
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
        _unknown_0=62,
        _unknown_1=63,
        _unknown_2=64,
        _unknown_3=65,
        _unknown_4=66,
        _unknown_5=67,
        _unknown_6=68,
        _unknown_7=79,
        _unknown_8=70,
        _unknown_9=71,
        ignore_crippled_limbs=72,
        dehydration=73,
        hunger=74,
        sleep_deprivation=75,
        damage=76,
    ),
    "boost" / Int8sl,
)

DestructionCollection = SubrecordCollection(
    [
        Subrecord(
            "DEST",
            Struct(
                "health" / Int32sl,
                "count" / Int8ul,
                "flags" / FlagsEnum(Int8ul, vats_targetable=0x01),
                "_unknown_0" / Bytes(2),
            )
            * "Header"
        ),
        SubrecordCollection(
            [
                Subrecord(
                    "DSTD",
                    Struct(
                        "health_percentage" / Int8ul,
                        "index" / Int8ul,
                        "damage_stage" / Int8ul,
                        "flags"
                        / FlagsEnum(
                            Int8ul, cap_damage=0x01, disable=0x02, destroy=0x04
                        ),
                        "self_damage_per_second" / Int32sl,
                        "explosion" / FNVFormID(["EXPL"]),
                        "debris" / FNVFormID(["DEBR"]),
                        "debris_count" / Int32sl,
                    )
                    * "Stage Data"
                ),
                Subrecord(
                    "DMDL", CString("utf8") * "Stage Model Filename", optional=True
                ),
                Subrecord(
                    "DMDT",
                    GreedyBytes * "Stage Model Texture File Hashes",
                    optional=True
                ),
                Subrecord("DSTF", Bytes(0) * "Stage End Marker", optional=True),
            ],
            optional=True,
            multiple=True,
        ),
    ]
)


ModelCollection = SubrecordCollection(
    [
        Subrecord("MODL", CString("utf8") * "Model Filename"),
        Subrecord("MODB", Bytes(4) * "Unknown", optional=True),
        Subrecord("MODT", GreedyBytes * "Texture File Hashes", optional=True),
        Subrecord(
            "MODS",
            Struct(
                "count" / Int32ul,
                "alternate_texture"
                / Struct(
                    "name_length" / Int32ul,
                    "3d_name" / PaddedString(lambda this: this.name_length, "utf8"),
                    "new_texture" / FNVFormID(["TXST"]),
                    "3d_index" / Int32sl,
                ),
            )
            * "Alternate Textures",
            optional=True
        ),
        Subrecord(
            "MODD",
            FlagsEnum(Int8ul, head=0x01, torso=0x02, right_hand=0x04, left_hand=0x08)
            * "Facegen Model Flags",
            optional=True
        ),
    ]
)


Model2Collection = SubrecordCollection(
    [
        Subrecord("MOD2", CString("utf8") * "Model Filename"),
        Subrecord("MO2T", GreedyBytes * "Texture File Hashes", optional=True),
        Subrecord(
            "MO2S",
            Struct(
                "count" / Int32ul,
                "alternate_texture"
                / Struct(
                    "name_length" / Int32ul,
                    "3d_name" / PaddedString(lambda this: this.name_length, "utf8"),
                    "new_texture" / FNVFormID(["TXST"]),
                    "3d_index" / Int32sl,
                ),
            )
            * "Alternate Textures",
            optional=True
        ),
    ]
)


Model3Collection = SubrecordCollection(
    [
        Subrecord("MOD3", CString("utf8") * "Model Filename"),
        Subrecord("MO3T", GreedyBytes * "Texture File Hashes", optional=True),
        Subrecord(
            "MO3S",
            Struct(
                "count" / Int32ul,
                "alternate_texture"
                / Struct(
                    "name_length" / Int32ul,
                    "3d_name" / PaddedString(lambda this: this.name_length, "utf8"),
                    "new_texture" / FNVFormID(["TXST"]),
                    "3d_index" / Int32sl,
                ),
            )
            * "Alternate Textures",
            optional=True
        ),
        Subrecord(
            "MOSD",
            FlagsEnum(Int8ul, head=0x01, torso=0x02, right_hand=0x04, left_hand=0x08)
            * "Facegen Model Flags",
            optional=True
        ),
    ]
)


Model4Collection = SubrecordCollection(
    [
        Subrecord("MOD4", CString("utf8") * "Model Filename"),
        Subrecord("MO4T", GreedyBytes * "Texture File Hashes", optional=True),
        Subrecord(
            "MO4S",
            Struct(
                "count" / Int32ul,
                "alternate_texture"
                / Struct(
                    "name_length" / Int32ul,
                    "3d_name" / PaddedString(lambda this: this.name_length, "utf8"),
                    "new_texture" / FNVFormID(["TXST"]),
                    "3d_index" / Int32sl,
                ),
            )
            * "Alternate Textures",
            optional=True
        ),
    ]
)


EffectCollection = SubrecordCollection(
    [
        Subrecord("EFID", FNVFormID(["MGEF"]) * "Base Effect", optional=True),
        Subrecord(
            "EFIT",
            Struct(
                "magnitude" / Int32ul,
                "area" / Int32ul,
                "duration" / Int32ul,
                "type" / Enum(Int32ul, self_=0, touch=1, target=2),
                "actor_value"
                / Enum(
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
                    throwing_=44,
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
                    _unknown_0=62,
                    _unknown_1=63,
                    _unknown_2=64,
                    _unknown_3=65,
                    _unknown_4=66,
                    _unknown_5=67,
                    _unknown_6=68,
                    _unknown_7=69,
                    _unknown_8=70,
                    _unknown_9=71,
                    ignore_negative_effects=72,
                ),
            )
            * "Effect Data"
        ),
        Subrecord("CTDA", CTDAStruct * "Condition", optional=True),
    ]
)


ItemCollection = SubrecordCollection(
    [
        Subrecord(
            "CNTO",
            Struct(
                "item"
                / FNVFormID(
                    [
                        "AMRO",
                        "AMMO",
                        "MISC",
                        "WEAP",
                        "BOOK",
                        "LVLI",
                        "KEYM",
                        "ALCH",
                        "NOTE",
                        "IMOD",
                        "CMNY",
                        "CCRD",
                        "LIGH",
                        "CHIP",
                        "MSTT",
                        "STAT",
                    ]
                ),
                "count" / Int32sl,
            )
            * "Item",
            optional=True
        ),
        Subrecord(
            "COED",
            Struct(
                "owner" / FNVFormID(["NPC_", "FACT"]),
                "global_variable" / FNVFormID(["GLOB"]),  # FIXME: various types,
                "item_condition" / Float32l,
            )
            * "Extra Data",
            optional=True
        ),
    ]
)


ScriptCollection = SubrecordCollection(
    [
        Subrecord(
            "SCHR",
            Struct(
                "_unknown_0" / Bytes(4),
                "ref_count" / Int32ul,
                "compiled_size" / Int32ul,
                "variable_count" / Int32ul,
                "type" / FlagsEnum(Int16ul, object=0x000, quest=0x001, effect=0x100),
                "flags" / FlagsEnum(Int16ul, enabled=0x0001),
            )
            * "Basic Script Data"
        ),
        Subrecord("SCDA", GreedyBytes * "Commpiled Script Source"),
        Subrecord("SCTX", GreedyString("utf8") * "Script Source"),
        SubrecordCollection(
            [
                Subrecord(
                    "SLSD",
                    Struct(
                        "index" / Int32ul,
                        "_unknown_0" / Bytes(12),
                        "flags" / FlagsEnum(Int8ul, is_long_or_short=0x01),
                        "_unknown_1" / Bytes(7),
                    )
                    * "Local Variable Data"
                ),
                Subrecord("SCVR", CString("utf8") * "Local Variable Name"),
            ],
            optional=True,
            multiple=True,
        ),
        Subrecord(
            "SCRO",
            FNVFormID(
                [
                    "ACTI",
                    "DOOR",
                    "STAT",
                    "FURN",
                    "CREA",
                    "SPEL",
                    "NPC_",
                    "CONT",
                    "ARMO",
                    "AMMO",
                    "MISC",
                    "WEAP",
                    "IMAD",
                    "BOOK",
                    "KEYM",
                    "ALCH",
                    "LIGH",
                    "QUST",
                    "PLYR",
                    "PACK",
                    "LVLI",
                    "ECZN",
                    "EXPL",
                    "FLST",
                    "IDLM",
                    "PMIS",
                    "FACT",
                    "ACHR",
                    "REFR",
                    "ACRE",
                    "GLOB",
                    "DIAL",
                    "CELL",
                    "SOUN",
                    "MGEF",
                    "WTHR",
                    "CLAS",
                    "EFSH",
                    "RACE",
                    "LVLC",
                    "CSTY",
                    "WRLD",
                    "SCPT",
                    "IMGS",
                    "MESG",
                    "MSTT",
                    "MUSC",
                    "NOTE",
                    "PERK",
                    "PGRE",
                    "PROJ",
                    "LVLN",
                    "WATR",
                    "ENCH",
                    "TREE",
                    "REPU",
                    "REGN",
                    "CSNO",
                    "CHAL",
                    "IMOD",
                    "RCCT",
                    "CMNY",
                    "CDCK",
                    "CHIP",
                    "CCRD",
                    "TERM",
                    "HAIR",
                    "EYES",
                    "ADDN",
                    "NULL",
                ]
            )
            * "Reference",
            optional=True,
            multiple=True
        ),
    ]
)
