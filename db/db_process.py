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



async def create_table_db(async_session: async_sessionmaker[AsyncSession]):
    async with async_session() as session:
        await session.execute(text(str(CreateTable(ItemsDB.__table__).compile(dialect=dialect()))))
        await session.commit()


async def get_hero_db(async_session: async_sessionmaker[AsyncSession], user_id = 0):
    async with async_session() as session:
        if user_id:
            result = await session.execute(select(HeroDB).where(HeroDB.user_id == user_id))
        else:
            result = await session.execute(select(HeroDB))
        return result.scalars().all()


async def get_hero_weapon_db(async_session: async_sessionmaker[AsyncSession], herodb):
    async with async_session() as session:
        result = await session.execute(select(WeaponDB).where(WeaponDB.user_id == herodb.id))
        return result.scalars().all()


async def get_hero_armor_db(async_session: async_sessionmaker[AsyncSession], herodb):
    async with async_session() as session:
        result = await session.execute(select(ArmorDB).where(ArmorDB.user_id == herodb.id))
        return result.scalars().all()


async def add_hero_db(async_session: async_sessionmaker[AsyncSession], hero: Hero):
    async with async_session() as session:
        async with session.begin():
            new_hero = hero.to_db()
            session.add(new_hero)
            hero.base_id = new_hero.id
            return new_hero


async def upd_hero_weapon(async_session: async_sessionmaker[AsyncSession], hero: Hero):
    async with async_session() as session:
        result = await session.execute(select(WeaponDB).where(WeaponDB.user_id == hero.base_id))
        codes = []
        drop_codes = []
        for w in result.scalars().all():
            codes.append(w.code)
            if hero.weapon and hero.weapon.get_code() == w.code:
                w.use = 1
                w.life = hero.weapon.life
                w.max_life = hero.weapon.max_life
                w.z = hero.weapon.z
                continue

            wp = hero.stock.equip.get(w.code, None)
            if wp:
                w.use = 0
                w.life = wp.life
                w.max_life = wp.max_life
                w.z = wp.z
            else:
                drop_codes.append(w.code)

        for key, val in hero.stock.equip.items():
            if key not in codes and isinstance(val, Weapon):
                itm = val.to_db()
                itm.user_id = hero.base_id
                session.add(itm)
        for code in drop_codes:
            await session.execute(delete(WeaponDB).where(and_(WeaponDB.user_id == hero.base_id, WeaponDB.code == code)))

        await session.commit()


async def upd_hero_armor(async_session: async_sessionmaker[AsyncSession], hero: Hero):
    async with async_session() as session:
        result = await session.execute(select(ArmorDB).where(ArmorDB.user_id == hero.base_id))
        codes = []
        drop_codes = []
        for a in result.scalars().all():
            codes.append(a.code)
            skip = False
            for ia in hero.armor:
                if ia and ia.get_code() == a.code:
                    a.use = 1
                    a.life = ia.life
                    a.max_life = ia.max_life
                    a.z = ia.z
                    skip = True
                    break
            if skip:
                continue

            ap = hero.stock.equip.get(a.code, None)
            if ap:
                a.use = 0
                a.life = ap.life
                a.max_life = ap.max_life
                a.z = ap.z
            else:
                drop_codes.append(a.code)

        for key, val in hero.stock.equip.items():

            if key not in codes and isinstance(val, Armor):
                itm = val.to_db()
                itm.user_id = hero.base_id
                session.add(itm)

        for code in drop_codes:
            await session.execute(delete(ArmorDB).where(and_(ArmorDB.user_id == hero.base_id, ArmorDB.code == code)))

        await session.commit()



async def upd_hero_db(async_session: async_sessionmaker[AsyncSession], hero: Hero):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(HeroDB).where(HeroDB.user_id == hero.id))
            res = result.scalars().one()
            res.copy_val(hero.to_db())
            await session.commit()


async def get_hero_items_db(async_session: async_sessionmaker[AsyncSession], herodb):
    async with async_session() as session:
        result = await session.execute(select(ItemsDB).where(ItemsDB.user_id == herodb.id))
        return result.scalars().all()


async def update_hero_items(async_session: async_sessionmaker[AsyncSession], hero: Hero):
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

        for key, val in hero.stock.used_stuff.items():
            if key not in ind:
                itm = ItemsDB(index = key, user_id=hero.base_id, count = val )
                session.add(itm)

        await session.commit()


