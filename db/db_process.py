from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from db.models import HeroDB, WeaponDB, ArmorDB
from weapon import Weapon
from armor import Armor
from hero import Hero

async def get_hero_db(async_session: async_sessionmaker[AsyncSession], user_id):
    async with async_session() as session:
        result = await session.execute(select(HeroDB).where(HeroDB.user_id == user_id))
        return result.scalars().all()


async def get_hero_weapon_db(async_session: async_sessionmaker[AsyncSession], hero):
    async with async_session() as session:
        result = await session.execute(select(WeaponDB).where(WeaponDB.user_id == hero.id))
        return result.scalars().all()


async def get_hero_armor_db(async_session: async_sessionmaker[AsyncSession], hero):
    async with async_session() as session:
        result = await session.execute(select(ArmorDB).where(ArmorDB.user_id == hero.id))
        return result.scalars().all()


async def add_hero_db(async_session: async_sessionmaker[AsyncSession], hero: Hero):
    async with async_session() as session:
        async with session.begin():
            new_hero = hero.to_db()
            session.add(new_hero)
            hero.base_id = new_hero.id
            return new_hero


async def add_hero_weapon_db(async_session: async_sessionmaker[AsyncSession], hero: Hero):
    async with async_session() as session:
        async with session.begin():
            if hero.weapon:
                wdb = hero.weapon.to_db()
                wdb.user_id = hero.base_id
                session.add(wdb)
            for eq in hero.stock.equip:
                if isinstance(hero.stock.equip[eq], Weapon):
                    wdb = hero.stock.equip[eq].to_db()
                    wdb.user_id = hero.base_id
                    session.add(wdb)


async def add_hero_armor_db(async_session: async_sessionmaker[AsyncSession], hero: Hero):
    async with async_session() as session:
        async with session.begin():
            for i in hero.armor:
                if i:
                    i.use = 1
                    adb = i.to_db()
                    adb.user_id = hero.base_id
                    session.add(adb)

            for eq in hero.stock.equip:
                if isinstance(hero.stock.equip[eq], Armor):
                    hero.stock.equip[eq].use = 0
                    adb = hero.stock.equip[eq].to_db()
                    adb.user_id = hero.base_id
                    session.add(adb)


async def delete_hero_weapon_db(async_session: async_sessionmaker[AsyncSession], hero: Hero):
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(WeaponDB).where(WeaponDB.user_id == hero.base_id))
            await session.commit()


async def delete_hero_armor_db(async_session: async_sessionmaker[AsyncSession], hero: Hero):
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(ArmorDB).where(ArmorDB.user_id == hero.base_id))
            await session.commit()


async def upd_hero_db(async_session: async_sessionmaker[AsyncSession], hero: Hero):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(HeroDB).where(HeroDB.user_id == hero.id))
            res = result.scalars().one()
            res.copy_val(hero.to_db())
            await session.commit()