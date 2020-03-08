

class CDClientTable:
    def __init__(self):
        pass

    @classmethod
    def filter_return_results(cls, results):
        pass


class AICombatRolesTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.preferredRole = None
        self.specifiedMinRangeNOUSE = None
        self.specifiedMaxRangeNOUSE = None
        self.specificMinRange = None
        self.specificMaxRange = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = AICombatRolesTable()
            return_val.id = results[0]
            return_val.preferredRole = results[1]
            return_val.specifiedMinRangeNOUSE = results[2]
            return_val.specifiedMaxRangeNOUSE = results[3]
            return_val.specificMinRange = results[4]
            return_val.specificMaxRange = results[5]
        else:
            return_val = []
            for row in results:
                val = AICombatRolesTable()
                val.id = row[0]
                val.preferredRole = row[1]
                val.specifiedMinRangeNOUSE = row[2]
                val.specifiedMaxRangeNOUSE = row[3]
                val.specificMinRange = row[4]
                val.specificMaxRange = row[5]
                return_val.append(val)

        return return_val


class AccessoryDefaultLocTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.GroupID = None
        self.Description = None
        self.Pos_X = None
        self.Pos_Y = None
        self.Pos_Z = None
        self.Rot_X = None
        self.Rot_Y = None
        self.Rot_Z = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = AccessoryDefaultLocTable()
            return_val.GroupID = results[0]
            return_val.Description = results[1]
            return_val.Pos_X = results[2]
            return_val.Pos_Y = results[3]
            return_val.Pos_Z = results[4]
            return_val.Rot_X = results[5]
            return_val.Rot_Y = results[6]
            return_val.Rot_Z = results[7]
        else:
            return_val = []
            for row in results:
                val = AccessoryDefaultLocTable()
                val.GroupID = row[0]
                val.Description = row[1]
                val.Pos_X = row[2]
                val.Pos_Y = row[3]
                val.Pos_Z = row[4]
                val.Rot_X = row[5]
                val.Rot_Y = row[6]
                val.Rot_Z = row[7]
                return_val.append(val)

        return return_val


class ActivitiesTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.ActivityID = None
        self.locStatus = None
        self.instanceMapID = None
        self.minTeams = None
        self.maxTeams = None
        self.minTeamSize = None
        self.maxTeamSize = None
        self.waitTime = None
        self.startDelay = None
        self.requiresUniqueData = None
        self.leaderboardType = None
        self.localize = None
        self.optionalCostLOT = None
        self.optionalCostCount = None
        self.showUIRewards = None
        self.CommunityActivityFlagID = None
        self.gate_version = None
        self.noTeamLootOnDeath = None
        self.optionalPercentage = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ActivitiesTable()
            return_val.ActivityID = results[0]
            return_val.locStatus = results[1]
            return_val.instanceMapID = results[2]
            return_val.minTeams = results[3]
            return_val.maxTeams = results[4]
            return_val.minTeamSize = results[5]
            return_val.maxTeamSize = results[6]
            return_val.waitTime = results[7]
            return_val.startDelay = results[8]
            return_val.requiresUniqueData = results[9]
            return_val.leaderboardType = results[10]
            return_val.localize = results[11]
            return_val.optionalCostLOT = results[12]
            return_val.optionalCostCount = results[13]
            return_val.showUIRewards = results[14]
            return_val.CommunityActivityFlagID = results[15]
            return_val.gate_version = results[16]
            return_val.noTeamLootOnDeath = results[17]
            return_val.optionalPercentage = results[18]
        else:
            return_val = []
            for row in results:
                val = ActivitiesTable()
                val.ActivityID = row[0]
                val.locStatus = row[1]
                val.instanceMapID = row[2]
                val.minTeams = row[3]
                val.maxTeams = row[4]
                val.minTeamSize = row[5]
                val.maxTeamSize = row[6]
                val.waitTime = row[7]
                val.startDelay = row[8]
                val.requiresUniqueData = row[9]
                val.leaderboardType = row[10]
                val.localize = row[11]
                val.optionalCostLOT = row[12]
                val.optionalCostCount = row[13]
                val.showUIRewards = row[14]
                val.CommunityActivityFlagID = row[15]
                val.gate_version = row[16]
                val.noTeamLootOnDeath = row[17]
                val.optionalPercentage = row[18]
                return_val.append(val)

        return return_val


class ActivityRewardsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.objectTemplate = None
        self.ActivityRewardIndex = None
        self.activityRating = None
        self.LootMatrixIndex = None
        self.CurrencyIndex = None
        self.ChallengeRating = None
        self.description = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ActivityRewardsTable()
            return_val.objectTemplate = results[0]
            return_val.ActivityRewardIndex = results[1]
            return_val.activityRating = results[2]
            return_val.LootMatrixIndex = results[3]
            return_val.CurrencyIndex = results[4]
            return_val.ChallengeRating = results[5]
            return_val.description = results[6]
        else:
            return_val = []
            for row in results:
                val = ActivityRewardsTable()
                val.objectTemplate = row[0]
                val.ActivityRewardIndex = row[1]
                val.activityRating = row[2]
                val.LootMatrixIndex = row[3]
                val.CurrencyIndex = row[4]
                val.ChallengeRating = row[5]
                val.description = row[6]
                return_val.append(val)

        return return_val


class ActivityTextTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.activityID = None
        self.type = None
        self.localize = None
        self.locStatus = None
        self.gate_version = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ActivityTextTable()
            return_val.activityID = results[0]
            return_val.type = results[1]
            return_val.localize = results[2]
            return_val.locStatus = results[3]
            return_val.gate_version = results[4]
        else:
            return_val = []
            for row in results:
                val = ActivityTextTable()
                val.activityID = row[0]
                val.type = row[1]
                val.localize = row[2]
                val.locStatus = row[3]
                val.gate_version = row[4]
                return_val.append(val)

        return return_val


class AnimationIndexTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.animationGroupID = None
        self.description = None
        self.groupType = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = AnimationIndexTable()
            return_val.animationGroupID = results[0]
            return_val.description = results[1]
            return_val.groupType = results[2]
        else:
            return_val = []
            for row in results:
                val = AnimationIndexTable()
                val.animationGroupID = row[0]
                val.description = row[1]
                val.groupType = row[2]
                return_val.append(val)

        return return_val


class AnimationsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.animationGroupID = None
        self.animation_type = None
        self.animation_name = None
        self.chance_to_play = None
        self.min_loops = None
        self.max_loops = None
        self.animation_length = None
        self.hideEquip = None
        self.ignoreUpperBody = None
        self.restartable = None
        self.face_animation_name = None
        self.priority = None
        self.blendTime = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = AnimationsTable()
            return_val.animationGroupID = results[0]
            return_val.animation_type = results[1]
            return_val.animation_name = results[2]
            return_val.chance_to_play = results[3]
            return_val.min_loops = results[4]
            return_val.max_loops = results[5]
            return_val.animation_length = results[6]
            return_val.hideEquip = results[7]
            return_val.ignoreUpperBody = results[8]
            return_val.restartable = results[9]
            return_val.face_animation_name = results[10]
            return_val.priority = results[11]
            return_val.blendTime = results[12]
        else:
            return_val = []
            for row in results:
                val = AnimationsTable()
                val.animationGroupID = row[0]
                val.animation_type = row[1]
                val.animation_name = row[2]
                val.chance_to_play = row[3]
                val.min_loops = row[4]
                val.max_loops = row[5]
                val.animation_length = row[6]
                val.hideEquip = row[7]
                val.ignoreUpperBody = row[8]
                val.restartable = row[9]
                val.face_animation_name = row[10]
                val.priority = row[11]
                val.blendTime = row[12]
                return_val.append(val)

        return return_val


class BaseCombatAIComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.behaviorType = None
        self.combatRoundLength = None
        self.combatRole = None
        self.minRoundLength = None
        self.maxRoundLength = None
        self.tetherSpeed = None
        self.pursuitSpeed = None
        self.combatStartDelay = None
        self.softTetherRadius = None
        self.hardTetherRadius = None
        self.spawnTimer = None
        self.tetherEffectID = None
        self.ignoreMediator = None
        self.aggroRadius = None
        self.ignoreStatReset = None
        self.ignoreParent = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = BaseCombatAIComponentTable()
            return_val.id = results[0]
            return_val.behaviorType = results[1]
            return_val.combatRoundLength = results[2]
            return_val.combatRole = results[3]
            return_val.minRoundLength = results[4]
            return_val.maxRoundLength = results[5]
            return_val.tetherSpeed = results[6]
            return_val.pursuitSpeed = results[7]
            return_val.combatStartDelay = results[8]
            return_val.softTetherRadius = results[9]
            return_val.hardTetherRadius = results[10]
            return_val.spawnTimer = results[11]
            return_val.tetherEffectID = results[12]
            return_val.ignoreMediator = results[13]
            return_val.aggroRadius = results[14]
            return_val.ignoreStatReset = results[15]
            return_val.ignoreParent = results[16]
        else:
            return_val = []
            for row in results:
                val = BaseCombatAIComponentTable()
                val.id = row[0]
                val.behaviorType = row[1]
                val.combatRoundLength = row[2]
                val.combatRole = row[3]
                val.minRoundLength = row[4]
                val.maxRoundLength = row[5]
                val.tetherSpeed = row[6]
                val.pursuitSpeed = row[7]
                val.combatStartDelay = row[8]
                val.softTetherRadius = row[9]
                val.hardTetherRadius = row[10]
                val.spawnTimer = row[11]
                val.tetherEffectID = row[12]
                val.ignoreMediator = row[13]
                val.aggroRadius = row[14]
                val.ignoreStatReset = row[15]
                val.ignoreParent = row[16]
                return_val.append(val)

        return return_val


class BehaviorEffectTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.effectID = None
        self.effectType = None
        self.effectName = None
        self.trailID = None
        self.pcreateDuration = None
        self.animationName = None
        self.attachToObject = None
        self.boneName = None
        self.useSecondary = None
        self.cameraEffectType = None
        self.cameraDuration = None
        self.cameraFrequency = None
        self.cameraXAmp = None
        self.cameraYAmp = None
        self.cameraZAmp = None
        self.cameraRotFrequency = None
        self.cameraRoll = None
        self.cameraPitch = None
        self.cameraYaw = None
        self.AudioEventGUID = None
        self.renderEffectType = None
        self.renderEffectTime = None
        self.renderStartVal = None
        self.renderEndVal = None
        self.renderDelayVal = None
        self.renderValue1 = None
        self.renderValue2 = None
        self.renderValue3 = None
        self.renderRGBA = None
        self.renderShaderVal = None
        self.motionID = None
        self.meshID = None
        self.meshDuration = None
        self.meshLockedNode = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = BehaviorEffectTable()
            return_val.effectID = results[0]
            return_val.effectType = results[1]
            return_val.effectName = results[2]
            return_val.trailID = results[3]
            return_val.pcreateDuration = results[4]
            return_val.animationName = results[5]
            return_val.attachToObject = results[6]
            return_val.boneName = results[7]
            return_val.useSecondary = results[8]
            return_val.cameraEffectType = results[9]
            return_val.cameraDuration = results[10]
            return_val.cameraFrequency = results[11]
            return_val.cameraXAmp = results[12]
            return_val.cameraYAmp = results[13]
            return_val.cameraZAmp = results[14]
            return_val.cameraRotFrequency = results[15]
            return_val.cameraRoll = results[16]
            return_val.cameraPitch = results[17]
            return_val.cameraYaw = results[18]
            return_val.AudioEventGUID = results[19]
            return_val.renderEffectType = results[20]
            return_val.renderEffectTime = results[21]
            return_val.renderStartVal = results[22]
            return_val.renderEndVal = results[23]
            return_val.renderDelayVal = results[24]
            return_val.renderValue1 = results[25]
            return_val.renderValue2 = results[26]
            return_val.renderValue3 = results[27]
            return_val.renderRGBA = results[28]
            return_val.renderShaderVal = results[29]
            return_val.motionID = results[30]
            return_val.meshID = results[31]
            return_val.meshDuration = results[32]
            return_val.meshLockedNode = results[33]
        else:
            return_val = []
            for row in results:
                val = BehaviorEffectTable()
                val.effectID = row[0]
                val.effectType = row[1]
                val.effectName = row[2]
                val.trailID = row[3]
                val.pcreateDuration = row[4]
                val.animationName = row[5]
                val.attachToObject = row[6]
                val.boneName = row[7]
                val.useSecondary = row[8]
                val.cameraEffectType = row[9]
                val.cameraDuration = row[10]
                val.cameraFrequency = row[11]
                val.cameraXAmp = row[12]
                val.cameraYAmp = row[13]
                val.cameraZAmp = row[14]
                val.cameraRotFrequency = row[15]
                val.cameraRoll = row[16]
                val.cameraPitch = row[17]
                val.cameraYaw = row[18]
                val.AudioEventGUID = row[19]
                val.renderEffectType = row[20]
                val.renderEffectTime = row[21]
                val.renderStartVal = row[22]
                val.renderEndVal = row[23]
                val.renderDelayVal = row[24]
                val.renderValue1 = row[25]
                val.renderValue2 = row[26]
                val.renderValue3 = row[27]
                val.renderRGBA = row[28]
                val.renderShaderVal = row[29]
                val.motionID = row[30]
                val.meshID = row[31]
                val.meshDuration = row[32]
                val.meshLockedNode = row[33]
                return_val.append(val)

        return return_val


class BehaviorParameterTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.behaviorID = None
        self.parameterID = None
        self.value = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = BehaviorParameterTable()
            return_val.behaviorID = results[0]
            return_val.parameterID = results[1]
            return_val.value = results[2]
        else:
            return_val = []
            for row in results:
                val = BehaviorParameterTable()
                val.behaviorID = row[0]
                val.parameterID = row[1]
                val.value = row[2]
                return_val.append(val)

        return return_val


class BehaviorTemplateTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.behaviorID = None
        self.templateID = None
        self.effectID = None
        self.effectHandle = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = BehaviorTemplateTable()
            return_val.behaviorID = results[0]
            return_val.templateID = results[1]
            return_val.effectID = results[2]
            return_val.effectHandle = results[3]
        else:
            return_val = []
            for row in results:
                val = BehaviorTemplateTable()
                val.behaviorID = row[0]
                val.templateID = row[1]
                val.effectID = row[2]
                val.effectHandle = row[3]
                return_val.append(val)

        return return_val


class BehaviorTemplateNameTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.templateID = None
        self.name = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = BehaviorTemplateNameTable()
            return_val.templateID = results[0]
            return_val.name = results[1]
        else:
            return_val = []
            for row in results:
                val = BehaviorTemplateNameTable()
                val.templateID = row[0]
                val.name = row[1]
                return_val.append(val)

        return return_val


class BlueprintsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.name = None
        self.description = None
        self.accountid = None
        self.characterid = None
        self.price = None
        self.rating = None
        self.categoryid = None
        self.lxfpath = None
        self.deleted = None
        self.created = None
        self.modified = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = BlueprintsTable()
            return_val.id = results[0]
            return_val.name = results[1]
            return_val.description = results[2]
            return_val.accountid = results[3]
            return_val.characterid = results[4]
            return_val.price = results[5]
            return_val.rating = results[6]
            return_val.categoryid = results[7]
            return_val.lxfpath = results[8]
            return_val.deleted = results[9]
            return_val.created = results[10]
            return_val.modified = results[11]
        else:
            return_val = []
            for row in results:
                val = BlueprintsTable()
                val.id = row[0]
                val.name = row[1]
                val.description = row[2]
                val.accountid = row[3]
                val.characterid = row[4]
                val.price = row[5]
                val.rating = row[6]
                val.categoryid = row[7]
                val.lxfpath = row[8]
                val.deleted = row[9]
                val.created = row[10]
                val.modified = row[11]
                return_val.append(val)

        return return_val


class BrickColorsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.red = None
        self.green = None
        self.blue = None
        self.alpha = None
        self.legopaletteid = None
        self.description = None
        self.validTypes = None
        self.validCharacters = None
        self.factoryValid = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = BrickColorsTable()
            return_val.id = results[0]
            return_val.red = results[1]
            return_val.green = results[2]
            return_val.blue = results[3]
            return_val.alpha = results[4]
            return_val.legopaletteid = results[5]
            return_val.description = results[6]
            return_val.validTypes = results[7]
            return_val.validCharacters = results[8]
            return_val.factoryValid = results[9]
        else:
            return_val = []
            for row in results:
                val = BrickColorsTable()
                val.id = row[0]
                val.red = row[1]
                val.green = row[2]
                val.blue = row[3]
                val.alpha = row[4]
                val.legopaletteid = row[5]
                val.description = row[6]
                val.validTypes = row[7]
                val.validCharacters = row[8]
                val.factoryValid = row[9]
                return_val.append(val)

        return return_val


class BrickIDTableTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.NDObjectID = None
        self.LEGOBrickID = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = BrickIDTableTable()
            return_val.NDObjectID = results[0]
            return_val.LEGOBrickID = results[1]
        else:
            return_val = []
            for row in results:
                val = BrickIDTableTable()
                val.NDObjectID = row[0]
                val.LEGOBrickID = row[1]
                return_val.append(val)

        return return_val


class BuffDefinitionsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.ID = None
        self.Priority = None
        self.UIIcon = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = BuffDefinitionsTable()
            return_val.ID = results[0]
            return_val.Priority = results[1]
            return_val.UIIcon = results[2]
        else:
            return_val = []
            for row in results:
                val = BuffDefinitionsTable()
                val.ID = row[0]
                val.Priority = row[1]
                val.UIIcon = row[2]
                return_val.append(val)

        return return_val


class BuffParametersTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.BuffID = None
        self.ParameterName = None
        self.NumberValue = None
        self.StringValue = None
        self.EffectID = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = BuffParametersTable()
            return_val.BuffID = results[0]
            return_val.ParameterName = results[1]
            return_val.NumberValue = results[2]
            return_val.StringValue = results[3]
            return_val.EffectID = results[4]
        else:
            return_val = []
            for row in results:
                val = BuffParametersTable()
                val.BuffID = row[0]
                val.ParameterName = row[1]
                val.NumberValue = row[2]
                val.StringValue = row[3]
                val.EffectID = row[4]
                return_val.append(val)

        return return_val


class CameraTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.camera_name = None
        self.pitch_angle_tolerance = None
        self.starting_zoom = None
        self.zoom_return_modifier = None
        self.pitch_return_modifier = None
        self.tether_out_return_modifier = None
        self.tether_in_return_multiplier = None
        self.verticle_movement_dampening_modifier = None
        self.return_from_incline_modifier = None
        self.horizontal_return_modifier = None
        self.yaw_behavior_speed_multiplier = None
        self.camera_collision_padding = None
        self.glide_speed = None
        self.fade_player_min_range = None
        self.min_movement_delta_tolerance = None
        self.min_glide_distance_tolerance = None
        self.look_forward_offset = None
        self.look_up_offset = None
        self.minimum_vertical_dampening_distance = None
        self.maximum_vertical_dampening_distance = None
        self.minimum_ignore_jump_distance = None
        self.maximum_ignore_jump_distance = None
        self.maximum_auto_glide_angle = None
        self.minimum_tether_glide_distance = None
        self.yaw_sign_correction = None
        self.set_1_look_forward_offset = None
        self.set_1_look_up_offset = None
        self.set_2_look_forward_offset = None
        self.set_2_look_up_offset = None
        self.set_0_speed_influence_on_dir = None
        self.set_1_speed_influence_on_dir = None
        self.set_2_speed_influence_on_dir = None
        self.set_0_angular_relaxation = None
        self.set_1_angular_relaxation = None
        self.set_2_angular_relaxation = None
        self.set_0_position_up_offset = None
        self.set_1_position_up_offset = None
        self.set_2_position_up_offset = None
        self.set_0_position_forward_offset = None
        self.set_1_position_forward_offset = None
        self.set_2_position_forward_offset = None
        self.set_0_FOV = None
        self.set_1_FOV = None
        self.set_2_FOV = None
        self.set_0_max_yaw_angle = None
        self.set_1_max_yaw_angle = None
        self.set_2_max_yaw_angle = None
        self.set_1_fade_in_camera_set_change = None
        self.set_1_fade_out_camera_set_change = None
        self.set_2_fade_in_camera_set_change = None
        self.set_2_fade_out_camera_set_change = None
        self.input_movement_scalar = None
        self.input_rotation_scalar = None
        self.input_zoom_scalar = None
        self.minimum_pitch_desired = None
        self.maximum_pitch_desired = None
        self.minimum_zoom = None
        self.maximum_zoom = None
        self.horizontal_rotate_tolerance = None
        self.horizontal_rotate_modifier = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = CameraTable()
            return_val.camera_name = results[0]
            return_val.pitch_angle_tolerance = results[1]
            return_val.starting_zoom = results[2]
            return_val.zoom_return_modifier = results[3]
            return_val.pitch_return_modifier = results[4]
            return_val.tether_out_return_modifier = results[5]
            return_val.tether_in_return_multiplier = results[6]
            return_val.verticle_movement_dampening_modifier = results[7]
            return_val.return_from_incline_modifier = results[8]
            return_val.horizontal_return_modifier = results[9]
            return_val.yaw_behavior_speed_multiplier = results[10]
            return_val.camera_collision_padding = results[11]
            return_val.glide_speed = results[12]
            return_val.fade_player_min_range = results[13]
            return_val.min_movement_delta_tolerance = results[14]
            return_val.min_glide_distance_tolerance = results[15]
            return_val.look_forward_offset = results[16]
            return_val.look_up_offset = results[17]
            return_val.minimum_vertical_dampening_distance = results[18]
            return_val.maximum_vertical_dampening_distance = results[19]
            return_val.minimum_ignore_jump_distance = results[20]
            return_val.maximum_ignore_jump_distance = results[21]
            return_val.maximum_auto_glide_angle = results[22]
            return_val.minimum_tether_glide_distance = results[23]
            return_val.yaw_sign_correction = results[24]
            return_val.set_1_look_forward_offset = results[25]
            return_val.set_1_look_up_offset = results[26]
            return_val.set_2_look_forward_offset = results[27]
            return_val.set_2_look_up_offset = results[28]
            return_val.set_0_speed_influence_on_dir = results[29]
            return_val.set_1_speed_influence_on_dir = results[30]
            return_val.set_2_speed_influence_on_dir = results[31]
            return_val.set_0_angular_relaxation = results[32]
            return_val.set_1_angular_relaxation = results[33]
            return_val.set_2_angular_relaxation = results[34]
            return_val.set_0_position_up_offset = results[35]
            return_val.set_1_position_up_offset = results[36]
            return_val.set_2_position_up_offset = results[37]
            return_val.set_0_position_forward_offset = results[38]
            return_val.set_1_position_forward_offset = results[39]
            return_val.set_2_position_forward_offset = results[40]
            return_val.set_0_FOV = results[41]
            return_val.set_1_FOV = results[42]
            return_val.set_2_FOV = results[43]
            return_val.set_0_max_yaw_angle = results[44]
            return_val.set_1_max_yaw_angle = results[45]
            return_val.set_2_max_yaw_angle = results[46]
            return_val.set_1_fade_in_camera_set_change = results[47]
            return_val.set_1_fade_out_camera_set_change = results[48]
            return_val.set_2_fade_in_camera_set_change = results[49]
            return_val.set_2_fade_out_camera_set_change = results[50]
            return_val.input_movement_scalar = results[51]
            return_val.input_rotation_scalar = results[52]
            return_val.input_zoom_scalar = results[53]
            return_val.minimum_pitch_desired = results[54]
            return_val.maximum_pitch_desired = results[55]
            return_val.minimum_zoom = results[56]
            return_val.maximum_zoom = results[57]
            return_val.horizontal_rotate_tolerance = results[58]
            return_val.horizontal_rotate_modifier = results[59]
        else:
            return_val = []
            for row in results:
                val = CameraTable()
                val.camera_name = row[0]
                val.pitch_angle_tolerance = row[1]
                val.starting_zoom = row[2]
                val.zoom_return_modifier = row[3]
                val.pitch_return_modifier = row[4]
                val.tether_out_return_modifier = row[5]
                val.tether_in_return_multiplier = row[6]
                val.verticle_movement_dampening_modifier = row[7]
                val.return_from_incline_modifier = row[8]
                val.horizontal_return_modifier = row[9]
                val.yaw_behavior_speed_multiplier = row[10]
                val.camera_collision_padding = row[11]
                val.glide_speed = row[12]
                val.fade_player_min_range = row[13]
                val.min_movement_delta_tolerance = row[14]
                val.min_glide_distance_tolerance = row[15]
                val.look_forward_offset = row[16]
                val.look_up_offset = row[17]
                val.minimum_vertical_dampening_distance = row[18]
                val.maximum_vertical_dampening_distance = row[19]
                val.minimum_ignore_jump_distance = row[20]
                val.maximum_ignore_jump_distance = row[21]
                val.maximum_auto_glide_angle = row[22]
                val.minimum_tether_glide_distance = row[23]
                val.yaw_sign_correction = row[24]
                val.set_1_look_forward_offset = row[25]
                val.set_1_look_up_offset = row[26]
                val.set_2_look_forward_offset = row[27]
                val.set_2_look_up_offset = row[28]
                val.set_0_speed_influence_on_dir = row[29]
                val.set_1_speed_influence_on_dir = row[30]
                val.set_2_speed_influence_on_dir = row[31]
                val.set_0_angular_relaxation = row[32]
                val.set_1_angular_relaxation = row[33]
                val.set_2_angular_relaxation = row[34]
                val.set_0_position_up_offset = row[35]
                val.set_1_position_up_offset = row[36]
                val.set_2_position_up_offset = row[37]
                val.set_0_position_forward_offset = row[38]
                val.set_1_position_forward_offset = row[39]
                val.set_2_position_forward_offset = row[40]
                val.set_0_FOV = row[41]
                val.set_1_FOV = row[42]
                val.set_2_FOV = row[43]
                val.set_0_max_yaw_angle = row[44]
                val.set_1_max_yaw_angle = row[45]
                val.set_2_max_yaw_angle = row[46]
                val.set_1_fade_in_camera_set_change = row[47]
                val.set_1_fade_out_camera_set_change = row[48]
                val.set_2_fade_in_camera_set_change = row[49]
                val.set_2_fade_out_camera_set_change = row[50]
                val.input_movement_scalar = row[51]
                val.input_rotation_scalar = row[52]
                val.input_zoom_scalar = row[53]
                val.minimum_pitch_desired = row[54]
                val.maximum_pitch_desired = row[55]
                val.minimum_zoom = row[56]
                val.maximum_zoom = row[57]
                val.horizontal_rotate_tolerance = row[58]
                val.horizontal_rotate_modifier = row[59]
                return_val.append(val)

        return return_val


class CelebrationParametersTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.animation = None
        self.backgroundObject = None
        self.duration = None
        self.subText = None
        self.mainText = None
        self.iconID = None
        self.celeLeadIn = None
        self.celeLeadOut = None
        self.cameraPathLOT = None
        self.pathNodeName = None
        self.ambientR = None
        self.ambientG = None
        self.ambientB = None
        self.directionalR = None
        self.directionalG = None
        self.directionalB = None
        self.specularR = None
        self.specularG = None
        self.specularB = None
        self.lightPositionX = None
        self.lightPositionY = None
        self.lightPositionZ = None
        self.blendTime = None
        self.fogColorR = None
        self.fogColorG = None
        self.fogColorB = None
        self.musicCue = None
        self.soundGUID = None
        self.mixerProgram = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = CelebrationParametersTable()
            return_val.id = results[0]
            return_val.animation = results[1]
            return_val.backgroundObject = results[2]
            return_val.duration = results[3]
            return_val.subText = results[4]
            return_val.mainText = results[5]
            return_val.iconID = results[6]
            return_val.celeLeadIn = results[7]
            return_val.celeLeadOut = results[8]
            return_val.cameraPathLOT = results[9]
            return_val.pathNodeName = results[10]
            return_val.ambientR = results[11]
            return_val.ambientG = results[12]
            return_val.ambientB = results[13]
            return_val.directionalR = results[14]
            return_val.directionalG = results[15]
            return_val.directionalB = results[16]
            return_val.specularR = results[17]
            return_val.specularG = results[18]
            return_val.specularB = results[19]
            return_val.lightPositionX = results[20]
            return_val.lightPositionY = results[21]
            return_val.lightPositionZ = results[22]
            return_val.blendTime = results[23]
            return_val.fogColorR = results[24]
            return_val.fogColorG = results[25]
            return_val.fogColorB = results[26]
            return_val.musicCue = results[27]
            return_val.soundGUID = results[28]
            return_val.mixerProgram = results[29]
        else:
            return_val = []
            for row in results:
                val = CelebrationParametersTable()
                val.id = row[0]
                val.animation = row[1]
                val.backgroundObject = row[2]
                val.duration = row[3]
                val.subText = row[4]
                val.mainText = row[5]
                val.iconID = row[6]
                val.celeLeadIn = row[7]
                val.celeLeadOut = row[8]
                val.cameraPathLOT = row[9]
                val.pathNodeName = row[10]
                val.ambientR = row[11]
                val.ambientG = row[12]
                val.ambientB = row[13]
                val.directionalR = row[14]
                val.directionalG = row[15]
                val.directionalB = row[16]
                val.specularR = row[17]
                val.specularG = row[18]
                val.specularB = row[19]
                val.lightPositionX = row[20]
                val.lightPositionY = row[21]
                val.lightPositionZ = row[22]
                val.blendTime = row[23]
                val.fogColorR = row[24]
                val.fogColorG = row[25]
                val.fogColorB = row[26]
                val.musicCue = row[27]
                val.soundGUID = row[28]
                val.mixerProgram = row[29]
                return_val.append(val)

        return return_val


class ChoiceBuildComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.selections = None
        self.imaginationOverride = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ChoiceBuildComponentTable()
            return_val.id = results[0]
            return_val.selections = results[1]
            return_val.imaginationOverride = results[2]
        else:
            return_val = []
            for row in results:
                val = ChoiceBuildComponentTable()
                val.id = row[0]
                val.selections = row[1]
                val.imaginationOverride = row[2]
                return_val.append(val)

        return return_val


class CollectibleComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.requirement_mission = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = CollectibleComponentTable()
            return_val.id = results[0]
            return_val.requirement_mission = results[1]
        else:
            return_val = []
            for row in results:
                val = CollectibleComponentTable()
                val.id = row[0]
                val.requirement_mission = row[1]
                return_val.append(val)

        return return_val


class ComponentsRegistryTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.component_type = None
        self.component_id = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ComponentsRegistryTable()
            return_val.id = results[0]
            return_val.component_type = results[1]
            return_val.component_id = results[2]
        else:
            return_val = []
            for row in results:
                val = ComponentsRegistryTable()
                val.id = row[0]
                val.component_type = row[1]
                val.component_id = row[2]
                return_val.append(val)

        return return_val


class ControlSchemesTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.control_scheme = None
        self.scheme_name = None
        self.rotation_speed = None
        self.walk_forward_speed = None
        self.walk_backward_speed = None
        self.walk_strafe_speed = None
        self.walk_strafe_forward_speed = None
        self.walk_strafe_backward_speed = None
        self.run_backward_speed = None
        self.run_strafe_speed = None
        self.run_strafe_forward_speed = None
        self.run_strafe_backward_speed = None
        self.keyboard_zoom_sensitivity = None
        self.keyboard_pitch_sensitivity = None
        self.keyboard_yaw_sensitivity = None
        self.mouse_zoom_wheel_sensitivity = None
        self.x_mouse_move_sensitivity_modifier = None
        self.y_mouse_move_sensitivity_modifier = None
        self.freecam_speed_modifier = None
        self.freecam_slow_speed_multiplier = None
        self.freecam_fast_speed_multiplier = None
        self.freecam_mouse_modifier = None
        self.gamepad_pitch_rot_sensitivity = None
        self.gamepad_yaw_rot_sensitivity = None
        self.gamepad_trigger_sensitivity = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ControlSchemesTable()
            return_val.control_scheme = results[0]
            return_val.scheme_name = results[1]
            return_val.rotation_speed = results[2]
            return_val.walk_forward_speed = results[3]
            return_val.walk_backward_speed = results[4]
            return_val.walk_strafe_speed = results[5]
            return_val.walk_strafe_forward_speed = results[6]
            return_val.walk_strafe_backward_speed = results[7]
            return_val.run_backward_speed = results[8]
            return_val.run_strafe_speed = results[9]
            return_val.run_strafe_forward_speed = results[10]
            return_val.run_strafe_backward_speed = results[11]
            return_val.keyboard_zoom_sensitivity = results[12]
            return_val.keyboard_pitch_sensitivity = results[13]
            return_val.keyboard_yaw_sensitivity = results[14]
            return_val.mouse_zoom_wheel_sensitivity = results[15]
            return_val.x_mouse_move_sensitivity_modifier = results[16]
            return_val.y_mouse_move_sensitivity_modifier = results[17]
            return_val.freecam_speed_modifier = results[18]
            return_val.freecam_slow_speed_multiplier = results[19]
            return_val.freecam_fast_speed_multiplier = results[20]
            return_val.freecam_mouse_modifier = results[21]
            return_val.gamepad_pitch_rot_sensitivity = results[22]
            return_val.gamepad_yaw_rot_sensitivity = results[23]
            return_val.gamepad_trigger_sensitivity = results[24]
        else:
            return_val = []
            for row in results:
                val = ControlSchemesTable()
                val.control_scheme = row[0]
                val.scheme_name = row[1]
                val.rotation_speed = row[2]
                val.walk_forward_speed = row[3]
                val.walk_backward_speed = row[4]
                val.walk_strafe_speed = row[5]
                val.walk_strafe_forward_speed = row[6]
                val.walk_strafe_backward_speed = row[7]
                val.run_backward_speed = row[8]
                val.run_strafe_speed = row[9]
                val.run_strafe_forward_speed = row[10]
                val.run_strafe_backward_speed = row[11]
                val.keyboard_zoom_sensitivity = row[12]
                val.keyboard_pitch_sensitivity = row[13]
                val.keyboard_yaw_sensitivity = row[14]
                val.mouse_zoom_wheel_sensitivity = row[15]
                val.x_mouse_move_sensitivity_modifier = row[16]
                val.y_mouse_move_sensitivity_modifier = row[17]
                val.freecam_speed_modifier = row[18]
                val.freecam_slow_speed_multiplier = row[19]
                val.freecam_fast_speed_multiplier = row[20]
                val.freecam_mouse_modifier = row[21]
                val.gamepad_pitch_rot_sensitivity = row[22]
                val.gamepad_yaw_rot_sensitivity = row[23]
                val.gamepad_trigger_sensitivity = row[24]
                return_val.append(val)

        return return_val


class CurrencyDenominationsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.value = None
        self.objectid = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = CurrencyDenominationsTable()
            return_val.value = results[0]
            return_val.objectid = results[1]
        else:
            return_val = []
            for row in results:
                val = CurrencyDenominationsTable()
                val.value = row[0]
                val.objectid = row[1]
                return_val.append(val)

        return return_val


class CurrencyTableTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.currencyIndex = None
        self.npcminlevel = None
        self.minvalue = None
        self.maxvalue = None
        self.id = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = CurrencyTableTable()
            return_val.currencyIndex = results[0]
            return_val.npcminlevel = results[1]
            return_val.minvalue = results[2]
            return_val.maxvalue = results[3]
            return_val.id = results[4]
        else:
            return_val = []
            for row in results:
                val = CurrencyTableTable()
                val.currencyIndex = row[0]
                val.npcminlevel = row[1]
                val.minvalue = row[2]
                val.maxvalue = row[3]
                val.id = row[4]
                return_val.append(val)

        return return_val


class DBExcludeTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.table = None
        self.column = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = DBExcludeTable()
            return_val.table = results[0]
            return_val.column = results[1]
        else:
            return_val = []
            for row in results:
                val = DBExcludeTable()
                val.table = row[0]
                val.column = row[1]
                return_val.append(val)

        return return_val


class DeletionRestrictionsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.restricted = None
        self.ids = None
        self.checkType = None
        self.localize = None
        self.locStatus = None
        self.gate_version = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = DeletionRestrictionsTable()
            return_val.id = results[0]
            return_val.restricted = results[1]
            return_val.ids = results[2]
            return_val.checkType = results[3]
            return_val.localize = results[4]
            return_val.locStatus = results[5]
            return_val.gate_version = results[6]
        else:
            return_val = []
            for row in results:
                val = DeletionRestrictionsTable()
                val.id = row[0]
                val.restricted = row[1]
                val.ids = row[2]
                val.checkType = row[3]
                val.localize = row[4]
                val.locStatus = row[5]
                val.gate_version = row[6]
                return_val.append(val)

        return return_val


class DestructibleComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.faction = None
        self.factionList = None
        self.life = None
        self.imagination = None
        self.LootMatrixIndex = None
        self.CurrencyIndex = None
        self.level = None
        self.armor = None
        self.death_behavior = None
        self.isnpc = None
        self.attack_priority = None
        self.isSmashable = None
        self.difficultyLevel = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = DestructibleComponentTable()
            return_val.id = results[0]
            return_val.faction = results[1]
            return_val.factionList = results[2]
            return_val.life = results[3]
            return_val.imagination = results[4]
            return_val.LootMatrixIndex = results[5]
            return_val.CurrencyIndex = results[6]
            return_val.level = results[7]
            return_val.armor = results[8]
            return_val.death_behavior = results[9]
            return_val.isnpc = results[10]
            return_val.attack_priority = results[11]
            return_val.isSmashable = results[12]
            return_val.difficultyLevel = results[13]
        else:
            return_val = []
            for row in results:
                val = DestructibleComponentTable()
                val.id = row[0]
                val.faction = row[1]
                val.factionList = row[2]
                val.life = row[3]
                val.imagination = row[4]
                val.LootMatrixIndex = row[5]
                val.CurrencyIndex = row[6]
                val.level = row[7]
                val.armor = row[8]
                val.death_behavior = row[9]
                val.isnpc = row[10]
                val.attack_priority = row[11]
                val.isSmashable = row[12]
                val.difficultyLevel = row[13]
                return_val.append(val)

        return return_val


class DevModelBehaviorsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.ModelID = None
        self.BehaviorID = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = DevModelBehaviorsTable()
            return_val.ModelID = results[0]
            return_val.BehaviorID = results[1]
        else:
            return_val = []
            for row in results:
                val = DevModelBehaviorsTable()
                val.ModelID = row[0]
                val.BehaviorID = row[1]
                return_val.append(val)

        return return_val


class EmotesTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.animationName = None
        self.iconFilename = None
        self.channel = None
        self.command = None
        self.locked = None
        self.localize = None
        self.locStatus = None
        self.gate_version = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = EmotesTable()
            return_val.id = results[0]
            return_val.animationName = results[1]
            return_val.iconFilename = results[2]
            return_val.channel = results[3]
            return_val.command = results[4]
            return_val.locked = results[5]
            return_val.localize = results[6]
            return_val.locStatus = results[7]
            return_val.gate_version = results[8]
        else:
            return_val = []
            for row in results:
                val = EmotesTable()
                val.id = row[0]
                val.animationName = row[1]
                val.iconFilename = row[2]
                val.channel = row[3]
                val.command = row[4]
                val.locked = row[5]
                val.localize = row[6]
                val.locStatus = row[7]
                val.gate_version = row[8]
                return_val.append(val)

        return return_val


class EventGatingTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.eventName = None
        self.date_start = None
        self.date_end = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = EventGatingTable()
            return_val.eventName = results[0]
            return_val.date_start = results[1]
            return_val.date_end = results[2]
        else:
            return_val = []
            for row in results:
                val = EventGatingTable()
                val.eventName = row[0]
                val.date_start = row[1]
                val.date_end = row[2]
                return_val.append(val)

        return return_val


class ExhibitComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.length = None
        self.width = None
        self.height = None
        self.offsetX = None
        self.offsetY = None
        self.offsetZ = None
        self.fReputationSizeMultiplier = None
        self.fImaginationCost = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ExhibitComponentTable()
            return_val.id = results[0]
            return_val.length = results[1]
            return_val.width = results[2]
            return_val.height = results[3]
            return_val.offsetX = results[4]
            return_val.offsetY = results[5]
            return_val.offsetZ = results[6]
            return_val.fReputationSizeMultiplier = results[7]
            return_val.fImaginationCost = results[8]
        else:
            return_val = []
            for row in results:
                val = ExhibitComponentTable()
                val.id = row[0]
                val.length = row[1]
                val.width = row[2]
                val.height = row[3]
                val.offsetX = row[4]
                val.offsetY = row[5]
                val.offsetZ = row[6]
                val.fReputationSizeMultiplier = row[7]
                val.fImaginationCost = row[8]
                return_val.append(val)

        return return_val


class FactionsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.faction = None
        self.factionList = None
        self.factionListFriendly = None
        self.friendList = None
        self.enemyList = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = FactionsTable()
            return_val.faction = results[0]
            return_val.factionList = results[1]
            return_val.factionListFriendly = results[2]
            return_val.friendList = results[3]
            return_val.enemyList = results[4]
        else:
            return_val = []
            for row in results:
                val = FactionsTable()
                val.faction = row[0]
                val.factionList = row[1]
                val.factionListFriendly = row[2]
                val.friendList = row[3]
                val.enemyList = row[4]
                return_val.append(val)

        return return_val


class FeatureGatingTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.featureName = None
        self.major = None
        self.current = None
        self.minor = None
        self.description = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = FeatureGatingTable()
            return_val.featureName = results[0]
            return_val.major = results[1]
            return_val.current = results[2]
            return_val.minor = results[3]
            return_val.description = results[4]
        else:
            return_val = []
            for row in results:
                val = FeatureGatingTable()
                val.featureName = row[0]
                val.major = row[1]
                val.current = row[2]
                val.minor = row[3]
                val.description = row[4]
                return_val.append(val)

        return return_val


class FlairTableTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.asset = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = FlairTableTable()
            return_val.id = results[0]
            return_val.asset = results[1]
        else:
            return_val = []
            for row in results:
                val = FlairTableTable()
                val.id = row[0]
                val.asset = row[1]
                return_val.append(val)

        return return_val


class IconsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.IconID = None
        self.IconPath = None
        self.IconName = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = IconsTable()
            return_val.IconID = results[0]
            return_val.IconPath = results[1]
            return_val.IconName = results[2]
        else:
            return_val = []
            for row in results:
                val = IconsTable()
                val.IconID = row[0]
                val.IconPath = row[1]
                val.IconName = row[2]
                return_val.append(val)

        return return_val


class InventoryComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.itemid = None
        self.count = None
        self.equip = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = InventoryComponentTable()
            return_val.id = results[0]
            return_val.itemid = results[1]
            return_val.count = results[2]
            return_val.equip = results[3]
        else:
            return_val = []
            for row in results:
                val = InventoryComponentTable()
                val.id = row[0]
                val.itemid = row[1]
                val.count = row[2]
                val.equip = row[3]
                return_val.append(val)

        return return_val


class ItemComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.equipLocation = None
        self.baseValue = None
        self.isKitPiece = None
        self.rarity = None
        self.itemType = None
        self.itemInfo = None
        self.inLootTable = None
        self.inVendor = None
        self.isUnique = None
        self.isBOP = None
        self.isBOE = None
        self.reqFlagID = None
        self.reqSpecialtyID = None
        self.reqSpecRank = None
        self.reqAchievementID = None
        self.stackSize = None
        self.color1 = None
        self.decal = None
        self.offsetGroupID = None
        self.buildTypes = None
        self.reqPrecondition = None
        self.animationFlag = None
        self.equipEffects = None
        self.readyForQA = None
        self.itemRating = None
        self.isTwoHanded = None
        self.minNumRequired = None
        self.delResIndex = None
        self.currencyLOT = None
        self.altCurrencyCost = None
        self.subItems = None
        self.audioEventUse = None
        self.noEquipAnimation = None
        self.commendationLOT = None
        self.commendationCost = None
        self.audioEquipMetaEventSet = None
        self.currencyCosts = None
        self.ingredientInfo = None
        self.locStatus = None
        self.forgeType = None
        self.SellMultiplier = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ItemComponentTable()
            return_val.id = results[0]
            return_val.equipLocation = results[1]
            return_val.baseValue = results[2]
            return_val.isKitPiece = results[3]
            return_val.rarity = results[4]
            return_val.itemType = results[5]
            return_val.itemInfo = results[6]
            return_val.inLootTable = results[7]
            return_val.inVendor = results[8]
            return_val.isUnique = results[9]
            return_val.isBOP = results[10]
            return_val.isBOE = results[11]
            return_val.reqFlagID = results[12]
            return_val.reqSpecialtyID = results[13]
            return_val.reqSpecRank = results[14]
            return_val.reqAchievementID = results[15]
            return_val.stackSize = results[16]
            return_val.color1 = results[17]
            return_val.decal = results[18]
            return_val.offsetGroupID = results[19]
            return_val.buildTypes = results[20]
            return_val.reqPrecondition = results[21]
            return_val.animationFlag = results[22]
            return_val.equipEffects = results[23]
            return_val.readyForQA = results[24]
            return_val.itemRating = results[25]
            return_val.isTwoHanded = results[26]
            return_val.minNumRequired = results[27]
            return_val.delResIndex = results[28]
            return_val.currencyLOT = results[29]
            return_val.altCurrencyCost = results[30]
            return_val.subItems = results[31]
            return_val.audioEventUse = results[32]
            return_val.noEquipAnimation = results[33]
            return_val.commendationLOT = results[34]
            return_val.commendationCost = results[35]
            return_val.audioEquipMetaEventSet = results[36]
            return_val.currencyCosts = results[37]
            return_val.ingredientInfo = results[38]
            return_val.locStatus = results[39]
            return_val.forgeType = results[40]
            return_val.SellMultiplier = results[41]
        else:
            return_val = []
            for row in results:
                val = ItemComponentTable()
                val.id = row[0]
                val.equipLocation = row[1]
                val.baseValue = row[2]
                val.isKitPiece = row[3]
                val.rarity = row[4]
                val.itemType = row[5]
                val.itemInfo = row[6]
                val.inLootTable = row[7]
                val.inVendor = row[8]
                val.isUnique = row[9]
                val.isBOP = row[10]
                val.isBOE = row[11]
                val.reqFlagID = row[12]
                val.reqSpecialtyID = row[13]
                val.reqSpecRank = row[14]
                val.reqAchievementID = row[15]
                val.stackSize = row[16]
                val.color1 = row[17]
                val.decal = row[18]
                val.offsetGroupID = row[19]
                val.buildTypes = row[20]
                val.reqPrecondition = row[21]
                val.animationFlag = row[22]
                val.equipEffects = row[23]
                val.readyForQA = row[24]
                val.itemRating = row[25]
                val.isTwoHanded = row[26]
                val.minNumRequired = row[27]
                val.delResIndex = row[28]
                val.currencyLOT = row[29]
                val.altCurrencyCost = row[30]
                val.subItems = row[31]
                val.audioEventUse = row[32]
                val.noEquipAnimation = row[33]
                val.commendationLOT = row[34]
                val.commendationCost = row[35]
                val.audioEquipMetaEventSet = row[36]
                val.currencyCosts = row[37]
                val.ingredientInfo = row[38]
                val.locStatus = row[39]
                val.forgeType = row[40]
                val.SellMultiplier = row[41]
                return_val.append(val)

        return return_val


class ItemEggDataTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.chassie_type_id = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ItemEggDataTable()
            return_val.id = results[0]
            return_val.chassie_type_id = results[1]
        else:
            return_val = []
            for row in results:
                val = ItemEggDataTable()
                val.id = row[0]
                val.chassie_type_id = row[1]
                return_val.append(val)

        return return_val


class ItemFoodDataTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.element_1 = None
        self.element_1_amount = None
        self.element_2 = None
        self.element_2_amount = None
        self.element_3 = None
        self.element_3_amount = None
        self.element_4 = None
        self.element_4_amount = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ItemFoodDataTable()
            return_val.id = results[0]
            return_val.element_1 = results[1]
            return_val.element_1_amount = results[2]
            return_val.element_2 = results[3]
            return_val.element_2_amount = results[4]
            return_val.element_3 = results[5]
            return_val.element_3_amount = results[6]
            return_val.element_4 = results[7]
            return_val.element_4_amount = results[8]
        else:
            return_val = []
            for row in results:
                val = ItemFoodDataTable()
                val.id = row[0]
                val.element_1 = row[1]
                val.element_1_amount = row[2]
                val.element_2 = row[3]
                val.element_2_amount = row[4]
                val.element_3 = row[5]
                val.element_3_amount = row[6]
                val.element_4 = row[7]
                val.element_4_amount = row[8]
                return_val.append(val)

        return return_val


class ItemSetSkillsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.SkillSetID = None
        self.SkillID = None
        self.SkillCastType = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ItemSetSkillsTable()
            return_val.SkillSetID = results[0]
            return_val.SkillID = results[1]
            return_val.SkillCastType = results[2]
        else:
            return_val = []
            for row in results:
                val = ItemSetSkillsTable()
                val.SkillSetID = row[0]
                val.SkillID = row[1]
                val.SkillCastType = row[2]
                return_val.append(val)

        return return_val


class ItemSetsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.setID = None
        self.locStatus = None
        self.itemIDs = None
        self.kitType = None
        self.kitRank = None
        self.kitImage = None
        self.skillSetWith2 = None
        self.skillSetWith3 = None
        self.skillSetWith4 = None
        self.skillSetWith5 = None
        self.skillSetWith6 = None
        self.localize = None
        self.gate_version = None
        self.kitID = None
        self.priority = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ItemSetsTable()
            return_val.setID = results[0]
            return_val.locStatus = results[1]
            return_val.itemIDs = results[2]
            return_val.kitType = results[3]
            return_val.kitRank = results[4]
            return_val.kitImage = results[5]
            return_val.skillSetWith2 = results[6]
            return_val.skillSetWith3 = results[7]
            return_val.skillSetWith4 = results[8]
            return_val.skillSetWith5 = results[9]
            return_val.skillSetWith6 = results[10]
            return_val.localize = results[11]
            return_val.gate_version = results[12]
            return_val.kitID = results[13]
            return_val.priority = results[14]
        else:
            return_val = []
            for row in results:
                val = ItemSetsTable()
                val.setID = row[0]
                val.locStatus = row[1]
                val.itemIDs = row[2]
                val.kitType = row[3]
                val.kitRank = row[4]
                val.kitImage = row[5]
                val.skillSetWith2 = row[6]
                val.skillSetWith3 = row[7]
                val.skillSetWith4 = row[8]
                val.skillSetWith5 = row[9]
                val.skillSetWith6 = row[10]
                val.localize = row[11]
                val.gate_version = row[12]
                val.kitID = row[13]
                val.priority = row[14]
                return_val.append(val)

        return return_val


class JetPackPadComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.xDistance = None
        self.yDistance = None
        self.warnDistance = None
        self.lotBlocker = None
        self.lotWarningVolume = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = JetPackPadComponentTable()
            return_val.id = results[0]
            return_val.xDistance = results[1]
            return_val.yDistance = results[2]
            return_val.warnDistance = results[3]
            return_val.lotBlocker = results[4]
            return_val.lotWarningVolume = results[5]
        else:
            return_val = []
            for row in results:
                val = JetPackPadComponentTable()
                val.id = row[0]
                val.xDistance = row[1]
                val.yDistance = row[2]
                val.warnDistance = row[3]
                val.lotBlocker = row[4]
                val.lotWarningVolume = row[5]
                return_val.append(val)

        return return_val


class LUPExhibitComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.minXZ = None
        self.maxXZ = None
        self.maxY = None
        self.offsetX = None
        self.offsetY = None
        self.offsetZ = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = LUPExhibitComponentTable()
            return_val.id = results[0]
            return_val.minXZ = results[1]
            return_val.maxXZ = results[2]
            return_val.maxY = results[3]
            return_val.offsetX = results[4]
            return_val.offsetY = results[5]
            return_val.offsetZ = results[6]
        else:
            return_val = []
            for row in results:
                val = LUPExhibitComponentTable()
                val.id = row[0]
                val.minXZ = row[1]
                val.maxXZ = row[2]
                val.maxY = row[3]
                val.offsetX = row[4]
                val.offsetY = row[5]
                val.offsetZ = row[6]
                return_val.append(val)

        return return_val


class LUPExhibitModelDataTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.LOT = None
        self.minXZ = None
        self.maxXZ = None
        self.maxY = None
        self.description = None
        self.owner = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = LUPExhibitModelDataTable()
            return_val.LOT = results[0]
            return_val.minXZ = results[1]
            return_val.maxXZ = results[2]
            return_val.maxY = results[3]
            return_val.description = results[4]
            return_val.owner = results[5]
        else:
            return_val = []
            for row in results:
                val = LUPExhibitModelDataTable()
                val.LOT = row[0]
                val.minXZ = row[1]
                val.maxXZ = row[2]
                val.maxY = row[3]
                val.description = row[4]
                val.owner = row[5]
                return_val.append(val)

        return return_val


class LUPZoneIDsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.zoneID = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = LUPZoneIDsTable()
            return_val.zoneID = results[0]
        else:
            return_val = []
            for row in results:
                val = LUPZoneIDsTable()
                val.zoneID = row[0]
                return_val.append(val)

        return return_val


class LanguageTypeTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.LanguageID = None
        self.LanguageDescription = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = LanguageTypeTable()
            return_val.LanguageID = results[0]
            return_val.LanguageDescription = results[1]
        else:
            return_val = []
            for row in results:
                val = LanguageTypeTable()
                val.LanguageID = row[0]
                val.LanguageDescription = row[1]
                return_val.append(val)

        return return_val


class LevelProgressionLookupTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.requiredUScore = None
        self.BehaviorEffect = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = LevelProgressionLookupTable()
            return_val.id = results[0]
            return_val.requiredUScore = results[1]
            return_val.BehaviorEffect = results[2]
        else:
            return_val = []
            for row in results:
                val = LevelProgressionLookupTable()
                val.id = row[0]
                val.requiredUScore = row[1]
                val.BehaviorEffect = row[2]
                return_val.append(val)

        return return_val


class LootMatrixTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.LootMatrixIndex = None
        self.LootTableIndex = None
        self.RarityTableIndex = None
        self.percent = None
        self.minToDrop = None
        self.maxToDrop = None
        self.id = None
        self.flagID = None
        self.gate_version = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = LootMatrixTable()
            return_val.LootMatrixIndex = results[0]
            return_val.LootTableIndex = results[1]
            return_val.RarityTableIndex = results[2]
            return_val.percent = results[3]
            return_val.minToDrop = results[4]
            return_val.maxToDrop = results[5]
            return_val.id = results[6]
            return_val.flagID = results[7]
            return_val.gate_version = results[8]
        else:
            return_val = []
            for row in results:
                val = LootMatrixTable()
                val.LootMatrixIndex = row[0]
                val.LootTableIndex = row[1]
                val.RarityTableIndex = row[2]
                val.percent = row[3]
                val.minToDrop = row[4]
                val.maxToDrop = row[5]
                val.id = row[6]
                val.flagID = row[7]
                val.gate_version = row[8]
                return_val.append(val)

        return return_val


class LootMatrixIndexTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.LootMatrixIndex = None
        self.inNpcEditor = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = LootMatrixIndexTable()
            return_val.LootMatrixIndex = results[0]
            return_val.inNpcEditor = results[1]
        else:
            return_val = []
            for row in results:
                val = LootMatrixIndexTable()
                val.LootMatrixIndex = row[0]
                val.inNpcEditor = row[1]
                return_val.append(val)

        return return_val


class LootTableTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.itemid = None
        self.LootTableIndex = None
        self.id = None
        self.MissionDrop = None
        self.sortPriority = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = LootTableTable()
            return_val.itemid = results[0]
            return_val.LootTableIndex = results[1]
            return_val.id = results[2]
            return_val.MissionDrop = results[3]
            return_val.sortPriority = results[4]
        else:
            return_val = []
            for row in results:
                val = LootTableTable()
                val.itemid = row[0]
                val.LootTableIndex = row[1]
                val.id = row[2]
                val.MissionDrop = row[3]
                val.sortPriority = row[4]
                return_val.append(val)

        return return_val


class LootTableIndexTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.LootTableIndex = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = LootTableIndexTable()
            return_val.LootTableIndex = results[0]
        else:
            return_val = []
            for row in results:
                val = LootTableIndexTable()
                val.LootTableIndex = row[0]
                return_val.append(val)

        return return_val


class MinifigComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.head = None
        self.chest = None
        self.legs = None
        self.hairstyle = None
        self.haircolor = None
        self.chestdecal = None
        self.headcolor = None
        self.lefthand = None
        self.righthand = None
        self.eyebrowstyle = None
        self.eyesstyle = None
        self.mouthstyle = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MinifigComponentTable()
            return_val.id = results[0]
            return_val.head = results[1]
            return_val.chest = results[2]
            return_val.legs = results[3]
            return_val.hairstyle = results[4]
            return_val.haircolor = results[5]
            return_val.chestdecal = results[6]
            return_val.headcolor = results[7]
            return_val.lefthand = results[8]
            return_val.righthand = results[9]
            return_val.eyebrowstyle = results[10]
            return_val.eyesstyle = results[11]
            return_val.mouthstyle = results[12]
        else:
            return_val = []
            for row in results:
                val = MinifigComponentTable()
                val.id = row[0]
                val.head = row[1]
                val.chest = row[2]
                val.legs = row[3]
                val.hairstyle = row[4]
                val.haircolor = row[5]
                val.chestdecal = row[6]
                val.headcolor = row[7]
                val.lefthand = row[8]
                val.righthand = row[9]
                val.eyebrowstyle = row[10]
                val.eyesstyle = row[11]
                val.mouthstyle = row[12]
                return_val.append(val)

        return return_val


class MinifigDecalsEyebrowsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.ID = None
        self.High_path = None
        self.Low_path = None
        self.CharacterCreateValid = None
        self.male = None
        self.female = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MinifigDecalsEyebrowsTable()
            return_val.ID = results[0]
            return_val.High_path = results[1]
            return_val.Low_path = results[2]
            return_val.CharacterCreateValid = results[3]
            return_val.male = results[4]
            return_val.female = results[5]
        else:
            return_val = []
            for row in results:
                val = MinifigDecalsEyebrowsTable()
                val.ID = row[0]
                val.High_path = row[1]
                val.Low_path = row[2]
                val.CharacterCreateValid = row[3]
                val.male = row[4]
                val.female = row[5]
                return_val.append(val)

        return return_val


class MinifigDecalsEyesTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.ID = None
        self.High_path = None
        self.Low_path = None
        self.CharacterCreateValid = None
        self.male = None
        self.female = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MinifigDecalsEyesTable()
            return_val.ID = results[0]
            return_val.High_path = results[1]
            return_val.Low_path = results[2]
            return_val.CharacterCreateValid = results[3]
            return_val.male = results[4]
            return_val.female = results[5]
        else:
            return_val = []
            for row in results:
                val = MinifigDecalsEyesTable()
                val.ID = row[0]
                val.High_path = row[1]
                val.Low_path = row[2]
                val.CharacterCreateValid = row[3]
                val.male = row[4]
                val.female = row[5]
                return_val.append(val)

        return return_val


class MinifigDecalsLegsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.ID = None
        self.High_path = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MinifigDecalsLegsTable()
            return_val.ID = results[0]
            return_val.High_path = results[1]
        else:
            return_val = []
            for row in results:
                val = MinifigDecalsLegsTable()
                val.ID = row[0]
                val.High_path = row[1]
                return_val.append(val)

        return return_val


class MinifigDecalsMouthsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.ID = None
        self.High_path = None
        self.Low_path = None
        self.CharacterCreateValid = None
        self.male = None
        self.female = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MinifigDecalsMouthsTable()
            return_val.ID = results[0]
            return_val.High_path = results[1]
            return_val.Low_path = results[2]
            return_val.CharacterCreateValid = results[3]
            return_val.male = results[4]
            return_val.female = results[5]
        else:
            return_val = []
            for row in results:
                val = MinifigDecalsMouthsTable()
                val.ID = row[0]
                val.High_path = row[1]
                val.Low_path = row[2]
                val.CharacterCreateValid = row[3]
                val.male = row[4]
                val.female = row[5]
                return_val.append(val)

        return return_val


class MinifigDecalsTorsosTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.ID = None
        self.High_path = None
        self.CharacterCreateValid = None
        self.male = None
        self.female = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MinifigDecalsTorsosTable()
            return_val.ID = results[0]
            return_val.High_path = results[1]
            return_val.CharacterCreateValid = results[2]
            return_val.male = results[3]
            return_val.female = results[4]
        else:
            return_val = []
            for row in results:
                val = MinifigDecalsTorsosTable()
                val.ID = row[0]
                val.High_path = row[1]
                val.CharacterCreateValid = row[2]
                val.male = row[3]
                val.female = row[4]
                return_val.append(val)

        return return_val


class MissionEmailTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.ID = None
        self.messageType = None
        self.notificationGroup = None
        self.missionID = None
        self.attachmentLOT = None
        self.localize = None
        self.locStatus = None
        self.gate_version = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MissionEmailTable()
            return_val.ID = results[0]
            return_val.messageType = results[1]
            return_val.notificationGroup = results[2]
            return_val.missionID = results[3]
            return_val.attachmentLOT = results[4]
            return_val.localize = results[5]
            return_val.locStatus = results[6]
            return_val.gate_version = results[7]
        else:
            return_val = []
            for row in results:
                val = MissionEmailTable()
                val.ID = row[0]
                val.messageType = row[1]
                val.notificationGroup = row[2]
                val.missionID = row[3]
                val.attachmentLOT = row[4]
                val.localize = row[5]
                val.locStatus = row[6]
                val.gate_version = row[7]
                return_val.append(val)

        return return_val


class MissionNPCComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.missionID = None
        self.offersMission = None
        self.acceptsMission = None
        self.gate_version = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MissionNPCComponentTable()
            return_val.id = results[0]
            return_val.missionID = results[1]
            return_val.offersMission = results[2]
            return_val.acceptsMission = results[3]
            return_val.gate_version = results[4]
        else:
            return_val = []
            for row in results:
                val = MissionNPCComponentTable()
                val.id = row[0]
                val.missionID = row[1]
                val.offersMission = row[2]
                val.acceptsMission = row[3]
                val.gate_version = row[4]
                return_val.append(val)

        return return_val


class MissionTasksTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.locStatus = None
        self.taskType = None
        self.target = None
        self.targetGroup = None
        self.targetValue = None
        self.taskParam1 = None
        self.largeTaskIcon = None
        self.IconID = None
        self.uid = None
        self.largeTaskIconID = None
        self.localize = None
        self.gate_version = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MissionTasksTable()
            return_val.id = results[0]
            return_val.locStatus = results[1]
            return_val.taskType = results[2]
            return_val.target = results[3]
            return_val.targetGroup = results[4]
            return_val.targetValue = results[5]
            return_val.taskParam1 = results[6]
            return_val.largeTaskIcon = results[7]
            return_val.IconID = results[8]
            return_val.uid = results[9]
            return_val.largeTaskIconID = results[10]
            return_val.localize = results[11]
            return_val.gate_version = results[12]
        else:
            return_val = []
            for row in results:
                val = MissionTasksTable()
                val.id = row[0]
                val.locStatus = row[1]
                val.taskType = row[2]
                val.target = row[3]
                val.targetGroup = row[4]
                val.targetValue = row[5]
                val.taskParam1 = row[6]
                val.largeTaskIcon = row[7]
                val.IconID = row[8]
                val.uid = row[9]
                val.largeTaskIconID = row[10]
                val.localize = row[11]
                val.gate_version = row[12]
                return_val.append(val)

        return return_val


class MissionTextTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.story_icon = None
        self.missionIcon = None
        self.offerNPCIcon = None
        self.IconID = None
        self.state_1_anim = None
        self.state_2_anim = None
        self.state_3_anim = None
        self.state_4_anim = None
        self.state_3_turnin_anim = None
        self.state_4_turnin_anim = None
        self.onclick_anim = None
        self.CinematicAccepted = None
        self.CinematicAcceptedLeadin = None
        self.CinematicCompleted = None
        self.CinematicCompletedLeadin = None
        self.CinematicRepeatable = None
        self.CinematicRepeatableLeadin = None
        self.CinematicRepeatableCompleted = None
        self.CinematicRepeatableCompletedLeadin = None
        self.AudioEventGUID_Interact = None
        self.AudioEventGUID_OfferAccept = None
        self.AudioEventGUID_OfferDeny = None
        self.AudioEventGUID_Completed = None
        self.AudioEventGUID_TurnIn = None
        self.AudioEventGUID_Failed = None
        self.AudioEventGUID_Progress = None
        self.AudioMusicCue_OfferAccept = None
        self.AudioMusicCue_TurnIn = None
        self.turnInIconID = None
        self.localize = None
        self.locStatus = None
        self.gate_version = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MissionTextTable()
            return_val.id = results[0]
            return_val.story_icon = results[1]
            return_val.missionIcon = results[2]
            return_val.offerNPCIcon = results[3]
            return_val.IconID = results[4]
            return_val.state_1_anim = results[5]
            return_val.state_2_anim = results[6]
            return_val.state_3_anim = results[7]
            return_val.state_4_anim = results[8]
            return_val.state_3_turnin_anim = results[9]
            return_val.state_4_turnin_anim = results[10]
            return_val.onclick_anim = results[11]
            return_val.CinematicAccepted = results[12]
            return_val.CinematicAcceptedLeadin = results[13]
            return_val.CinematicCompleted = results[14]
            return_val.CinematicCompletedLeadin = results[15]
            return_val.CinematicRepeatable = results[16]
            return_val.CinematicRepeatableLeadin = results[17]
            return_val.CinematicRepeatableCompleted = results[18]
            return_val.CinematicRepeatableCompletedLeadin = results[19]
            return_val.AudioEventGUID_Interact = results[20]
            return_val.AudioEventGUID_OfferAccept = results[21]
            return_val.AudioEventGUID_OfferDeny = results[22]
            return_val.AudioEventGUID_Completed = results[23]
            return_val.AudioEventGUID_TurnIn = results[24]
            return_val.AudioEventGUID_Failed = results[25]
            return_val.AudioEventGUID_Progress = results[26]
            return_val.AudioMusicCue_OfferAccept = results[27]
            return_val.AudioMusicCue_TurnIn = results[28]
            return_val.turnInIconID = results[29]
            return_val.localize = results[30]
            return_val.locStatus = results[31]
            return_val.gate_version = results[32]
        else:
            return_val = []
            for row in results:
                val = MissionTextTable()
                val.id = row[0]
                val.story_icon = row[1]
                val.missionIcon = row[2]
                val.offerNPCIcon = row[3]
                val.IconID = row[4]
                val.state_1_anim = row[5]
                val.state_2_anim = row[6]
                val.state_3_anim = row[7]
                val.state_4_anim = row[8]
                val.state_3_turnin_anim = row[9]
                val.state_4_turnin_anim = row[10]
                val.onclick_anim = row[11]
                val.CinematicAccepted = row[12]
                val.CinematicAcceptedLeadin = row[13]
                val.CinematicCompleted = row[14]
                val.CinematicCompletedLeadin = row[15]
                val.CinematicRepeatable = row[16]
                val.CinematicRepeatableLeadin = row[17]
                val.CinematicRepeatableCompleted = row[18]
                val.CinematicRepeatableCompletedLeadin = row[19]
                val.AudioEventGUID_Interact = row[20]
                val.AudioEventGUID_OfferAccept = row[21]
                val.AudioEventGUID_OfferDeny = row[22]
                val.AudioEventGUID_Completed = row[23]
                val.AudioEventGUID_TurnIn = row[24]
                val.AudioEventGUID_Failed = row[25]
                val.AudioEventGUID_Progress = row[26]
                val.AudioMusicCue_OfferAccept = row[27]
                val.AudioMusicCue_TurnIn = row[28]
                val.turnInIconID = row[29]
                val.localize = row[30]
                val.locStatus = row[31]
                val.gate_version = row[32]
                return_val.append(val)

        return return_val


class MissionsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.defined_type = None
        self.defined_subtype = None
        self.UISortOrder = None
        self.offer_objectID = None
        self.target_objectID = None
        self.reward_currency = None
        self.LegoScore = None
        self.reward_reputation = None
        self.isChoiceReward = None
        self.reward_item1 = None
        self.reward_item1_count = None
        self.reward_item2 = None
        self.reward_item2_count = None
        self.reward_item3 = None
        self.reward_item3_count = None
        self.reward_item4 = None
        self.reward_item4_count = None
        self.reward_emote = None
        self.reward_emote2 = None
        self.reward_emote3 = None
        self.reward_emote4 = None
        self.reward_maximagination = None
        self.reward_maxhealth = None
        self.reward_maxinventory = None
        self.reward_maxmodel = None
        self.reward_maxwidget = None
        self.reward_maxwallet = None
        self.repeatable = None
        self.reward_currency_repeatable = None
        self.reward_item1_repeatable = None
        self.reward_item1_repeat_count = None
        self.reward_item2_repeatable = None
        self.reward_item2_repeat_count = None
        self.reward_item3_repeatable = None
        self.reward_item3_repeat_count = None
        self.reward_item4_repeatable = None
        self.reward_item4_repeat_count = None
        self.time_limit = None
        self.isMission = None
        self.missionIconID = None
        self.prereqMissionID = None
        self.localize = None
        self.inMOTD = None
        self.cooldownTime = None
        self.isRandom = None
        self.randomPool = None
        self.UIPrereqID = None
        self.gate_version = None
        self.HUDStates = None
        self.locStatus = None
        self.reward_bankinventory = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MissionsTable()
            return_val.id = results[0]
            return_val.defined_type = results[1]
            return_val.defined_subtype = results[2]
            return_val.UISortOrder = results[3]
            return_val.offer_objectID = results[4]
            return_val.target_objectID = results[5]
            return_val.reward_currency = results[6]
            return_val.LegoScore = results[7]
            return_val.reward_reputation = results[8]
            return_val.isChoiceReward = results[9]
            return_val.reward_item1 = results[10]
            return_val.reward_item1_count = results[11]
            return_val.reward_item2 = results[12]
            return_val.reward_item2_count = results[13]
            return_val.reward_item3 = results[14]
            return_val.reward_item3_count = results[15]
            return_val.reward_item4 = results[16]
            return_val.reward_item4_count = results[17]
            return_val.reward_emote = results[18]
            return_val.reward_emote2 = results[19]
            return_val.reward_emote3 = results[20]
            return_val.reward_emote4 = results[21]
            return_val.reward_maximagination = results[22]
            return_val.reward_maxhealth = results[23]
            return_val.reward_maxinventory = results[24]
            return_val.reward_maxmodel = results[25]
            return_val.reward_maxwidget = results[26]
            return_val.reward_maxwallet = results[27]
            return_val.repeatable = results[28]
            return_val.reward_currency_repeatable = results[29]
            return_val.reward_item1_repeatable = results[30]
            return_val.reward_item1_repeat_count = results[31]
            return_val.reward_item2_repeatable = results[32]
            return_val.reward_item2_repeat_count = results[33]
            return_val.reward_item3_repeatable = results[34]
            return_val.reward_item3_repeat_count = results[35]
            return_val.reward_item4_repeatable = results[36]
            return_val.reward_item4_repeat_count = results[37]
            return_val.time_limit = results[38]
            return_val.isMission = results[39]
            return_val.missionIconID = results[40]
            return_val.prereqMissionID = results[41]
            return_val.localize = results[42]
            return_val.inMOTD = results[43]
            return_val.cooldownTime = results[44]
            return_val.isRandom = results[45]
            return_val.randomPool = results[46]
            return_val.UIPrereqID = results[47]
            return_val.gate_version = results[48]
            return_val.HUDStates = results[49]
            return_val.locStatus = results[50]
            return_val.reward_bankinventory = results[51]
        else:
            return_val = []
            for row in results:
                val = MissionsTable()
                val.id = row[0]
                val.defined_type = row[1]
                val.defined_subtype = row[2]
                val.UISortOrder = row[3]
                val.offer_objectID = row[4]
                val.target_objectID = row[5]
                val.reward_currency = row[6]
                val.LegoScore = row[7]
                val.reward_reputation = row[8]
                val.isChoiceReward = row[9]
                val.reward_item1 = row[10]
                val.reward_item1_count = row[11]
                val.reward_item2 = row[12]
                val.reward_item2_count = row[13]
                val.reward_item3 = row[14]
                val.reward_item3_count = row[15]
                val.reward_item4 = row[16]
                val.reward_item4_count = row[17]
                val.reward_emote = row[18]
                val.reward_emote2 = row[19]
                val.reward_emote3 = row[20]
                val.reward_emote4 = row[21]
                val.reward_maximagination = row[22]
                val.reward_maxhealth = row[23]
                val.reward_maxinventory = row[24]
                val.reward_maxmodel = row[25]
                val.reward_maxwidget = row[26]
                val.reward_maxwallet = row[27]
                val.repeatable = row[28]
                val.reward_currency_repeatable = row[29]
                val.reward_item1_repeatable = row[30]
                val.reward_item1_repeat_count = row[31]
                val.reward_item2_repeatable = row[32]
                val.reward_item2_repeat_count = row[33]
                val.reward_item3_repeatable = row[34]
                val.reward_item3_repeat_count = row[35]
                val.reward_item4_repeatable = row[36]
                val.reward_item4_repeat_count = row[37]
                val.time_limit = row[38]
                val.isMission = row[39]
                val.missionIconID = row[40]
                val.prereqMissionID = row[41]
                val.localize = row[42]
                val.inMOTD = row[43]
                val.cooldownTime = row[44]
                val.isRandom = row[45]
                val.randomPool = row[46]
                val.UIPrereqID = row[47]
                val.gate_version = row[48]
                val.HUDStates = row[49]
                val.locStatus = row[50]
                val.reward_bankinventory = row[51]
                return_val.append(val)

        return return_val


class ModelBehaviorTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.definitionXMLfilename = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ModelBehaviorTable()
            return_val.id = results[0]
            return_val.definitionXMLfilename = results[1]
        else:
            return_val = []
            for row in results:
                val = ModelBehaviorTable()
                val.id = row[0]
                val.definitionXMLfilename = row[1]
                return_val.append(val)

        return return_val


class ModularBuildComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.buildType = None
        self.xml = None
        self.createdLOT = None
        self.createdPhysicsID = None
        self.AudioEventGUID_Snap = None
        self.AudioEventGUID_Complete = None
        self.AudioEventGUID_Present = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ModularBuildComponentTable()
            return_val.id = results[0]
            return_val.buildType = results[1]
            return_val.xml = results[2]
            return_val.createdLOT = results[3]
            return_val.createdPhysicsID = results[4]
            return_val.AudioEventGUID_Snap = results[5]
            return_val.AudioEventGUID_Complete = results[6]
            return_val.AudioEventGUID_Present = results[7]
        else:
            return_val = []
            for row in results:
                val = ModularBuildComponentTable()
                val.id = row[0]
                val.buildType = row[1]
                val.xml = row[2]
                val.createdLOT = row[3]
                val.createdPhysicsID = row[4]
                val.AudioEventGUID_Snap = row[5]
                val.AudioEventGUID_Complete = row[6]
                val.AudioEventGUID_Present = row[7]
                return_val.append(val)

        return return_val


class ModuleComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.partCode = None
        self.buildType = None
        self.xml = None
        self.primarySoundGUID = None
        self.assembledEffectID = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ModuleComponentTable()
            return_val.id = results[0]
            return_val.partCode = results[1]
            return_val.buildType = results[2]
            return_val.xml = results[3]
            return_val.primarySoundGUID = results[4]
            return_val.assembledEffectID = results[5]
        else:
            return_val = []
            for row in results:
                val = ModuleComponentTable()
                val.id = row[0]
                val.partCode = row[1]
                val.buildType = row[2]
                val.xml = row[3]
                val.primarySoundGUID = row[4]
                val.assembledEffectID = row[5]
                return_val.append(val)

        return return_val


class MotionFXTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.typeID = None
        self.slamVelocity = None
        self.addVelocity = None
        self.duration = None
        self.destGroupName = None
        self.startScale = None
        self.endScale = None
        self.velocity = None
        self.distance = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MotionFXTable()
            return_val.id = results[0]
            return_val.typeID = results[1]
            return_val.slamVelocity = results[2]
            return_val.addVelocity = results[3]
            return_val.duration = results[4]
            return_val.destGroupName = results[5]
            return_val.startScale = results[6]
            return_val.endScale = results[7]
            return_val.velocity = results[8]
            return_val.distance = results[9]
        else:
            return_val = []
            for row in results:
                val = MotionFXTable()
                val.id = row[0]
                val.typeID = row[1]
                val.slamVelocity = row[2]
                val.addVelocity = row[3]
                val.duration = row[4]
                val.destGroupName = row[5]
                val.startScale = row[6]
                val.endScale = row[7]
                val.velocity = row[8]
                val.distance = row[9]
                return_val.append(val)

        return return_val


class MovementAIComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.MovementType = None
        self.WanderChance = None
        self.WanderDelayMin = None
        self.WanderDelayMax = None
        self.WanderSpeed = None
        self.WanderRadius = None
        self.attachedPath = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MovementAIComponentTable()
            return_val.id = results[0]
            return_val.MovementType = results[1]
            return_val.WanderChance = results[2]
            return_val.WanderDelayMin = results[3]
            return_val.WanderDelayMax = results[4]
            return_val.WanderSpeed = results[5]
            return_val.WanderRadius = results[6]
            return_val.attachedPath = results[7]
        else:
            return_val = []
            for row in results:
                val = MovementAIComponentTable()
                val.id = row[0]
                val.MovementType = row[1]
                val.WanderChance = row[2]
                val.WanderDelayMin = row[3]
                val.WanderDelayMax = row[4]
                val.WanderSpeed = row[5]
                val.WanderRadius = row[6]
                val.attachedPath = row[7]
                return_val.append(val)

        return return_val


class MovingPlatformsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.platformIsSimpleMover = None
        self.platformMoveX = None
        self.platformMoveY = None
        self.platformMoveZ = None
        self.platformMoveTime = None
        self.platformStartAtEnd = None
        self.description = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MovingPlatformsTable()
            return_val.id = results[0]
            return_val.platformIsSimpleMover = results[1]
            return_val.platformMoveX = results[2]
            return_val.platformMoveY = results[3]
            return_val.platformMoveZ = results[4]
            return_val.platformMoveTime = results[5]
            return_val.platformStartAtEnd = results[6]
            return_val.description = results[7]
        else:
            return_val = []
            for row in results:
                val = MovingPlatformsTable()
                val.id = row[0]
                val.platformIsSimpleMover = row[1]
                val.platformMoveX = row[2]
                val.platformMoveY = row[3]
                val.platformMoveZ = row[4]
                val.platformMoveTime = row[5]
                val.platformStartAtEnd = row[6]
                val.description = row[7]
                return_val.append(val)

        return return_val


class NpcIconsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.color = None
        self.offset = None
        self.LOT = None
        self.Texture = None
        self.isClickable = None
        self.scale = None
        self.rotateToFace = None
        self.compositeHorizOffset = None
        self.compositeVertOffset = None
        self.compositeScale = None
        self.compositeConnectionNode = None
        self.compositeLOTMultiMission = None
        self.compositeLOTMultiMissionVentor = None
        self.compositeIconTexture = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = NpcIconsTable()
            return_val.id = results[0]
            return_val.color = results[1]
            return_val.offset = results[2]
            return_val.LOT = results[3]
            return_val.Texture = results[4]
            return_val.isClickable = results[5]
            return_val.scale = results[6]
            return_val.rotateToFace = results[7]
            return_val.compositeHorizOffset = results[8]
            return_val.compositeVertOffset = results[9]
            return_val.compositeScale = results[10]
            return_val.compositeConnectionNode = results[11]
            return_val.compositeLOTMultiMission = results[12]
            return_val.compositeLOTMultiMissionVentor = results[13]
            return_val.compositeIconTexture = results[14]
        else:
            return_val = []
            for row in results:
                val = NpcIconsTable()
                val.id = row[0]
                val.color = row[1]
                val.offset = row[2]
                val.LOT = row[3]
                val.Texture = row[4]
                val.isClickable = row[5]
                val.scale = row[6]
                val.rotateToFace = row[7]
                val.compositeHorizOffset = row[8]
                val.compositeVertOffset = row[9]
                val.compositeScale = row[10]
                val.compositeConnectionNode = row[11]
                val.compositeLOTMultiMission = row[12]
                val.compositeLOTMultiMissionVentor = row[13]
                val.compositeIconTexture = row[14]
                return_val.append(val)

        return return_val


class ObjectBehaviorXREFTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.LOT = None
        self.behaviorID1 = None
        self.behaviorID2 = None
        self.behaviorID3 = None
        self.behaviorID4 = None
        self.behaviorID5 = None
        self.type = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ObjectBehaviorXREFTable()
            return_val.LOT = results[0]
            return_val.behaviorID1 = results[1]
            return_val.behaviorID2 = results[2]
            return_val.behaviorID3 = results[3]
            return_val.behaviorID4 = results[4]
            return_val.behaviorID5 = results[5]
            return_val.type = results[6]
        else:
            return_val = []
            for row in results:
                val = ObjectBehaviorXREFTable()
                val.LOT = row[0]
                val.behaviorID1 = row[1]
                val.behaviorID2 = row[2]
                val.behaviorID3 = row[3]
                val.behaviorID4 = row[4]
                val.behaviorID5 = row[5]
                val.type = row[6]
                return_val.append(val)

        return return_val


class ObjectBehaviorsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.BehaviorID = None
        self.xmldata = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ObjectBehaviorsTable()
            return_val.BehaviorID = results[0]
            return_val.xmldata = results[1]
        else:
            return_val = []
            for row in results:
                val = ObjectBehaviorsTable()
                val.BehaviorID = row[0]
                val.xmldata = row[1]
                return_val.append(val)

        return return_val


class ObjectSkillsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.objectTemplate = None
        self.skillID = None
        self.castOnType = None
        self.AICombatWeight = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ObjectSkillsTable()
            return_val.objectTemplate = results[0]
            return_val.skillID = results[1]
            return_val.castOnType = results[2]
            return_val.AICombatWeight = results[3]
        else:
            return_val = []
            for row in results:
                val = ObjectSkillsTable()
                val.objectTemplate = row[0]
                val.skillID = row[1]
                val.castOnType = row[2]
                val.AICombatWeight = row[3]
                return_val.append(val)

        return return_val


class ObjectsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.name = None
        self.placeable = None
        self.type = None
        self.description = None
        self.localize = None
        self.npcTemplateID = None
        self.displayName = None
        self.interactionDistance = None
        self.nametag = None
        self._internalNotes = None
        self.locStatus = None
        self.gate_version = None
        self.HQ_valid = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ObjectsTable()
            return_val.id = results[0]
            return_val.name = results[1]
            return_val.placeable = results[2]
            return_val.type = results[3]
            return_val.description = results[4]
            return_val.localize = results[5]
            return_val.npcTemplateID = results[6]
            return_val.displayName = results[7]
            return_val.interactionDistance = results[8]
            return_val.nametag = results[9]
            return_val._internalNotes = results[10]
            return_val.locStatus = results[11]
            return_val.gate_version = results[12]
            return_val.HQ_valid = results[13]
        else:
            return_val = []
            for row in results:
                val = ObjectsTable()
                val.id = row[0]
                val.name = row[1]
                val.placeable = row[2]
                val.type = row[3]
                val.description = row[4]
                val.localize = row[5]
                val.npcTemplateID = row[6]
                val.displayName = row[7]
                val.interactionDistance = row[8]
                val.nametag = row[9]
                val._internalNotes = row[10]
                val.locStatus = row[11]
                val.gate_version = row[12]
                val.HQ_valid = row[13]
                return_val.append(val)

        return return_val


class PackageComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.LootMatrixIndex = None
        self.packageType = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = PackageComponentTable()
            return_val.id = results[0]
            return_val.LootMatrixIndex = results[1]
            return_val.packageType = results[2]
        else:
            return_val = []
            for row in results:
                val = PackageComponentTable()
                val.id = row[0]
                val.LootMatrixIndex = row[1]
                val.packageType = row[2]
                return_val.append(val)

        return return_val


class PetAbilitiesTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.AbilityName = None
        self.ImaginationCost = None
        self.locStatus = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = PetAbilitiesTable()
            return_val.id = results[0]
            return_val.AbilityName = results[1]
            return_val.ImaginationCost = results[2]
            return_val.locStatus = results[3]
        else:
            return_val = []
            for row in results:
                val = PetAbilitiesTable()
                val.id = row[0]
                val.AbilityName = row[1]
                val.ImaginationCost = row[2]
                val.locStatus = row[3]
                return_val.append(val)

        return return_val


class PetComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.minTameUpdateTime = None
        self.maxTameUpdateTime = None
        self.percentTameChance = None
        self.tamability = None
        self.elementType = None
        self.walkSpeed = None
        self.runSpeed = None
        self.sprintSpeed = None
        self.idleTimeMin = None
        self.idleTimeMax = None
        self.petForm = None
        self.imaginationDrainRate = None
        self.AudioMetaEventSet = None
        self.buffIDs = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = PetComponentTable()
            return_val.id = results[0]
            return_val.minTameUpdateTime = results[1]
            return_val.maxTameUpdateTime = results[2]
            return_val.percentTameChance = results[3]
            return_val.tamability = results[4]
            return_val.elementType = results[5]
            return_val.walkSpeed = results[6]
            return_val.runSpeed = results[7]
            return_val.sprintSpeed = results[8]
            return_val.idleTimeMin = results[9]
            return_val.idleTimeMax = results[10]
            return_val.petForm = results[11]
            return_val.imaginationDrainRate = results[12]
            return_val.AudioMetaEventSet = results[13]
            return_val.buffIDs = results[14]
        else:
            return_val = []
            for row in results:
                val = PetComponentTable()
                val.id = row[0]
                val.minTameUpdateTime = row[1]
                val.maxTameUpdateTime = row[2]
                val.percentTameChance = row[3]
                val.tamability = row[4]
                val.elementType = row[5]
                val.walkSpeed = row[6]
                val.runSpeed = row[7]
                val.sprintSpeed = row[8]
                val.idleTimeMin = row[9]
                val.idleTimeMax = row[10]
                val.petForm = row[11]
                val.imaginationDrainRate = row[12]
                val.AudioMetaEventSet = row[13]
                val.buffIDs = row[14]
                return_val.append(val)

        return return_val


class PetNestComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.ElementalType = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = PetNestComponentTable()
            return_val.id = results[0]
            return_val.ElementalType = results[1]
        else:
            return_val = []
            for row in results:
                val = PetNestComponentTable()
                val.id = row[0]
                val.ElementalType = row[1]
                return_val.append(val)

        return return_val


class PhysicsComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.static = None
        self.physics_asset = None
        self.jump = None
        self.doublejump = None
        self.speed = None
        self.rotSpeed = None
        self.playerHeight = None
        self.playerRadius = None
        self.pcShapeType = None
        self.collisionGroup = None
        self.airSpeed = None
        self.boundaryAsset = None
        self.jumpAirSpeed = None
        self.friction = None
        self.gravityVolumeAsset = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = PhysicsComponentTable()
            return_val.id = results[0]
            return_val.static = results[1]
            return_val.physics_asset = results[2]
            return_val.jump = results[3]
            return_val.doublejump = results[4]
            return_val.speed = results[5]
            return_val.rotSpeed = results[6]
            return_val.playerHeight = results[7]
            return_val.playerRadius = results[8]
            return_val.pcShapeType = results[9]
            return_val.collisionGroup = results[10]
            return_val.airSpeed = results[11]
            return_val.boundaryAsset = results[12]
            return_val.jumpAirSpeed = results[13]
            return_val.friction = results[14]
            return_val.gravityVolumeAsset = results[15]
        else:
            return_val = []
            for row in results:
                val = PhysicsComponentTable()
                val.id = row[0]
                val.static = row[1]
                val.physics_asset = row[2]
                val.jump = row[3]
                val.doublejump = row[4]
                val.speed = row[5]
                val.rotSpeed = row[6]
                val.playerHeight = row[7]
                val.playerRadius = row[8]
                val.pcShapeType = row[9]
                val.collisionGroup = row[10]
                val.airSpeed = row[11]
                val.boundaryAsset = row[12]
                val.jumpAirSpeed = row[13]
                val.friction = row[14]
                val.gravityVolumeAsset = row[15]
                return_val.append(val)

        return return_val


class PlayerFlagsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.SessionOnly = None
        self.OnlySetByServer = None
        self.SessionZoneOnly = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = PlayerFlagsTable()
            return_val.id = results[0]
            return_val.SessionOnly = results[1]
            return_val.OnlySetByServer = results[2]
            return_val.SessionZoneOnly = results[3]
        else:
            return_val = []
            for row in results:
                val = PlayerFlagsTable()
                val.id = row[0]
                val.SessionOnly = row[1]
                val.OnlySetByServer = row[2]
                val.SessionZoneOnly = row[3]
                return_val.append(val)

        return return_val


class PlayerStatisticsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.statID = None
        self.sortOrder = None
        self.locStatus = None
        self.gate_version = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = PlayerStatisticsTable()
            return_val.statID = results[0]
            return_val.sortOrder = results[1]
            return_val.locStatus = results[2]
            return_val.gate_version = results[3]
        else:
            return_val = []
            for row in results:
                val = PlayerStatisticsTable()
                val.statID = row[0]
                val.sortOrder = row[1]
                val.locStatus = row[2]
                val.gate_version = row[3]
                return_val.append(val)

        return return_val


class PossessableComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.controlSchemeID = None
        self.minifigAttachPoint = None
        self.minifigAttachAnimation = None
        self.minifigDetachAnimation = None
        self.mountAttachAnimation = None
        self.mountDetachAnimation = None
        self.attachOffsetFwd = None
        self.attachOffsetRight = None
        self.possessionType = None
        self.wantBillboard = None
        self.billboardOffsetUp = None
        self.depossessOnHit = None
        self.hitStunTime = None
        self.skillSet = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = PossessableComponentTable()
            return_val.id = results[0]
            return_val.controlSchemeID = results[1]
            return_val.minifigAttachPoint = results[2]
            return_val.minifigAttachAnimation = results[3]
            return_val.minifigDetachAnimation = results[4]
            return_val.mountAttachAnimation = results[5]
            return_val.mountDetachAnimation = results[6]
            return_val.attachOffsetFwd = results[7]
            return_val.attachOffsetRight = results[8]
            return_val.possessionType = results[9]
            return_val.wantBillboard = results[10]
            return_val.billboardOffsetUp = results[11]
            return_val.depossessOnHit = results[12]
            return_val.hitStunTime = results[13]
            return_val.skillSet = results[14]
        else:
            return_val = []
            for row in results:
                val = PossessableComponentTable()
                val.id = row[0]
                val.controlSchemeID = row[1]
                val.minifigAttachPoint = row[2]
                val.minifigAttachAnimation = row[3]
                val.minifigDetachAnimation = row[4]
                val.mountAttachAnimation = row[5]
                val.mountDetachAnimation = row[6]
                val.attachOffsetFwd = row[7]
                val.attachOffsetRight = row[8]
                val.possessionType = row[9]
                val.wantBillboard = row[10]
                val.billboardOffsetUp = row[11]
                val.depossessOnHit = row[12]
                val.hitStunTime = row[13]
                val.skillSet = row[14]
                return_val.append(val)

        return return_val


class PreconditionsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.type = None
        self.targetLOT = None
        self.targetGroup = None
        self.targetCount = None
        self.iconID = None
        self.localize = None
        self.validContexts = None
        self.locStatus = None
        self.gate_version = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = PreconditionsTable()
            return_val.id = results[0]
            return_val.type = results[1]
            return_val.targetLOT = results[2]
            return_val.targetGroup = results[3]
            return_val.targetCount = results[4]
            return_val.iconID = results[5]
            return_val.localize = results[6]
            return_val.validContexts = results[7]
            return_val.locStatus = results[8]
            return_val.gate_version = results[9]
        else:
            return_val = []
            for row in results:
                val = PreconditionsTable()
                val.id = row[0]
                val.type = row[1]
                val.targetLOT = row[2]
                val.targetGroup = row[3]
                val.targetCount = row[4]
                val.iconID = row[5]
                val.localize = row[6]
                val.validContexts = row[7]
                val.locStatus = row[8]
                val.gate_version = row[9]
                return_val.append(val)

        return return_val


class PropertyEntranceComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.mapID = None
        self.propertyName = None
        self.isOnProperty = None
        self.groupType = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = PropertyEntranceComponentTable()
            return_val.id = results[0]
            return_val.mapID = results[1]
            return_val.propertyName = results[2]
            return_val.isOnProperty = results[3]
            return_val.groupType = results[4]
        else:
            return_val = []
            for row in results:
                val = PropertyEntranceComponentTable()
                val.id = row[0]
                val.mapID = row[1]
                val.propertyName = row[2]
                val.isOnProperty = row[3]
                val.groupType = row[4]
                return_val.append(val)

        return return_val


class PropertyTemplateTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.mapID = None
        self.vendorMapID = None
        self.spawnName = None
        self.type = None
        self.sizecode = None
        self.minimumPrice = None
        self.rentDuration = None
        self.path = None
        self.cloneLimit = None
        self.durationType = None
        self.achievementRequired = None
        self.zoneX = None
        self.zoneY = None
        self.zoneZ = None
        self.maxBuildHeight = None
        self.localize = None
        self.reputationPerMinute = None
        self.locStatus = None
        self.gate_version = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = PropertyTemplateTable()
            return_val.id = results[0]
            return_val.mapID = results[1]
            return_val.vendorMapID = results[2]
            return_val.spawnName = results[3]
            return_val.type = results[4]
            return_val.sizecode = results[5]
            return_val.minimumPrice = results[6]
            return_val.rentDuration = results[7]
            return_val.path = results[8]
            return_val.cloneLimit = results[9]
            return_val.durationType = results[10]
            return_val.achievementRequired = results[11]
            return_val.zoneX = results[12]
            return_val.zoneY = results[13]
            return_val.zoneZ = results[14]
            return_val.maxBuildHeight = results[15]
            return_val.localize = results[16]
            return_val.reputationPerMinute = results[17]
            return_val.locStatus = results[18]
            return_val.gate_version = results[19]
        else:
            return_val = []
            for row in results:
                val = PropertyTemplateTable()
                val.id = row[0]
                val.mapID = row[1]
                val.vendorMapID = row[2]
                val.spawnName = row[3]
                val.type = row[4]
                val.sizecode = row[5]
                val.minimumPrice = row[6]
                val.rentDuration = row[7]
                val.path = row[8]
                val.cloneLimit = row[9]
                val.durationType = row[10]
                val.achievementRequired = row[11]
                val.zoneX = row[12]
                val.zoneY = row[13]
                val.zoneZ = row[14]
                val.maxBuildHeight = row[15]
                val.localize = row[16]
                val.reputationPerMinute = row[17]
                val.locStatus = row[18]
                val.gate_version = row[19]
                return_val.append(val)

        return return_val


class ProximityMonitorComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.Proximities = None
        self.LoadOnClient = None
        self.LoadOnServer = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ProximityMonitorComponentTable()
            return_val.id = results[0]
            return_val.Proximities = results[1]
            return_val.LoadOnClient = results[2]
            return_val.LoadOnServer = results[3]
        else:
            return_val = []
            for row in results:
                val = ProximityMonitorComponentTable()
                val.id = row[0]
                val.Proximities = row[1]
                val.LoadOnClient = row[2]
                val.LoadOnServer = row[3]
                return_val.append(val)

        return return_val


class ProximityTypesTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.Name = None
        self.Radius = None
        self.CollisionGroup = None
        self.PassiveChecks = None
        self.IconID = None
        self.LoadOnClient = None
        self.LoadOnServer = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ProximityTypesTable()
            return_val.id = results[0]
            return_val.Name = results[1]
            return_val.Radius = results[2]
            return_val.CollisionGroup = results[3]
            return_val.PassiveChecks = results[4]
            return_val.IconID = results[5]
            return_val.LoadOnClient = results[6]
            return_val.LoadOnServer = results[7]
        else:
            return_val = []
            for row in results:
                val = ProximityTypesTable()
                val.id = row[0]
                val.Name = row[1]
                val.Radius = row[2]
                val.CollisionGroup = row[3]
                val.PassiveChecks = row[4]
                val.IconID = row[5]
                val.LoadOnClient = row[6]
                val.LoadOnServer = row[7]
                return_val.append(val)

        return return_val


class RacingModuleComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.topSpeed = None
        self.acceleration = None
        self.handling = None
        self.stability = None
        self.imagination = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = RacingModuleComponentTable()
            return_val.id = results[0]
            return_val.topSpeed = results[1]
            return_val.acceleration = results[2]
            return_val.handling = results[3]
            return_val.stability = results[4]
            return_val.imagination = results[5]
        else:
            return_val = []
            for row in results:
                val = RacingModuleComponentTable()
                val.id = row[0]
                val.topSpeed = row[1]
                val.acceleration = row[2]
                val.handling = row[3]
                val.stability = row[4]
                val.imagination = row[5]
                return_val.append(val)

        return return_val


class RailActivatorComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.startAnim = None
        self.loopAnim = None
        self.stopAnim = None
        self.startSound = None
        self.loopSound = None
        self.stopSound = None
        self.effectIDs = None
        self.preconditions = None
        self.playerCollision = None
        self.cameraLocked = None
        self.StartEffectID = None
        self.StopEffectID = None
        self.DamageImmune = None
        self.NoAggro = None
        self.ShowNameBillboard = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = RailActivatorComponentTable()
            return_val.id = results[0]
            return_val.startAnim = results[1]
            return_val.loopAnim = results[2]
            return_val.stopAnim = results[3]
            return_val.startSound = results[4]
            return_val.loopSound = results[5]
            return_val.stopSound = results[6]
            return_val.effectIDs = results[7]
            return_val.preconditions = results[8]
            return_val.playerCollision = results[9]
            return_val.cameraLocked = results[10]
            return_val.StartEffectID = results[11]
            return_val.StopEffectID = results[12]
            return_val.DamageImmune = results[13]
            return_val.NoAggro = results[14]
            return_val.ShowNameBillboard = results[15]
        else:
            return_val = []
            for row in results:
                val = RailActivatorComponentTable()
                val.id = row[0]
                val.startAnim = row[1]
                val.loopAnim = row[2]
                val.stopAnim = row[3]
                val.startSound = row[4]
                val.loopSound = row[5]
                val.stopSound = row[6]
                val.effectIDs = row[7]
                val.preconditions = row[8]
                val.playerCollision = row[9]
                val.cameraLocked = row[10]
                val.StartEffectID = row[11]
                val.StopEffectID = row[12]
                val.DamageImmune = row[13]
                val.NoAggro = row[14]
                val.ShowNameBillboard = row[15]
                return_val.append(val)

        return return_val


class RarityTableTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.randmax = None
        self.rarity = None
        self.RarityTableIndex = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = RarityTableTable()
            return_val.id = results[0]
            return_val.randmax = results[1]
            return_val.rarity = results[2]
            return_val.RarityTableIndex = results[3]
        else:
            return_val = []
            for row in results:
                val = RarityTableTable()
                val.id = row[0]
                val.randmax = row[1]
                val.rarity = row[2]
                val.RarityTableIndex = row[3]
                return_val.append(val)

        return return_val


class RarityTableIndexTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.RarityTableIndex = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = RarityTableIndexTable()
            return_val.RarityTableIndex = results[0]
        else:
            return_val = []
            for row in results:
                val = RarityTableIndexTable()
                val.RarityTableIndex = row[0]
                return_val.append(val)

        return return_val


class RebuildComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.reset_time = None
        self.complete_time = None
        self.take_imagination = None
        self.interruptible = None
        self.self_activator = None
        self.custom_modules = None
        self.activityID = None
        self.post_imagination_cost = None
        self.time_before_smash = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = RebuildComponentTable()
            return_val.id = results[0]
            return_val.reset_time = results[1]
            return_val.complete_time = results[2]
            return_val.take_imagination = results[3]
            return_val.interruptible = results[4]
            return_val.self_activator = results[5]
            return_val.custom_modules = results[6]
            return_val.activityID = results[7]
            return_val.post_imagination_cost = results[8]
            return_val.time_before_smash = results[9]
        else:
            return_val = []
            for row in results:
                val = RebuildComponentTable()
                val.id = row[0]
                val.reset_time = row[1]
                val.complete_time = row[2]
                val.take_imagination = row[3]
                val.interruptible = row[4]
                val.self_activator = row[5]
                val.custom_modules = row[6]
                val.activityID = row[7]
                val.post_imagination_cost = row[8]
                val.time_before_smash = row[9]
                return_val.append(val)

        return return_val


class RebuildSectionsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.rebuildID = None
        self.objectID = None
        self.offset_x = None
        self.offset_y = None
        self.offset_z = None
        self.fall_angle_x = None
        self.fall_angle_y = None
        self.fall_angle_z = None
        self.fall_height = None
        self.requires_list = None
        self.size = None
        self.bPlaced = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = RebuildSectionsTable()
            return_val.id = results[0]
            return_val.rebuildID = results[1]
            return_val.objectID = results[2]
            return_val.offset_x = results[3]
            return_val.offset_y = results[4]
            return_val.offset_z = results[5]
            return_val.fall_angle_x = results[6]
            return_val.fall_angle_y = results[7]
            return_val.fall_angle_z = results[8]
            return_val.fall_height = results[9]
            return_val.requires_list = results[10]
            return_val.size = results[11]
            return_val.bPlaced = results[12]
        else:
            return_val = []
            for row in results:
                val = RebuildSectionsTable()
                val.id = row[0]
                val.rebuildID = row[1]
                val.objectID = row[2]
                val.offset_x = row[3]
                val.offset_y = row[4]
                val.offset_z = row[5]
                val.fall_angle_x = row[6]
                val.fall_angle_y = row[7]
                val.fall_angle_z = row[8]
                val.fall_height = row[9]
                val.requires_list = row[10]
                val.size = row[11]
                val.bPlaced = row[12]
                return_val.append(val)

        return return_val


class ReleaseVersionTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.ReleaseVersion = None
        self.ReleaseDate = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ReleaseVersionTable()
            return_val.ReleaseVersion = results[0]
            return_val.ReleaseDate = results[1]
        else:
            return_val = []
            for row in results:
                val = ReleaseVersionTable()
                val.ReleaseVersion = row[0]
                val.ReleaseDate = row[1]
                return_val.append(val)

        return return_val


class RenderComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.render_asset = None
        self.icon_asset = None
        self.IconID = None
        self.shader_id = None
        self.effect1 = None
        self.effect2 = None
        self.effect3 = None
        self.effect4 = None
        self.effect5 = None
        self.effect6 = None
        self.animationGroupIDs = None
        self.fade = None
        self.usedropshadow = None
        self.preloadAnimations = None
        self.fadeInTime = None
        self.maxShadowDistance = None
        self.ignoreCameraCollision = None
        self.renderComponentLOD1 = None
        self.renderComponentLOD2 = None
        self.gradualSnap = None
        self.animationFlag = None
        self.AudioMetaEventSet = None
        self.billboardHeight = None
        self.chatBubbleOffset = None
        self.staticBillboard = None
        self.LXFMLFolder = None
        self.attachIndicatorsToNode = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = RenderComponentTable()
            return_val.id = results[0]
            return_val.render_asset = results[1]
            return_val.icon_asset = results[2]
            return_val.IconID = results[3]
            return_val.shader_id = results[4]
            return_val.effect1 = results[5]
            return_val.effect2 = results[6]
            return_val.effect3 = results[7]
            return_val.effect4 = results[8]
            return_val.effect5 = results[9]
            return_val.effect6 = results[10]
            return_val.animationGroupIDs = results[11]
            return_val.fade = results[12]
            return_val.usedropshadow = results[13]
            return_val.preloadAnimations = results[14]
            return_val.fadeInTime = results[15]
            return_val.maxShadowDistance = results[16]
            return_val.ignoreCameraCollision = results[17]
            return_val.renderComponentLOD1 = results[18]
            return_val.renderComponentLOD2 = results[19]
            return_val.gradualSnap = results[20]
            return_val.animationFlag = results[21]
            return_val.AudioMetaEventSet = results[22]
            return_val.billboardHeight = results[23]
            return_val.chatBubbleOffset = results[24]
            return_val.staticBillboard = results[25]
            return_val.LXFMLFolder = results[26]
            return_val.attachIndicatorsToNode = results[27]
        else:
            return_val = []
            for row in results:
                val = RenderComponentTable()
                val.id = row[0]
                val.render_asset = row[1]
                val.icon_asset = row[2]
                val.IconID = row[3]
                val.shader_id = row[4]
                val.effect1 = row[5]
                val.effect2 = row[6]
                val.effect3 = row[7]
                val.effect4 = row[8]
                val.effect5 = row[9]
                val.effect6 = row[10]
                val.animationGroupIDs = row[11]
                val.fade = row[12]
                val.usedropshadow = row[13]
                val.preloadAnimations = row[14]
                val.fadeInTime = row[15]
                val.maxShadowDistance = row[16]
                val.ignoreCameraCollision = row[17]
                val.renderComponentLOD1 = row[18]
                val.renderComponentLOD2 = row[19]
                val.gradualSnap = row[20]
                val.animationFlag = row[21]
                val.AudioMetaEventSet = row[22]
                val.billboardHeight = row[23]
                val.chatBubbleOffset = row[24]
                val.staticBillboard = row[25]
                val.LXFMLFolder = row[26]
                val.attachIndicatorsToNode = row[27]
                return_val.append(val)

        return return_val


class RenderComponentFlashTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.interactive = None
        self.animated = None
        self.nodeName = None
        self.flashPath = None
        self.elementName = None
        self._uid = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = RenderComponentFlashTable()
            return_val.id = results[0]
            return_val.interactive = results[1]
            return_val.animated = results[2]
            return_val.nodeName = results[3]
            return_val.flashPath = results[4]
            return_val.elementName = results[5]
            return_val._uid = results[6]
        else:
            return_val = []
            for row in results:
                val = RenderComponentFlashTable()
                val.id = row[0]
                val.interactive = row[1]
                val.animated = row[2]
                val.nodeName = row[3]
                val.flashPath = row[4]
                val.elementName = row[5]
                val._uid = row[6]
                return_val.append(val)

        return return_val


class RenderComponentWrapperTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.defaultWrapperAsset = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = RenderComponentWrapperTable()
            return_val.id = results[0]
            return_val.defaultWrapperAsset = results[1]
        else:
            return_val = []
            for row in results:
                val = RenderComponentWrapperTable()
                val.id = row[0]
                val.defaultWrapperAsset = row[1]
                return_val.append(val)

        return return_val


class RenderIconAssetsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.icon_asset = None
        self.blank_column = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = RenderIconAssetsTable()
            return_val.id = results[0]
            return_val.icon_asset = results[1]
            return_val.blank_column = results[2]
        else:
            return_val = []
            for row in results:
                val = RenderIconAssetsTable()
                val.id = row[0]
                val.icon_asset = row[1]
                val.blank_column = row[2]
                return_val.append(val)

        return return_val


class ReputationRewardsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.repLevel = None
        self.sublevel = None
        self.reputation = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ReputationRewardsTable()
            return_val.repLevel = results[0]
            return_val.sublevel = results[1]
            return_val.reputation = results[2]
        else:
            return_val = []
            for row in results:
                val = ReputationRewardsTable()
                val.repLevel = row[0]
                val.sublevel = row[1]
                val.reputation = row[2]
                return_val.append(val)

        return return_val


class RewardCodesTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.code = None
        self.attachmentLOT = None
        self.locStatus = None
        self.gate_version = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = RewardCodesTable()
            return_val.id = results[0]
            return_val.code = results[1]
            return_val.attachmentLOT = results[2]
            return_val.locStatus = results[3]
            return_val.gate_version = results[4]
        else:
            return_val = []
            for row in results:
                val = RewardCodesTable()
                val.id = row[0]
                val.code = row[1]
                val.attachmentLOT = row[2]
                val.locStatus = row[3]
                val.gate_version = row[4]
                return_val.append(val)

        return return_val


class RewardsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.LevelID = None
        self.MissionID = None
        self.RewardType = None
        self.value = None
        self.count = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = RewardsTable()
            return_val.id = results[0]
            return_val.LevelID = results[1]
            return_val.MissionID = results[2]
            return_val.RewardType = results[3]
            return_val.value = results[4]
            return_val.count = results[5]
        else:
            return_val = []
            for row in results:
                val = RewardsTable()
                val.id = row[0]
                val.LevelID = row[1]
                val.MissionID = row[2]
                val.RewardType = row[3]
                val.value = row[4]
                val.count = row[5]
                return_val.append(val)

        return return_val


class RocketLaunchpadControlComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.targetZone = None
        self.defaultZoneID = None
        self.targetScene = None
        self.gmLevel = None
        self.playerAnimation = None
        self.rocketAnimation = None
        self.launchMusic = None
        self.useLaunchPrecondition = None
        self.useAltLandingPrecondition = None
        self.launchPrecondition = None
        self.altLandingPrecondition = None
        self.altLandingSpawnPointName = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = RocketLaunchpadControlComponentTable()
            return_val.id = results[0]
            return_val.targetZone = results[1]
            return_val.defaultZoneID = results[2]
            return_val.targetScene = results[3]
            return_val.gmLevel = results[4]
            return_val.playerAnimation = results[5]
            return_val.rocketAnimation = results[6]
            return_val.launchMusic = results[7]
            return_val.useLaunchPrecondition = results[8]
            return_val.useAltLandingPrecondition = results[9]
            return_val.launchPrecondition = results[10]
            return_val.altLandingPrecondition = results[11]
            return_val.altLandingSpawnPointName = results[12]
        else:
            return_val = []
            for row in results:
                val = RocketLaunchpadControlComponentTable()
                val.id = row[0]
                val.targetZone = row[1]
                val.defaultZoneID = row[2]
                val.targetScene = row[3]
                val.gmLevel = row[4]
                val.playerAnimation = row[5]
                val.rocketAnimation = row[6]
                val.launchMusic = row[7]
                val.useLaunchPrecondition = row[8]
                val.useAltLandingPrecondition = row[9]
                val.launchPrecondition = row[10]
                val.altLandingPrecondition = row[11]
                val.altLandingSpawnPointName = row[12]
                return_val.append(val)

        return return_val


class SceneTableTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.sceneID = None
        self.sceneName = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = SceneTableTable()
            return_val.sceneID = results[0]
            return_val.sceneName = results[1]
        else:
            return_val = []
            for row in results:
                val = SceneTableTable()
                val.sceneID = row[0]
                val.sceneName = row[1]
                return_val.append(val)

        return return_val


class ScriptComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.script_name = None
        self.client_script_name = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ScriptComponentTable()
            return_val.id = results[0]
            return_val.script_name = results[1]
            return_val.client_script_name = results[2]
        else:
            return_val = []
            for row in results:
                val = ScriptComponentTable()
                val.id = row[0]
                val.script_name = row[1]
                val.client_script_name = row[2]
                return_val.append(val)

        return return_val


class SkillBehaviorTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.skillID = None
        self.locStatus = None
        self.behaviorID = None
        self.imaginationcost = None
        self.cooldowngroup = None
        self.cooldown = None
        self.inNpcEditor = None
        self.skillIcon = None
        self.oomSkillID = None
        self.oomBehaviorEffectID = None
        self.castTypeDesc = None
        self.imBonusUI = None
        self.lifeBonusUI = None
        self.armorBonusUI = None
        self.damageUI = None
        self.hideIcon = None
        self.localize = None
        self.gate_version = None
        self.cancelType = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = SkillBehaviorTable()
            return_val.skillID = results[0]
            return_val.locStatus = results[1]
            return_val.behaviorID = results[2]
            return_val.imaginationcost = results[3]
            return_val.cooldowngroup = results[4]
            return_val.cooldown = results[5]
            return_val.inNpcEditor = results[6]
            return_val.skillIcon = results[7]
            return_val.oomSkillID = results[8]
            return_val.oomBehaviorEffectID = results[9]
            return_val.castTypeDesc = results[10]
            return_val.imBonusUI = results[11]
            return_val.lifeBonusUI = results[12]
            return_val.armorBonusUI = results[13]
            return_val.damageUI = results[14]
            return_val.hideIcon = results[15]
            return_val.localize = results[16]
            return_val.gate_version = results[17]
            return_val.cancelType = results[18]
        else:
            return_val = []
            for row in results:
                val = SkillBehaviorTable()
                val.skillID = row[0]
                val.locStatus = row[1]
                val.behaviorID = row[2]
                val.imaginationcost = row[3]
                val.cooldowngroup = row[4]
                val.cooldown = row[5]
                val.inNpcEditor = row[6]
                val.skillIcon = row[7]
                val.oomSkillID = row[8]
                val.oomBehaviorEffectID = row[9]
                val.castTypeDesc = row[10]
                val.imBonusUI = row[11]
                val.lifeBonusUI = row[12]
                val.armorBonusUI = row[13]
                val.damageUI = row[14]
                val.hideIcon = row[15]
                val.localize = row[16]
                val.gate_version = row[17]
                val.cancelType = row[18]
                return_val.append(val)

        return return_val


class SmashableChainTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.chainIndex = None
        self.chainLevel = None
        self.lootMatrixID = None
        self.rarityTableIndex = None
        self.currencyIndex = None
        self.currencyLevel = None
        self.smashCount = None
        self.timeLimit = None
        self.chainStepID = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = SmashableChainTable()
            return_val.chainIndex = results[0]
            return_val.chainLevel = results[1]
            return_val.lootMatrixID = results[2]
            return_val.rarityTableIndex = results[3]
            return_val.currencyIndex = results[4]
            return_val.currencyLevel = results[5]
            return_val.smashCount = results[6]
            return_val.timeLimit = results[7]
            return_val.chainStepID = results[8]
        else:
            return_val = []
            for row in results:
                val = SmashableChainTable()
                val.chainIndex = row[0]
                val.chainLevel = row[1]
                val.lootMatrixID = row[2]
                val.rarityTableIndex = row[3]
                val.currencyIndex = row[4]
                val.currencyLevel = row[5]
                val.smashCount = row[6]
                val.timeLimit = row[7]
                val.chainStepID = row[8]
                return_val.append(val)

        return return_val


class SmashableChainIndexTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.targetGroup = None
        self.description = None
        self.continuous = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = SmashableChainIndexTable()
            return_val.id = results[0]
            return_val.targetGroup = results[1]
            return_val.description = results[2]
            return_val.continuous = results[3]
        else:
            return_val = []
            for row in results:
                val = SmashableChainIndexTable()
                val.id = row[0]
                val.targetGroup = row[1]
                val.description = row[2]
                val.continuous = row[3]
                return_val.append(val)

        return return_val


class SmashableComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.LootMatrixIndex = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = SmashableComponentTable()
            return_val.id = results[0]
            return_val.LootMatrixIndex = results[1]
        else:
            return_val = []
            for row in results:
                val = SmashableComponentTable()
                val.id = row[0]
                val.LootMatrixIndex = row[1]
                return_val.append(val)

        return return_val


class SmashableElementsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.elementID = None
        self.dropWeight = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = SmashableElementsTable()
            return_val.elementID = results[0]
            return_val.dropWeight = results[1]
        else:
            return_val = []
            for row in results:
                val = SmashableElementsTable()
                val.elementID = row[0]
                val.dropWeight = row[1]
                return_val.append(val)

        return return_val


class SpeedchatMenuTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.parentId = None
        self.emoteId = None
        self.imageName = None
        self.localize = None
        self.locStatus = None
        self.gate_version = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = SpeedchatMenuTable()
            return_val.id = results[0]
            return_val.parentId = results[1]
            return_val.emoteId = results[2]
            return_val.imageName = results[3]
            return_val.localize = results[4]
            return_val.locStatus = results[5]
            return_val.gate_version = results[6]
        else:
            return_val = []
            for row in results:
                val = SpeedchatMenuTable()
                val.id = row[0]
                val.parentId = row[1]
                val.emoteId = row[2]
                val.imageName = row[3]
                val.localize = row[4]
                val.locStatus = row[5]
                val.gate_version = row[6]
                return_val.append(val)

        return return_val


class SubscriptionPricingTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.countryCode = None
        self.monthlyFeeGold = None
        self.monthlyFeeSilver = None
        self.monthlyFeeBronze = None
        self.monetarySymbol = None
        self.symbolIsAppended = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = SubscriptionPricingTable()
            return_val.id = results[0]
            return_val.countryCode = results[1]
            return_val.monthlyFeeGold = results[2]
            return_val.monthlyFeeSilver = results[3]
            return_val.monthlyFeeBronze = results[4]
            return_val.monetarySymbol = results[5]
            return_val.symbolIsAppended = results[6]
        else:
            return_val = []
            for row in results:
                val = SubscriptionPricingTable()
                val.id = row[0]
                val.countryCode = row[1]
                val.monthlyFeeGold = row[2]
                val.monthlyFeeSilver = row[3]
                val.monthlyFeeBronze = row[4]
                val.monetarySymbol = row[5]
                val.symbolIsAppended = row[6]
                return_val.append(val)

        return return_val


class SurfaceTypeTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.SurfaceType = None
        self.FootstepNDAudioMetaEventSetName = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = SurfaceTypeTable()
            return_val.SurfaceType = results[0]
            return_val.FootstepNDAudioMetaEventSetName = results[1]
        else:
            return_val = []
            for row in results:
                val = SurfaceTypeTable()
                val.SurfaceType = row[0]
                val.FootstepNDAudioMetaEventSetName = row[1]
                return_val.append(val)

        return return_val


class TamingBuildPuzzlesTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.PuzzleModelLot = None
        self.NPCLot = None
        self.ValidPiecesLXF = None
        self.InvalidPiecesLXF = None
        self.Difficulty = None
        self.Timelimit = None
        self.NumValidPieces = None
        self.TotalNumPieces = None
        self.ModelName = None
        self.FullModelLXF = None
        self.Duration = None
        self.imagCostPerBuild = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = TamingBuildPuzzlesTable()
            return_val.id = results[0]
            return_val.PuzzleModelLot = results[1]
            return_val.NPCLot = results[2]
            return_val.ValidPiecesLXF = results[3]
            return_val.InvalidPiecesLXF = results[4]
            return_val.Difficulty = results[5]
            return_val.Timelimit = results[6]
            return_val.NumValidPieces = results[7]
            return_val.TotalNumPieces = results[8]
            return_val.ModelName = results[9]
            return_val.FullModelLXF = results[10]
            return_val.Duration = results[11]
            return_val.imagCostPerBuild = results[12]
        else:
            return_val = []
            for row in results:
                val = TamingBuildPuzzlesTable()
                val.id = row[0]
                val.PuzzleModelLot = row[1]
                val.NPCLot = row[2]
                val.ValidPiecesLXF = row[3]
                val.InvalidPiecesLXF = row[4]
                val.Difficulty = row[5]
                val.Timelimit = row[6]
                val.NumValidPieces = row[7]
                val.TotalNumPieces = row[8]
                val.ModelName = row[9]
                val.FullModelLXF = row[10]
                val.Duration = row[11]
                val.imagCostPerBuild = row[12]
                return_val.append(val)

        return return_val


class TextDescriptionTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.TextID = None
        self.TestDescription = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = TextDescriptionTable()
            return_val.TextID = results[0]
            return_val.TestDescription = results[1]
        else:
            return_val = []
            for row in results:
                val = TextDescriptionTable()
                val.TextID = row[0]
                val.TestDescription = row[1]
                return_val.append(val)

        return return_val


class TextLanguageTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.TextID = None
        self.LanguageID = None
        self.Text = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = TextLanguageTable()
            return_val.TextID = results[0]
            return_val.LanguageID = results[1]
            return_val.Text = results[2]
        else:
            return_val = []
            for row in results:
                val = TextLanguageTable()
                val.TextID = row[0]
                val.LanguageID = row[1]
                val.Text = row[2]
                return_val.append(val)

        return return_val


class TrailEffectsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.trailID = None
        self.textureName = None
        self.blendmode = None
        self.cardlifetime = None
        self.colorlifetime = None
        self.minTailFade = None
        self.tailFade = None
        self.max_particles = None
        self.birthDelay = None
        self.deathDelay = None
        self.bone1 = None
        self.bone2 = None
        self.texLength = None
        self.texWidth = None
        self.startColorR = None
        self.startColorG = None
        self.startColorB = None
        self.startColorA = None
        self.middleColorR = None
        self.middleColorG = None
        self.middleColorB = None
        self.middleColorA = None
        self.endColorR = None
        self.endColorG = None
        self.endColorB = None
        self.endColorA = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = TrailEffectsTable()
            return_val.trailID = results[0]
            return_val.textureName = results[1]
            return_val.blendmode = results[2]
            return_val.cardlifetime = results[3]
            return_val.colorlifetime = results[4]
            return_val.minTailFade = results[5]
            return_val.tailFade = results[6]
            return_val.max_particles = results[7]
            return_val.birthDelay = results[8]
            return_val.deathDelay = results[9]
            return_val.bone1 = results[10]
            return_val.bone2 = results[11]
            return_val.texLength = results[12]
            return_val.texWidth = results[13]
            return_val.startColorR = results[14]
            return_val.startColorG = results[15]
            return_val.startColorB = results[16]
            return_val.startColorA = results[17]
            return_val.middleColorR = results[18]
            return_val.middleColorG = results[19]
            return_val.middleColorB = results[20]
            return_val.middleColorA = results[21]
            return_val.endColorR = results[22]
            return_val.endColorG = results[23]
            return_val.endColorB = results[24]
            return_val.endColorA = results[25]
        else:
            return_val = []
            for row in results:
                val = TrailEffectsTable()
                val.trailID = row[0]
                val.textureName = row[1]
                val.blendmode = row[2]
                val.cardlifetime = row[3]
                val.colorlifetime = row[4]
                val.minTailFade = row[5]
                val.tailFade = row[6]
                val.max_particles = row[7]
                val.birthDelay = row[8]
                val.deathDelay = row[9]
                val.bone1 = row[10]
                val.bone2 = row[11]
                val.texLength = row[12]
                val.texWidth = row[13]
                val.startColorR = row[14]
                val.startColorG = row[15]
                val.startColorB = row[16]
                val.startColorA = row[17]
                val.middleColorR = row[18]
                val.middleColorG = row[19]
                val.middleColorB = row[20]
                val.middleColorA = row[21]
                val.endColorR = row[22]
                val.endColorG = row[23]
                val.endColorB = row[24]
                val.endColorA = row[25]
                return_val.append(val)

        return return_val


class UGBehaviorSoundsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.guid = None
        self.localize = None
        self.locStatus = None
        self.gate_version = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = UGBehaviorSoundsTable()
            return_val.id = results[0]
            return_val.guid = results[1]
            return_val.localize = results[2]
            return_val.locStatus = results[3]
            return_val.gate_version = results[4]
        else:
            return_val = []
            for row in results:
                val = UGBehaviorSoundsTable()
                val.id = row[0]
                val.guid = row[1]
                val.localize = row[2]
                val.locStatus = row[3]
                val.gate_version = row[4]
                return_val.append(val)

        return return_val


class VehiclePhysicsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.hkxFilename = None
        self.fGravityScale = None
        self.fMass = None
        self.fChassisFriction = None
        self.fMaxSpeed = None
        self.fEngineTorque = None
        self.fBrakeFrontTorque = None
        self.fBrakeRearTorque = None
        self.fBrakeMinInputToBlock = None
        self.fBrakeMinTimeToBlock = None
        self.fSteeringMaxAngle = None
        self.fSteeringSpeedLimitForMaxAngle = None
        self.fSteeringMinAngle = None
        self.fFwdBias = None
        self.fFrontTireFriction = None
        self.fRearTireFriction = None
        self.fFrontTireFrictionSlide = None
        self.fRearTireFrictionSlide = None
        self.fFrontTireSlipAngle = None
        self.fRearTireSlipAngle = None
        self.fWheelWidth = None
        self.fWheelRadius = None
        self.fWheelMass = None
        self.fReorientPitchStrength = None
        self.fReorientRollStrength = None
        self.fSuspensionLength = None
        self.fSuspensionStrength = None
        self.fSuspensionDampingCompression = None
        self.fSuspensionDampingRelaxation = None
        self.iChassisCollisionGroup = None
        self.fNormalSpinDamping = None
        self.fCollisionSpinDamping = None
        self.fCollisionThreshold = None
        self.fTorqueRollFactor = None
        self.fTorquePitchFactor = None
        self.fTorqueYawFactor = None
        self.fInertiaRoll = None
        self.fInertiaPitch = None
        self.fInertiaYaw = None
        self.fExtraTorqueFactor = None
        self.fCenterOfMassFwd = None
        self.fCenterOfMassUp = None
        self.fCenterOfMassRight = None
        self.fWheelHardpointFrontFwd = None
        self.fWheelHardpointFrontUp = None
        self.fWheelHardpointFrontRight = None
        self.fWheelHardpointRearFwd = None
        self.fWheelHardpointRearUp = None
        self.fWheelHardpointRearRight = None
        self.fInputTurnSpeed = None
        self.fInputDeadTurnBackSpeed = None
        self.fInputAccelSpeed = None
        self.fInputDeadAccelDownSpeed = None
        self.fInputDecelSpeed = None
        self.fInputDeadDecelDownSpeed = None
        self.fInputSlopeChangePointX = None
        self.fInputInitialSlope = None
        self.fInputDeadZone = None
        self.fAeroAirDensity = None
        self.fAeroFrontalArea = None
        self.fAeroDragCoefficient = None
        self.fAeroLiftCoefficient = None
        self.fAeroExtraGravity = None
        self.fBoostTopSpeed = None
        self.fBoostCostPerSecond = None
        self.fBoostAccelerateChange = None
        self.fBoostDampingChange = None
        self.fPowerslideNeutralAngle = None
        self.fPowerslideTorqueStrength = None
        self.iPowerslideNumTorqueApplications = None
        self.fImaginationTankSize = None
        self.fSkillCost = None
        self.fWreckSpeedBase = None
        self.fWreckSpeedPercent = None
        self.fWreckMinAngle = None
        self.AudioEventEngine = None
        self.AudioEventSkid = None
        self.AudioEventLightHit = None
        self.AudioSpeedThresholdLightHit = None
        self.AudioTimeoutLightHit = None
        self.AudioEventHeavyHit = None
        self.AudioSpeedThresholdHeavyHit = None
        self.AudioTimeoutHeavyHit = None
        self.AudioEventStart = None
        self.AudioEventTreadConcrete = None
        self.AudioEventTreadSand = None
        self.AudioEventTreadWood = None
        self.AudioEventTreadDirt = None
        self.AudioEventTreadPlastic = None
        self.AudioEventTreadGrass = None
        self.AudioEventTreadGravel = None
        self.AudioEventTreadMud = None
        self.AudioEventTreadWater = None
        self.AudioEventTreadSnow = None
        self.AudioEventTreadIce = None
        self.AudioEventTreadMetal = None
        self.AudioEventTreadLeaves = None
        self.AudioEventLightLand = None
        self.AudioAirtimeForLightLand = None
        self.AudioEventHeavyLand = None
        self.AudioAirtimeForHeavyLand = None
        self.bWheelsVisible = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = VehiclePhysicsTable()
            return_val.id = results[0]
            return_val.hkxFilename = results[1]
            return_val.fGravityScale = results[2]
            return_val.fMass = results[3]
            return_val.fChassisFriction = results[4]
            return_val.fMaxSpeed = results[5]
            return_val.fEngineTorque = results[6]
            return_val.fBrakeFrontTorque = results[7]
            return_val.fBrakeRearTorque = results[8]
            return_val.fBrakeMinInputToBlock = results[9]
            return_val.fBrakeMinTimeToBlock = results[10]
            return_val.fSteeringMaxAngle = results[11]
            return_val.fSteeringSpeedLimitForMaxAngle = results[12]
            return_val.fSteeringMinAngle = results[13]
            return_val.fFwdBias = results[14]
            return_val.fFrontTireFriction = results[15]
            return_val.fRearTireFriction = results[16]
            return_val.fFrontTireFrictionSlide = results[17]
            return_val.fRearTireFrictionSlide = results[18]
            return_val.fFrontTireSlipAngle = results[19]
            return_val.fRearTireSlipAngle = results[20]
            return_val.fWheelWidth = results[21]
            return_val.fWheelRadius = results[22]
            return_val.fWheelMass = results[23]
            return_val.fReorientPitchStrength = results[24]
            return_val.fReorientRollStrength = results[25]
            return_val.fSuspensionLength = results[26]
            return_val.fSuspensionStrength = results[27]
            return_val.fSuspensionDampingCompression = results[28]
            return_val.fSuspensionDampingRelaxation = results[29]
            return_val.iChassisCollisionGroup = results[30]
            return_val.fNormalSpinDamping = results[31]
            return_val.fCollisionSpinDamping = results[32]
            return_val.fCollisionThreshold = results[33]
            return_val.fTorqueRollFactor = results[34]
            return_val.fTorquePitchFactor = results[35]
            return_val.fTorqueYawFactor = results[36]
            return_val.fInertiaRoll = results[37]
            return_val.fInertiaPitch = results[38]
            return_val.fInertiaYaw = results[39]
            return_val.fExtraTorqueFactor = results[40]
            return_val.fCenterOfMassFwd = results[41]
            return_val.fCenterOfMassUp = results[42]
            return_val.fCenterOfMassRight = results[43]
            return_val.fWheelHardpointFrontFwd = results[44]
            return_val.fWheelHardpointFrontUp = results[45]
            return_val.fWheelHardpointFrontRight = results[46]
            return_val.fWheelHardpointRearFwd = results[47]
            return_val.fWheelHardpointRearUp = results[48]
            return_val.fWheelHardpointRearRight = results[49]
            return_val.fInputTurnSpeed = results[50]
            return_val.fInputDeadTurnBackSpeed = results[51]
            return_val.fInputAccelSpeed = results[52]
            return_val.fInputDeadAccelDownSpeed = results[53]
            return_val.fInputDecelSpeed = results[54]
            return_val.fInputDeadDecelDownSpeed = results[55]
            return_val.fInputSlopeChangePointX = results[56]
            return_val.fInputInitialSlope = results[57]
            return_val.fInputDeadZone = results[58]
            return_val.fAeroAirDensity = results[59]
            return_val.fAeroFrontalArea = results[60]
            return_val.fAeroDragCoefficient = results[61]
            return_val.fAeroLiftCoefficient = results[62]
            return_val.fAeroExtraGravity = results[63]
            return_val.fBoostTopSpeed = results[64]
            return_val.fBoostCostPerSecond = results[65]
            return_val.fBoostAccelerateChange = results[66]
            return_val.fBoostDampingChange = results[67]
            return_val.fPowerslideNeutralAngle = results[68]
            return_val.fPowerslideTorqueStrength = results[69]
            return_val.iPowerslideNumTorqueApplications = results[70]
            return_val.fImaginationTankSize = results[71]
            return_val.fSkillCost = results[72]
            return_val.fWreckSpeedBase = results[73]
            return_val.fWreckSpeedPercent = results[74]
            return_val.fWreckMinAngle = results[75]
            return_val.AudioEventEngine = results[76]
            return_val.AudioEventSkid = results[77]
            return_val.AudioEventLightHit = results[78]
            return_val.AudioSpeedThresholdLightHit = results[79]
            return_val.AudioTimeoutLightHit = results[80]
            return_val.AudioEventHeavyHit = results[81]
            return_val.AudioSpeedThresholdHeavyHit = results[82]
            return_val.AudioTimeoutHeavyHit = results[83]
            return_val.AudioEventStart = results[84]
            return_val.AudioEventTreadConcrete = results[85]
            return_val.AudioEventTreadSand = results[86]
            return_val.AudioEventTreadWood = results[87]
            return_val.AudioEventTreadDirt = results[88]
            return_val.AudioEventTreadPlastic = results[89]
            return_val.AudioEventTreadGrass = results[90]
            return_val.AudioEventTreadGravel = results[91]
            return_val.AudioEventTreadMud = results[92]
            return_val.AudioEventTreadWater = results[93]
            return_val.AudioEventTreadSnow = results[94]
            return_val.AudioEventTreadIce = results[95]
            return_val.AudioEventTreadMetal = results[96]
            return_val.AudioEventTreadLeaves = results[97]
            return_val.AudioEventLightLand = results[98]
            return_val.AudioAirtimeForLightLand = results[99]
            return_val.AudioEventHeavyLand = results[100]
            return_val.AudioAirtimeForHeavyLand = results[101]
            return_val.bWheelsVisible = results[102]
        else:
            return_val = []
            for row in results:
                val = VehiclePhysicsTable()
                val.id = row[0]
                val.hkxFilename = row[1]
                val.fGravityScale = row[2]
                val.fMass = row[3]
                val.fChassisFriction = row[4]
                val.fMaxSpeed = row[5]
                val.fEngineTorque = row[6]
                val.fBrakeFrontTorque = row[7]
                val.fBrakeRearTorque = row[8]
                val.fBrakeMinInputToBlock = row[9]
                val.fBrakeMinTimeToBlock = row[10]
                val.fSteeringMaxAngle = row[11]
                val.fSteeringSpeedLimitForMaxAngle = row[12]
                val.fSteeringMinAngle = row[13]
                val.fFwdBias = row[14]
                val.fFrontTireFriction = row[15]
                val.fRearTireFriction = row[16]
                val.fFrontTireFrictionSlide = row[17]
                val.fRearTireFrictionSlide = row[18]
                val.fFrontTireSlipAngle = row[19]
                val.fRearTireSlipAngle = row[20]
                val.fWheelWidth = row[21]
                val.fWheelRadius = row[22]
                val.fWheelMass = row[23]
                val.fReorientPitchStrength = row[24]
                val.fReorientRollStrength = row[25]
                val.fSuspensionLength = row[26]
                val.fSuspensionStrength = row[27]
                val.fSuspensionDampingCompression = row[28]
                val.fSuspensionDampingRelaxation = row[29]
                val.iChassisCollisionGroup = row[30]
                val.fNormalSpinDamping = row[31]
                val.fCollisionSpinDamping = row[32]
                val.fCollisionThreshold = row[33]
                val.fTorqueRollFactor = row[34]
                val.fTorquePitchFactor = row[35]
                val.fTorqueYawFactor = row[36]
                val.fInertiaRoll = row[37]
                val.fInertiaPitch = row[38]
                val.fInertiaYaw = row[39]
                val.fExtraTorqueFactor = row[40]
                val.fCenterOfMassFwd = row[41]
                val.fCenterOfMassUp = row[42]
                val.fCenterOfMassRight = row[43]
                val.fWheelHardpointFrontFwd = row[44]
                val.fWheelHardpointFrontUp = row[45]
                val.fWheelHardpointFrontRight = row[46]
                val.fWheelHardpointRearFwd = row[47]
                val.fWheelHardpointRearUp = row[48]
                val.fWheelHardpointRearRight = row[49]
                val.fInputTurnSpeed = row[50]
                val.fInputDeadTurnBackSpeed = row[51]
                val.fInputAccelSpeed = row[52]
                val.fInputDeadAccelDownSpeed = row[53]
                val.fInputDecelSpeed = row[54]
                val.fInputDeadDecelDownSpeed = row[55]
                val.fInputSlopeChangePointX = row[56]
                val.fInputInitialSlope = row[57]
                val.fInputDeadZone = row[58]
                val.fAeroAirDensity = row[59]
                val.fAeroFrontalArea = row[60]
                val.fAeroDragCoefficient = row[61]
                val.fAeroLiftCoefficient = row[62]
                val.fAeroExtraGravity = row[63]
                val.fBoostTopSpeed = row[64]
                val.fBoostCostPerSecond = row[65]
                val.fBoostAccelerateChange = row[66]
                val.fBoostDampingChange = row[67]
                val.fPowerslideNeutralAngle = row[68]
                val.fPowerslideTorqueStrength = row[69]
                val.iPowerslideNumTorqueApplications = row[70]
                val.fImaginationTankSize = row[71]
                val.fSkillCost = row[72]
                val.fWreckSpeedBase = row[73]
                val.fWreckSpeedPercent = row[74]
                val.fWreckMinAngle = row[75]
                val.AudioEventEngine = row[76]
                val.AudioEventSkid = row[77]
                val.AudioEventLightHit = row[78]
                val.AudioSpeedThresholdLightHit = row[79]
                val.AudioTimeoutLightHit = row[80]
                val.AudioEventHeavyHit = row[81]
                val.AudioSpeedThresholdHeavyHit = row[82]
                val.AudioTimeoutHeavyHit = row[83]
                val.AudioEventStart = row[84]
                val.AudioEventTreadConcrete = row[85]
                val.AudioEventTreadSand = row[86]
                val.AudioEventTreadWood = row[87]
                val.AudioEventTreadDirt = row[88]
                val.AudioEventTreadPlastic = row[89]
                val.AudioEventTreadGrass = row[90]
                val.AudioEventTreadGravel = row[91]
                val.AudioEventTreadMud = row[92]
                val.AudioEventTreadWater = row[93]
                val.AudioEventTreadSnow = row[94]
                val.AudioEventTreadIce = row[95]
                val.AudioEventTreadMetal = row[96]
                val.AudioEventTreadLeaves = row[97]
                val.AudioEventLightLand = row[98]
                val.AudioAirtimeForLightLand = row[99]
                val.AudioEventHeavyLand = row[100]
                val.AudioAirtimeForHeavyLand = row[101]
                val.bWheelsVisible = row[102]
                return_val.append(val)

        return return_val


class VehicleStatMapTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.ModuleStat = None
        self.HavokStat = None
        self.HavokChangePerModuleStat = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = VehicleStatMapTable()
            return_val.id = results[0]
            return_val.ModuleStat = results[1]
            return_val.HavokStat = results[2]
            return_val.HavokChangePerModuleStat = results[3]
        else:
            return_val = []
            for row in results:
                val = VehicleStatMapTable()
                val.id = row[0]
                val.ModuleStat = row[1]
                val.HavokStat = row[2]
                val.HavokChangePerModuleStat = row[3]
                return_val.append(val)

        return return_val


class VendorComponentTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.buyScalar = None
        self.sellScalar = None
        self.refreshTimeSeconds = None
        self.LootMatrixIndex = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = VendorComponentTable()
            return_val.id = results[0]
            return_val.buyScalar = results[1]
            return_val.sellScalar = results[2]
            return_val.refreshTimeSeconds = results[3]
            return_val.LootMatrixIndex = results[4]
        else:
            return_val = []
            for row in results:
                val = VendorComponentTable()
                val.id = row[0]
                val.buyScalar = row[1]
                val.sellScalar = row[2]
                val.refreshTimeSeconds = row[3]
                val.LootMatrixIndex = row[4]
                return_val.append(val)

        return return_val


class WhatsCoolItemSpotlightTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.itemID = None
        self.localize = None
        self.gate_version = None
        self.locStatus = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = WhatsCoolItemSpotlightTable()
            return_val.id = results[0]
            return_val.itemID = results[1]
            return_val.localize = results[2]
            return_val.gate_version = results[3]
            return_val.locStatus = results[4]
        else:
            return_val = []
            for row in results:
                val = WhatsCoolItemSpotlightTable()
                val.id = row[0]
                val.itemID = row[1]
                val.localize = row[2]
                val.gate_version = row[3]
                val.locStatus = row[4]
                return_val.append(val)

        return return_val


class WhatsCoolNewsAndTipsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.iconID = None
        self.type = None
        self.localize = None
        self.gate_version = None
        self.locStatus = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = WhatsCoolNewsAndTipsTable()
            return_val.id = results[0]
            return_val.iconID = results[1]
            return_val.type = results[2]
            return_val.localize = results[3]
            return_val.gate_version = results[4]
            return_val.locStatus = results[5]
        else:
            return_val = []
            for row in results:
                val = WhatsCoolNewsAndTipsTable()
                val.id = row[0]
                val.iconID = row[1]
                val.type = row[2]
                val.localize = row[3]
                val.gate_version = row[4]
                val.locStatus = row[5]
                return_val.append(val)

        return return_val


class WorldConfigTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.WorldConfigID = None
        self.pegravityvalue = None
        self.pebroadphaseworldsize = None
        self.pegameobjscalefactor = None
        self.character_rotation_speed = None
        self.character_walk_forward_speed = None
        self.character_walk_backward_speed = None
        self.character_walk_strafe_speed = None
        self.character_walk_strafe_forward_speed = None
        self.character_walk_strafe_backward_speed = None
        self.character_run_backward_speed = None
        self.character_run_strafe_speed = None
        self.character_run_strafe_forward_speed = None
        self.character_run_strafe_backward_speed = None
        self.global_cooldown = None
        self.characterGroundedTime = None
        self.characterGroundedSpeed = None
        self.globalImmunityTime = None
        self.character_max_slope = None
        self.defaultrespawntime = None
        self.mission_tooltip_timeout = None
        self.vendor_buy_multiplier = None
        self.pet_follow_radius = None
        self.character_eye_height = None
        self.flight_vertical_velocity = None
        self.flight_airspeed = None
        self.flight_fuel_ratio = None
        self.flight_max_airspeed = None
        self.fReputationPerVote = None
        self.nPropertyCloneLimit = None
        self.defaultHomespaceTemplate = None
        self.coins_lost_on_death_percent = None
        self.coins_lost_on_death_min = None
        self.coins_lost_on_death_max = None
        self.character_votes_per_day = None
        self.property_moderation_request_approval_cost = None
        self.property_moderation_request_review_cost = None
        self.propertyModRequestsAllowedSpike = None
        self.propertyModRequestsAllowedInterval = None
        self.propertyModRequestsAllowedTotal = None
        self.propertyModRequestsSpikeDuration = None
        self.propertyModRequestsIntervalDuration = None
        self.modelModerateOnCreate = None
        self.defaultPropertyMaxHeight = None
        self.reputationPerVoteCast = None
        self.reputationPerVoteReceived = None
        self.showcaseTopModelConsiderationBattles = None
        self.reputationPerBattlePromotion = None
        self.coins_lost_on_death_min_timeout = None
        self.coins_lost_on_death_max_timeout = None
        self.mail_base_fee = None
        self.mail_percent_attachment_fee = None
        self.propertyReputationDelay = None
        self.LevelCap = None
        self.LevelUpBehaviorEffect = None
        self.CharacterVersion = None
        self.LevelCapCurrencyConversion = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = WorldConfigTable()
            return_val.WorldConfigID = results[0]
            return_val.pegravityvalue = results[1]
            return_val.pebroadphaseworldsize = results[2]
            return_val.pegameobjscalefactor = results[3]
            return_val.character_rotation_speed = results[4]
            return_val.character_walk_forward_speed = results[5]
            return_val.character_walk_backward_speed = results[6]
            return_val.character_walk_strafe_speed = results[7]
            return_val.character_walk_strafe_forward_speed = results[8]
            return_val.character_walk_strafe_backward_speed = results[9]
            return_val.character_run_backward_speed = results[10]
            return_val.character_run_strafe_speed = results[11]
            return_val.character_run_strafe_forward_speed = results[12]
            return_val.character_run_strafe_backward_speed = results[13]
            return_val.global_cooldown = results[14]
            return_val.characterGroundedTime = results[15]
            return_val.characterGroundedSpeed = results[16]
            return_val.globalImmunityTime = results[17]
            return_val.character_max_slope = results[18]
            return_val.defaultrespawntime = results[19]
            return_val.mission_tooltip_timeout = results[20]
            return_val.vendor_buy_multiplier = results[21]
            return_val.pet_follow_radius = results[22]
            return_val.character_eye_height = results[23]
            return_val.flight_vertical_velocity = results[24]
            return_val.flight_airspeed = results[25]
            return_val.flight_fuel_ratio = results[26]
            return_val.flight_max_airspeed = results[27]
            return_val.fReputationPerVote = results[28]
            return_val.nPropertyCloneLimit = results[29]
            return_val.defaultHomespaceTemplate = results[30]
            return_val.coins_lost_on_death_percent = results[31]
            return_val.coins_lost_on_death_min = results[32]
            return_val.coins_lost_on_death_max = results[33]
            return_val.character_votes_per_day = results[34]
            return_val.property_moderation_request_approval_cost = results[35]
            return_val.property_moderation_request_review_cost = results[36]
            return_val.propertyModRequestsAllowedSpike = results[37]
            return_val.propertyModRequestsAllowedInterval = results[38]
            return_val.propertyModRequestsAllowedTotal = results[39]
            return_val.propertyModRequestsSpikeDuration = results[40]
            return_val.propertyModRequestsIntervalDuration = results[41]
            return_val.modelModerateOnCreate = results[42]
            return_val.defaultPropertyMaxHeight = results[43]
            return_val.reputationPerVoteCast = results[44]
            return_val.reputationPerVoteReceived = results[45]
            return_val.showcaseTopModelConsiderationBattles = results[46]
            return_val.reputationPerBattlePromotion = results[47]
            return_val.coins_lost_on_death_min_timeout = results[48]
            return_val.coins_lost_on_death_max_timeout = results[49]
            return_val.mail_base_fee = results[50]
            return_val.mail_percent_attachment_fee = results[51]
            return_val.propertyReputationDelay = results[52]
            return_val.LevelCap = results[53]
            return_val.LevelUpBehaviorEffect = results[54]
            return_val.CharacterVersion = results[55]
            return_val.LevelCapCurrencyConversion = results[56]
        else:
            return_val = []
            for row in results:
                val = WorldConfigTable()
                val.WorldConfigID = row[0]
                val.pegravityvalue = row[1]
                val.pebroadphaseworldsize = row[2]
                val.pegameobjscalefactor = row[3]
                val.character_rotation_speed = row[4]
                val.character_walk_forward_speed = row[5]
                val.character_walk_backward_speed = row[6]
                val.character_walk_strafe_speed = row[7]
                val.character_walk_strafe_forward_speed = row[8]
                val.character_walk_strafe_backward_speed = row[9]
                val.character_run_backward_speed = row[10]
                val.character_run_strafe_speed = row[11]
                val.character_run_strafe_forward_speed = row[12]
                val.character_run_strafe_backward_speed = row[13]
                val.global_cooldown = row[14]
                val.characterGroundedTime = row[15]
                val.characterGroundedSpeed = row[16]
                val.globalImmunityTime = row[17]
                val.character_max_slope = row[18]
                val.defaultrespawntime = row[19]
                val.mission_tooltip_timeout = row[20]
                val.vendor_buy_multiplier = row[21]
                val.pet_follow_radius = row[22]
                val.character_eye_height = row[23]
                val.flight_vertical_velocity = row[24]
                val.flight_airspeed = row[25]
                val.flight_fuel_ratio = row[26]
                val.flight_max_airspeed = row[27]
                val.fReputationPerVote = row[28]
                val.nPropertyCloneLimit = row[29]
                val.defaultHomespaceTemplate = row[30]
                val.coins_lost_on_death_percent = row[31]
                val.coins_lost_on_death_min = row[32]
                val.coins_lost_on_death_max = row[33]
                val.character_votes_per_day = row[34]
                val.property_moderation_request_approval_cost = row[35]
                val.property_moderation_request_review_cost = row[36]
                val.propertyModRequestsAllowedSpike = row[37]
                val.propertyModRequestsAllowedInterval = row[38]
                val.propertyModRequestsAllowedTotal = row[39]
                val.propertyModRequestsSpikeDuration = row[40]
                val.propertyModRequestsIntervalDuration = row[41]
                val.modelModerateOnCreate = row[42]
                val.defaultPropertyMaxHeight = row[43]
                val.reputationPerVoteCast = row[44]
                val.reputationPerVoteReceived = row[45]
                val.showcaseTopModelConsiderationBattles = row[46]
                val.reputationPerBattlePromotion = row[47]
                val.coins_lost_on_death_min_timeout = row[48]
                val.coins_lost_on_death_max_timeout = row[49]
                val.mail_base_fee = row[50]
                val.mail_percent_attachment_fee = row[51]
                val.propertyReputationDelay = row[52]
                val.LevelCap = row[53]
                val.LevelUpBehaviorEffect = row[54]
                val.CharacterVersion = row[55]
                val.LevelCapCurrencyConversion = row[56]
                return_val.append(val)

        return return_val


class ZoneLoadingTipsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.zoneid = None
        self.imagelocation = None
        self.localize = None
        self.gate_version = None
        self.locStatus = None
        self.weight = None
        self.targetVersion = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ZoneLoadingTipsTable()
            return_val.id = results[0]
            return_val.zoneid = results[1]
            return_val.imagelocation = results[2]
            return_val.localize = results[3]
            return_val.gate_version = results[4]
            return_val.locStatus = results[5]
            return_val.weight = results[6]
            return_val.targetVersion = results[7]
        else:
            return_val = []
            for row in results:
                val = ZoneLoadingTipsTable()
                val.id = row[0]
                val.zoneid = row[1]
                val.imagelocation = row[2]
                val.localize = row[3]
                val.gate_version = row[4]
                val.locStatus = row[5]
                val.weight = row[6]
                val.targetVersion = row[7]
                return_val.append(val)

        return return_val


class ZoneSummaryTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.zoneID = None
        self.type = None
        self.value = None
        self._uniqueID = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ZoneSummaryTable()
            return_val.zoneID = results[0]
            return_val.type = results[1]
            return_val.value = results[2]
            return_val._uniqueID = results[3]
        else:
            return_val = []
            for row in results:
                val = ZoneSummaryTable()
                val.zoneID = row[0]
                val.type = row[1]
                val.value = row[2]
                val._uniqueID = row[3]
                return_val.append(val)

        return return_val


class ZoneTableTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.zoneID = None
        self.locStatus = None
        self.zoneName = None
        self.scriptID = None
        self.ghostdistance_min = None
        self.ghostdistance = None
        self.population_soft_cap = None
        self.population_hard_cap = None
        self.DisplayDescription = None
        self.mapFolder = None
        self.smashableMinDistance = None
        self.smashableMaxDistance = None
        self.mixerProgram = None
        self.clientPhysicsFramerate = None
        self.serverPhysicsFramerate = None
        self.zoneControlTemplate = None
        self.widthInChunks = None
        self.heightInChunks = None
        self.petsAllowed = None
        self.localize = None
        self.fZoneWeight = None
        self.thumbnail = None
        self.PlayerLoseCoinsOnDeath = None
        self.disableSaveLoc = None
        self.teamRadius = None
        self.gate_version = None
        self.mountsAllowed = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = ZoneTableTable()
            return_val.zoneID = results[0]
            return_val.locStatus = results[1]
            return_val.zoneName = results[2]
            return_val.scriptID = results[3]
            return_val.ghostdistance_min = results[4]
            return_val.ghostdistance = results[5]
            return_val.population_soft_cap = results[6]
            return_val.population_hard_cap = results[7]
            return_val.DisplayDescription = results[8]
            return_val.mapFolder = results[9]
            return_val.smashableMinDistance = results[10]
            return_val.smashableMaxDistance = results[11]
            return_val.mixerProgram = results[12]
            return_val.clientPhysicsFramerate = results[13]
            return_val.serverPhysicsFramerate = results[14]
            return_val.zoneControlTemplate = results[15]
            return_val.widthInChunks = results[16]
            return_val.heightInChunks = results[17]
            return_val.petsAllowed = results[18]
            return_val.localize = results[19]
            return_val.fZoneWeight = results[20]
            return_val.thumbnail = results[21]
            return_val.PlayerLoseCoinsOnDeath = results[22]
            return_val.disableSaveLoc = results[23]
            return_val.teamRadius = results[24]
            return_val.gate_version = results[25]
            return_val.mountsAllowed = results[26]
        else:
            return_val = []
            for row in results:
                val = ZoneTableTable()
                val.zoneID = row[0]
                val.locStatus = row[1]
                val.zoneName = row[2]
                val.scriptID = row[3]
                val.ghostdistance_min = row[4]
                val.ghostdistance = row[5]
                val.population_soft_cap = row[6]
                val.population_hard_cap = row[7]
                val.DisplayDescription = row[8]
                val.mapFolder = row[9]
                val.smashableMinDistance = row[10]
                val.smashableMaxDistance = row[11]
                val.mixerProgram = row[12]
                val.clientPhysicsFramerate = row[13]
                val.serverPhysicsFramerate = row[14]
                val.zoneControlTemplate = row[15]
                val.widthInChunks = row[16]
                val.heightInChunks = row[17]
                val.petsAllowed = row[18]
                val.localize = row[19]
                val.fZoneWeight = row[20]
                val.thumbnail = row[21]
                val.PlayerLoseCoinsOnDeath = row[22]
                val.disableSaveLoc = row[23]
                val.teamRadius = row[24]
                val.gate_version = row[25]
                val.mountsAllowed = row[26]
                return_val.append(val)

        return return_val


class BrickAttributesTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.ID = None
        self.icon_asset = None
        self.display_order = None
        self.locStatus = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = BrickAttributesTable()
            return_val.ID = results[0]
            return_val.icon_asset = results[1]
            return_val.display_order = results[2]
            return_val.locStatus = results[3]
        else:
            return_val = []
            for row in results:
                val = BrickAttributesTable()
                val.ID = row[0]
                val.icon_asset = row[1]
                val.display_order = row[2]
                val.locStatus = row[3]
                return_val.append(val)

        return return_val


class DtPropertiesTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.objectid = None
        self.property = None
        self.value = None
        self.uvalue = None
        self.lvalue = None
        self.version = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = DtPropertiesTable()
            return_val.id = results[0]
            return_val.objectid = results[1]
            return_val.property = results[2]
            return_val.value = results[3]
            return_val.uvalue = results[4]
            return_val.lvalue = results[5]
            return_val.version = results[6]
        else:
            return_val = []
            for row in results:
                val = DtPropertiesTable()
                val.id = row[0]
                val.objectid = row[1]
                val.property = row[2]
                val.value = row[3]
                val.uvalue = row[4]
                val.lvalue = row[5]
                val.version = row[6]
                return_val.append(val)

        return return_val


class MapAnimationPrioritiesTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.name = None
        self.priority = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MapAnimationPrioritiesTable()
            return_val.id = results[0]
            return_val.name = results[1]
            return_val.priority = results[2]
        else:
            return_val = []
            for row in results:
                val = MapAnimationPrioritiesTable()
                val.id = row[0]
                val.name = row[1]
                val.priority = row[2]
                return_val.append(val)

        return return_val


class MapAssetTypeTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.label = None
        self.pathdir = None
        self.typelabel = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MapAssetTypeTable()
            return_val.id = results[0]
            return_val.label = results[1]
            return_val.pathdir = results[2]
            return_val.typelabel = results[3]
        else:
            return_val = []
            for row in results:
                val = MapAssetTypeTable()
                val.id = row[0]
                val.label = row[1]
                val.pathdir = row[2]
                val.typelabel = row[3]
                return_val.append(val)

        return return_val


class MapIconTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.LOT = None
        self.iconID = None
        self.iconState = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MapIconTable()
            return_val.LOT = results[0]
            return_val.iconID = results[1]
            return_val.iconState = results[2]
        else:
            return_val = []
            for row in results:
                val = MapIconTable()
                val.LOT = row[0]
                val.iconID = row[1]
                val.iconState = row[2]
                return_val.append(val)

        return return_val


class MapItemTypesTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.description = None
        self.equipLocation = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MapItemTypesTable()
            return_val.id = results[0]
            return_val.description = results[1]
            return_val.equipLocation = results[2]
        else:
            return_val = []
            for row in results:
                val = MapItemTypesTable()
                val.id = row[0]
                val.description = row[1]
                val.equipLocation = row[2]
                return_val.append(val)

        return return_val


class MapRenderEffectsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.gameID = None
        self.description = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MapRenderEffectsTable()
            return_val.id = results[0]
            return_val.gameID = results[1]
            return_val.description = results[2]
        else:
            return_val = []
            for row in results:
                val = MapRenderEffectsTable()
                val.id = row[0]
                val.gameID = row[1]
                val.description = row[2]
                return_val.append(val)

        return return_val


class MapShadersTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.label = None
        self.gameValue = None
        self.priority = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MapShadersTable()
            return_val.id = results[0]
            return_val.label = results[1]
            return_val.gameValue = results[2]
            return_val.priority = results[3]
        else:
            return_val = []
            for row in results:
                val = MapShadersTable()
                val.id = row[0]
                val.label = row[1]
                val.gameValue = row[2]
                val.priority = row[3]
                return_val.append(val)

        return return_val


class MapTextureResourceTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.texturepath = None
        self.SurfaceType = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MapTextureResourceTable()
            return_val.id = results[0]
            return_val.texturepath = results[1]
            return_val.SurfaceType = results[2]
        else:
            return_val = []
            for row in results:
                val = MapTextureResourceTable()
                val.id = row[0]
                val.texturepath = row[1]
                val.SurfaceType = row[2]
                return_val.append(val)

        return return_val


class MapBlueprintCategoryTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.id = None
        self.description = None
        self.enabled = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = MapBlueprintCategoryTable()
            return_val.id = results[0]
            return_val.description = results[1]
            return_val.enabled = results[2]
        else:
            return_val = []
            for row in results:
                val = MapBlueprintCategoryTable()
                val.id = row[0]
                val.description = row[1]
                val.enabled = row[2]
                return_val.append(val)

        return return_val


class SysDiagramsTable(CDClientTable):
    def __init__(self):
        super().__init__()
        self.name = None
        self.principal_id = None
        self.diagram_id = None
        self.version = None
        self.definition = None

    @classmethod
    def filter_return_results(cls, results):
        if results is None:
            return []
        multilayer = isinstance(results[0], tuple)
        if not multilayer:
            return_val = SysDiagramsTable()
            return_val.name = results[0]
            return_val.principal_id = results[1]
            return_val.diagram_id = results[2]
            return_val.version = results[3]
            return_val.definition = results[4]
        else:
            return_val = []
            for row in results:
                val = SysDiagramsTable()
                val.name = row[0]
                val.principal_id = row[1]
                val.diagram_id = row[2]
                val.version = row[3]
                val.definition = row[4]
                return_val.append(val)

        return return_val

