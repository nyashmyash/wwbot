from sqlalchemy import Column, String, Integer, ForeignKey
from db.base import Base
#from hero import Hero
#from weapon import Weapon
#from armor import Armor

class DroneDB(Base):
    __tablename__ = "drones"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    index = Column(Integer)
    user_id = Column(Integer)
    life = Column(Integer)
    max_life = Column(Integer)

class ItemsDB(Base):
    __tablename__ = "items"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    index = Column(Integer)
    user_id = Column(Integer)
    count = Column(Integer)


class WeaponDB(Base):
    __tablename__ = "weapons"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(String)
    life = Column(Integer)
    max_life = Column(Integer)
    use = Column(Integer)
    user_id = Column(Integer)

    def copy_val(self, wp: object) -> None:
        self.use = wp.use
        self.life = wp.life
        self.max_life = wp.max_life
        self.z = wp.z
        self.code = wp.get_code()

class ArmorDB(Base):
    __tablename__ = "armor"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(String)
    life = Column(Integer)
    max_life = Column(Integer)
    use = Column(Integer)
    user_id = Column(Integer)

    def copy_val(self, arm: object) -> None:
        self.use = arm.use
        self.life = arm.life
        self.max_life = arm.max_life
        self.z = arm.z
        self.code = arm.get_code()


class HeroDB(Base):
    __tablename__ = "heroes"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(String, unique=True)
    hp = Column(Integer)
    max_hp = Column(Integer)  # здоровье 1500
    force = Column(Integer)  # cила 1300
    dexterity = Column(Integer)  # ловкость 1200
    charisma = Column(Integer)  # харизма 1200
    luck = Column(Integer)  # удача 1200
    accuracy = Column(Integer)  # меткость 1200
    materials = Column(Integer)
    coins = Column(Integer)
    hungry = Column(Integer)
    km = Column(Integer)
    mob = Column(String)
    all_km = Column(Integer)
    modul = Column(Integer)
    zone = Column(Integer)
    dzen = Column(Integer)

    def copy_val(self, hero: object) -> None:
        self.name = hero.name
        self.user_id = hero.user_id
        self.hp = hero.hp
        self.max_hp = hero.max_hp
        self.force = hero.force
        self.dexterity = hero.dexterity
        self.charisma = hero.charisma
        self.luck = hero.luck
        self.accuracy = hero.accuracy
        self.materials = hero.materials
        self.coins = hero.coins
        self.hungry = hero.hungry
        self.km = hero.km
        self.all_km = hero.all_km
        self.modul = hero.modul
        self.zone = hero.zone
        self.dzen = hero.dzen
