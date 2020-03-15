import sqlite3
from plugins.easy_cdclient.cdclient_tables import *
from plugins.easy_cdclient.cdclient_enum import *


class Zone:
    def __init__(self, zone_id):
        self.zone_id = zone_id
        self.checksum = 0

        if zone_id in zone_checksums:
            self.checksum = zone_checksums[zone_id]

        conn = sqlite3.connect("./res/cdclient.sqlite")
        c = conn.cursor()
        c.execute("SELECT * FROM ZoneTable WHERE zoneID = ?", (zone_id,))
        self.zone_data = ZoneTableTable.filter_return_results(c.fetchone())
        conn.close()


class GameObject:
    def __init__(self, lot):
        self.components = {}
        self.object_data = None

        conn = sqlite3.connect("./res/cdclient.sqlite")
        c = conn.cursor()
        c.execute("SELECT * FROM Objects WHERE id = ?", (lot,))
        self.object_data = ObjectsTable.filter_return_results(c.fetchone())
        c.execute("SELECT component_type, component_id FROM ComponentsRegistry WHERE id = ?", (lot,))
        components = c.fetchall()
        for component in components:
            data_class, table_name = GameObject.get_component_class(int(component[0]))
            if data_class is not None:
                c.execute(f"SELECT * FROM {table_name} WHERE id = ?", (component[1],))
                comp = data_class.filter_return_results(c.fetchall())
                if len(comp) == 1:
                    self.components[component[0]] = comp[0]
                else:
                    self.components[component[0]] = comp
            else:
                self.components[component[0]] = None
        conn.close()

    @classmethod
    def get_component_class(cls, component_type: int):
        if component_type == COMPONENTS.SIMPLE_PHYSICS.value:
            return None, None
        elif component_type == COMPONENTS.RENDER.value:
            return RenderComponentTable, "RenderComponent"
        elif component_type == COMPONENTS.SIMPLE_PHYSICS.value:
            return PhysicsComponentTable, "PhysicsComponent"
        elif component_type == COMPONENTS.CHARACTER.value:
            return None, None
        elif component_type == COMPONENTS.SCRIPT.value:
            return ScriptComponentTable, "ScriptComponent"
        elif component_type == COMPONENTS.BOUNCER.value:
            return None, None
        elif component_type == COMPONENTS.DESTROYABLE.value:
            return DestructibleComponentTable, "DestructibleComponent"
        elif component_type == COMPONENTS.SKILL.value:
            return ObjectSkillsTable, "ObjectSkills"
        elif component_type == COMPONENTS.SPAWNER.value:
            return None, None
        elif component_type == COMPONENTS.ITEM.value:
            return ItemComponentTable, "ItemComponent"
        elif component_type == COMPONENTS.REBUILD.value:
            return RebuildComponentTable, "RebuildComponent"
        elif component_type == COMPONENTS.REBUILD_START.value:
            return None, None
        elif component_type == COMPONENTS.VENDOR.value:
            return VendorComponentTable, "VenderComponent"
        elif component_type == COMPONENTS.INVENTORY.value:
            return InventoryComponentTable, "InventoryComponent"
        elif component_type == COMPONENTS.PROJECTILE_PHYSICS.value:
            return None, None
        elif component_type == COMPONENTS.SHOOTING_GALLERY.value:
            return None, None
        elif component_type == COMPONENTS.RIGID_BODY_PHANTOM_PHYSICS.value:
            return None, None
        elif component_type == COMPONENTS.CHEST.value:
            return None, None
        elif component_type == COMPONENTS.COLLECTIBLE.value:
            return CollectibleComponentTable, "CollectibleComponent"
        elif component_type == COMPONENTS.BLUEPRINT.value:
            return BlueprintsTable, "Blueprints"
        elif component_type == COMPONENTS.MOVING_PLATFORM.value:
            return MovingPlatformsTable, "MovingPlatforms"
        elif component_type == COMPONENTS.PET.value:
            return PetComponentTable, "PetComponent"
        elif component_type == COMPONENTS.PLATFORM_BOUNDARY.value:
            return None, None
        elif component_type == COMPONENTS.MODULE.value:
            return ModuleComponentTable, "ModuleComponent"
        elif component_type == COMPONENTS.ARCADE.value:
            return None, None
        elif component_type == COMPONENTS.VEHICLE_PHYSICS_0.value:
            return None, None # Vehicle Physics Table?
        elif component_type == COMPONENTS.MOVEMENT_AI.value:
            return MovementAIComponentTable, "MovingAIComponent"
        elif component_type == COMPONENTS.EXHIBIT.value:
            return ExhibitComponentTable, "ExhibitComponent"
        elif component_type == COMPONENTS.MINIFIG.value:
            return MinifigComponentTable, "MinifigComponent"
        elif component_type == COMPONENTS.PROPERTY.value:
            return None, None
        elif component_type == COMPONENTS.PET_CREATOR.value:
            return None, None
        elif component_type == COMPONENTS.MODEL_BUILDER.value:
            return None, None
        elif component_type == COMPONENTS.SCRIPTED_ACTIVITY.value:
            return None, None
        elif component_type == COMPONENTS.PHANTOM_PHYSICS.value:
            return None, None
        elif component_type == COMPONENTS.SPRINGPAD.value:
            return None, None
        elif component_type == COMPONENTS.B3_BEHAVIORS.value:
            return None, None
        elif component_type == COMPONENTS.PROPERTY_ENTRANCE.value:
            return PropertyEntranceComponentTable, "PropertyEntranceComponent"
        elif component_type == COMPONENTS.PROPERTY_MANAGEMENT.value:
            return None, None
        elif component_type == COMPONENTS.VEHICLE_PHYSICS_1.value:
            return None, None # Vehicle Physics Table?
        elif component_type == COMPONENTS.PHYSICS_SYSTEM.value:
            return None, None
        elif component_type == COMPONENTS.QUICK_BUILD.value:
            return RebuildComponentTable, "RebuildComponent" # ???
        elif component_type == COMPONENTS.SWITCH.value:
            return None, None
        elif component_type == COMPONENTS.MINIGAME.value:
            return None, None
        elif component_type == COMPONENTS.CHANGLING.value:
            return None, None
        elif component_type == COMPONENTS.CHOICE_BUILD.value:
            return ChoiceBuildComponentTable, "ChoiceBuildComponent"
        elif component_type == COMPONENTS.PACKAGE.value:
            return PackageComponentTable, "PackageComponent"
        elif component_type == COMPONENTS.SOUND_REPEATER.value:
            return None, None
        elif component_type == COMPONENTS.SOUND_AMBIENT_2D.value:
            return None, None
        elif component_type == COMPONENTS.SOUND_AMBIENT_3D.value:
            return None, None
        elif component_type == COMPONENTS.PRECONDITION.value:
            return PreconditionsTable, "Preconditions"
        elif component_type == COMPONENTS.CUSTOM_BUILD_ASSEMBLY.value:
            return None, None
        elif component_type == COMPONENTS.BASE_COMBAT_AI.value:
            return BaseCombatAIComponentTable, "BaseCombatAIComponent"
        elif component_type == COMPONENTS.MODULE_ASSEMBLY.value:
            return None, None # ???
        elif component_type == COMPONENTS.SHOWCASE_MODEL_HANDLER.value:
            return None, None
        elif component_type == COMPONENTS.RACING_MODULE.value:
            return RacingModuleComponentTable, "RacingModuleComponent"
        elif component_type == COMPONENTS.GENERIC_ACTIVATOR.value:
            return None, None
        elif component_type == COMPONENTS.PROPERTY_VENDOR.value:
            return None, None
        elif component_type == COMPONENTS.HF_LIGHT_DIRECTION_GADGET.value:
            return None, None
        elif component_type == COMPONENTS.ROCKET_LAUNCH.value:
            return None, None
        elif component_type == COMPONENTS.ROCKET_LANDING.value:
            return None, None
        elif component_type == COMPONENTS.RACING_CONTROL.value:
            return None, None
        elif component_type == COMPONENTS.FACTION_TRIGGER.value:
            return None, None
        elif component_type == COMPONENTS.MISSION_OFFER.value:
            return MissionNPCComponentTable, "MissionNPCComponent" # ???
        elif component_type == COMPONENTS.RACING_STATS.value:
            return None, None
        elif component_type == COMPONENTS.LUP_EXHIBIT.value:
            return LUPExhibitComponentTable, "LUPExhibitComponent"
        elif component_type == COMPONENTS.SOUND_TRIGGER.value:
            return None, None
        elif component_type == COMPONENTS.PROXIMITY_MONITOR.value:
            return ProximityMonitorComponentTable, "ProximityMonitorComponent"
        elif component_type == COMPONENTS.USER_CONTROL.value:
            return None, None
        elif component_type == COMPONENTS.LUP_LAUNCHPAD.value:
            return None, None
        elif component_type == COMPONENTS.BRICK_DONATION.value:
            return None, None
        elif component_type == COMPONENTS.COMMENDATION_VENDOR.value:
            return None, None
        elif component_type == COMPONENTS.RAIL_ACTIVATOR.value:
            return RailActivatorComponentTable, "RailActivatorComponent"
        elif component_type == COMPONENTS.ROLLER.value:
            return None, None
        elif component_type == COMPONENTS.POSSESSABLE.value:
            return PossessableComponentTable, "PossessableComponent"
        elif component_type == COMPONENTS.PROPERTY_PLAQUE.value:
            return None, None
        elif component_type == COMPONENTS.BUILD_BORDER.value:
            return None, None
        elif component_type == COMPONENTS.CULLING_PLANE.value:
            return None, None
