'''
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
'''
import sqlite3


#This is all for sqlalchemy orm implementation. I'm not 100% sure what Im doing so Im just gonna comment it out until I understand it better
'''
Base = declarative_base()

class Account(Base):
	__tablename__ = "Accounts"

	account_id = Column('account_id', INTEGER, primary_key=True, autoincrement=True)
	username = Column('username', TEXT)
	password = Column('password', TEXT)
	banned = Column('banned', INTEGER)
	is_admin = Column('is_admin', INTEGER)

class CharacterData(Base):
	__tablename__ = "CharacterData"

	universe_score = Column('universe_score', INTEGER)
	level = Column('level', INTEGER)
	health = Column('health', INTEGER)
	max_health = Column('max_health', INTEGER)
	armor = Column('armor', INTEGER)
	max_armor = Column('max_armor', INTEGER)
	imagination = Column('imagination', INTEGER)
	max_imagination = Column('max_imagination', INTEGER)
	currency = Column('currency', INTEGER)
	player_id = Column('player_id', INTEGER)
	backpack_space = Column('backpack_space', INTEGER)
	position = Column('position', TEXT)
	rotation = Column('rotation', TEXT)

class CharacterStats(Base):
	__tablename__ = "CharacterStats"

	currency_collected = Column('currency_collected', INTEGER)
	bricks_collected = Column('bricks_collected', INTEGER)
	smashables_smashed = Column('smashables_smashed', INTEGER)
	level = Column('level', INTEGER)
	quick_builds_done = Column('quick_builds_done', INTEGER)
	enemies_smashed = Column('enemies_smashed', INTEGER)
	rockets_used = Column('rockets_used', INTEGER)
	pets_tamed = Column('pets_tamed', INTEGER)
	imagination_collected = Column('imagination_collected', INTEGER)
	health_collected = Column('health_collected', INTEGER)
	armor_collected = Column('armor_collected', INTEGER)
	distance_traveled = Column('distance_traveled', INTEGER)
	times_died = Column('times_died', INTEGER)
	damage_taken = Column('damage_taken', INTEGER)
	damage_healed = Column('damage_healed', INTEGER)
	armor_repaired = Column('armor_repaired', INTEGER)
	imagination_restored = Column('imagination_restored', INTEGER)
	imagination_used = Column('imagination_used', INTEGER)
	distance_driven = Column('distance_driven', INTEGER)
	time_airborne_in_car = Column('time_airborne_in_car', INTEGER)
	racing_imagination_collected = Column('racing_imagination_collected', INTEGER)
	racing_imagination_crates_smashed = Column('racing_imagination_crates_smashed', INTEGER)
	race_car_boosts = Column('race_car_boosts', INTEGER)
	car_wrecks = Column('car_wrecks', INTEGER)
	racing_smashables_smashed = Column('racing_smashables_smashed', INTEGER)
	races_finished = Column('races_finished', INTEGER)
	races_won = Column('races_won', INTEGER)
	player_id = Column('player_id', INTEGER)

class Character(Base):
	__tablename__ = "Characters"

	player_id = Column('player_id', INTEGER)
	name = Column('name', TEXT)
	zone = Column('zone', INTEGER)
	shirt_color = Column('shirt_color', INTEGER)
	shirt_style = Column('shirt_style', INTEGER)
	pants_color = Column('pants_color', INTEGER)
	hair_color = Column('hair_color', INTEGER)
	hair_style = Column('hair_style', INTEGER)
	lh = Column('lh', INTEGER)
	rh = Column('rh', INTEGER)
	eyebrows = Column('eyebrows', INTEGER)
	eyes = Column('eyes', INTEGER)
	mouth = Column('mouth', INTEGER)
	account_id = Column('account_id', INTEGER)
	custom_name = Column('custom_name', TEXT)

class CompletedMission(Base):
	__tablename__ = "CompletedMissions"

	player_id = Column('player_id', INTEGER)
	mission_id = Column('mission_id', INTEGER)

class CurrentMission(Base):
	__tablename__ = "CurrentMissions"

	player_id = Column('player_id', INTEGER)
	mission_id = Column('mission_id', INTEGER)
	progress = Column('progress', INTEGER)

class Inventory(Base):
	__tablename__ = "Inventory"

	lot = Column('lot', INTEGER)
	slot = Column('slot', INTEGER)
	equipped = Column('equipped', INTEGER)
	linked = Column('linked', INTEGER)
	quantity = Column('quantity', INTEGER)
	item_id = Column('item_id', INTEGER)
	player_id = Column('player_id', INTEGER)
	JSON = Column('JSON', TEXT)

class ZoneObject(Base):
	__tablename__ = "ZoneObjects"

	zone_id = Column('zone_id', INTEGER)
	replica_config = Column('replica_config', TEXT)


class ServerDB():
	def __init__(self, database_path : str):
		engine = create_engine(f"sqlite:///{database_path}")
		metadata = MetaData()
		Base.metadata.create_all(bind=engine)
		Session = sessionmaker(bind=engine)
		Session.configure(bind=engine)
		self.session = Session()
		self.conn = engine.connect()
		self.accounts = Table('accounts', metadata, )
'''

class GameDB():
	def __init__(self, database_path : str):
		self.connection = sqlite3.connect(database_path, check_same_thread=False)
		self.connection.isolation_level = None
		def row_factory(cursor, row):
			d = {}
			for idx, col in enumerate(cursor.description):
				d[col[0]] = row[idx]
			return d
		self.connection.row_factory = row_factory