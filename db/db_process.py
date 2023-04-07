from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from db.models import HeroDB, WeaponDB, ArmorDB, ItemsDB
from weapon import Weapon
from armor import Armor
from hero import Hero
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects.postgresql import dialect
from sqlalchemy.sql import text, and_


async def create_table_db(async_session: async_sessionmaker[AsyncSession]) -> None:
    async with async_session() as session:
        await session.execute(text(str(CreateTable(ItemsDB.__table__).compile(dialect=dialect()))))
        await session.commit()


async def get_hero_db(async_session: async_sessionmaker[AsyncSession], user_id: int = 0) -> list:
    async with async_session() as session:
        if user_id:
            result = await session.execute(select(HeroDB).where(HeroDB.user_id == user_id))
        else:
            result = await session.execute(select(HeroDB))
        return result.scalars().all()


async def get_hero_weapon_db(async_session: async_sessionmaker[AsyncSession], herodb: HeroDB) -> list:
    async with async_session() as session:
        result = await session.execute(select(WeaponDB).where(WeaponDB.user_id == herodb.id))
        return result.scalars().all()


async def get_hero_armor_db(async_session: async_sessionmaker[AsyncSession], herodb: HeroDB) -> list:
    async with async_session() as session:
        result = await session.execute(select(ArmorDB).where(ArmorDB.user_id == herodb.id))
        return result.scalars().all()


async def add_hero_db(async_session: async_sessionmaker[AsyncSession], hero: Hero) -> HeroDB:
    async with async_session() as session:
        async with session.begin():
            new_hero = hero.to_db()
            session.add(new_hero)
            hero.base_id = new_hero.id
            return new_hero


async def upd_indexes(async_session: async_sessionmaker[AsyncSession]) -> None:
    async with async_session() as session:
        result = await session.execute(select(ArmorDB))
        i = 100
        for arm in result.scalars().all():
            arm.id = i
            i += 1
        i = 100
        result = await session.execute(select(WeaponDB))
        for wp in result.scalars().all():
            wp.id = i
            i += 1

        await session.commit()

async def upd_hero_db(async_session: async_sessionmaker[AsyncSession], hero: Hero) -> None:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(HeroDB).where(HeroDB.user_id == hero.id))
            res = result.scalars().one()
            res.copy_val(hero.to_db())
            await session.commit()


async def get_hero_items_db(async_session: async_sessionmaker[AsyncSession], herodb) -> list:
    async with async_session() as session:
        result = await session.execute(select(ItemsDB).where(ItemsDB.user_id == herodb.id))
        return result.scalars().all()


async def update_hero_items(async_session: async_sessionmaker[AsyncSession], hero: Hero) -> None:
    async with async_session() as session:
        result = await session.execute(select(ItemsDB).where(ItemsDB.user_id == hero.base_id))
        ind = []
        for i in result.scalars().all():
            item_user = hero.stock.used_stuff.get(i.index, 0)
            if item_user:
                i.count = hero.stock.used_stuff[i.index]
            else:
                i.count = 0
            ind.append(i.index)

        if hero.stock.used_stuff:
            for key, val in hero.stock.used_stuff.items():
                if key not in ind:
                    itm = ItemsDB(index=key, user_id=hero.base_id, count=val)
                    session.add(itm)
        else:
            hero.stock.used_stuff = {}

        await session.commit()


async def add_hero_weapon_db(async_session: async_sessionmaker[AsyncSession], hero: Hero) -> None:
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
            if hero.drone:
                ddb = hero.drone.to_db()
                ddb.user_id = hero.base_id
                session.add(ddb)
            await session.commit()


async def add_hero_armor_db(async_session: async_sessionmaker[AsyncSession], hero: Hero) -> None:
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
            await session.commit()


async def delete_hero_weapon_db(async_session: async_sessionmaker[AsyncSession], hero: Hero) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(WeaponDB).where(WeaponDB.user_id == hero.base_id))
            await session.commit()


async def delete_hero_armor_db(async_session: async_sessionmaker[AsyncSession], hero: Hero) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(ArmorDB).where(ArmorDB.user_id == hero.base_id))
            await session.commit()
