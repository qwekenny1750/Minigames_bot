from database.models import async_session
from database.models import User, City_Game, Roll_game, Bascetball_game, Football_game
from sqlalchemy import select, desc, asc
import asyncio

async def set_user(tg_id, username):
    async with async_session() as session:
        identity = await session.scalar(select(User).where((User.tg_id==tg_id) | (User.username==username)))

        if not identity:
            session.add(User(tg_id=tg_id, username=username))
            await session.commit()


async def set_phone(tg_id, phone):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id==tg_id))
        if user:
            user.phone = phone
            await session.commit()
            await session.refresh(user)


async def set_roll_scores(tg_id,username, roll_last_score):
    async with async_session() as session:
        user = await session.scalar(select(Roll_game).where(Roll_game.tg_id==tg_id))
        if not user:
            session.add(Roll_game(tg_id=tg_id,username=username, roll_last_score=roll_last_score, roll_max_score=roll_last_score))
            await session.commit()
        else:
            user.roll_last_score = roll_last_score
            if roll_last_score > user.roll_max_score:
                user.roll_max_score = roll_last_score
            await session.commit()
            await session.refresh(user)


async def stat_roll(tg_id):
    async with async_session() as session:
        return await session.scalar(select(Roll_game.roll_max_score).where(Roll_game.tg_id==tg_id))
    
async def stat_bascet(tg_id):
    async with async_session() as session:
        return await session.scalar(select(Bascetball_game.bascetball_max_score).where(Bascetball_game.tg_id==tg_id))
    
async def stat_football(tg_id):
    async with async_session() as session:
        return await session.scalar(select(Football_game.football__best_score).where(Football_game.tg_id==tg_id))

async def stat_city(tg_id):
    async with async_session() as session:
        return await session.scalar(select(City_Game.city_max_score).where(City_Game.tg_id==tg_id))
    
async def state_city_if_winner(tg_id):
    async with async_session() as session:
        return await session.scalar(select(City_Game.city_fs_winner).where(City_Game.tg_id==tg_id))


async def set_bascetball_scores(tg_id, username, bascetball_last_status, bascetball_last_score):
    async with async_session() as session:
        user = await session.scalar(select(Bascetball_game).where(Bascetball_game.tg_id==tg_id))
        if not user:
            session.add(Bascetball_game(tg_id=tg_id, username=username, bascetball_last_status=bascetball_last_status, bascetball_last_score=bascetball_last_score, bascetball_max_score=bascetball_last_score))
            await session.commit()
        else:
            user.bascetball_last_score = bascetball_last_score
            user.bascetball_last_status = bascetball_last_status
            if bascetball_last_score > user.bascetball_max_score:
                user.bascetball_max_score = bascetball_last_score
            await session.commit()
            await session.refresh(user)
        
async def set_football_scores(tg_id, username, football_last_status, football_last_score):
    async with async_session() as session:
        user = await session.scalar(select(Football_game).where(Football_game.tg_id==tg_id))
        if not user:
            session.add(Football_game(tg_id=tg_id, username=username, football_last_status=football_last_status, football_last_score=football_last_score, football__best_score=football_last_score))
            await session.commit()
        else:
            user.football_last_score = football_last_score
            user.football_last_status = football_last_status
            if football_last_score < user.football__best_score:
                user.football__best_score = football_last_score
            await session.commit()
            await session.refresh(user)
        
async def set_city_score(tg_id, username, city_last_score):
    async with async_session() as session:
        user = await session.scalar(select(City_Game).where(City_Game.tg_id==tg_id))
        if not user:
            session.add(City_Game(tg_id=tg_id, username=username, city_last_score=city_last_score, city_max_score=city_last_score))
            await session.commit()
        else:
            user.city_last_score = city_last_score
            if city_last_score > user.city_max_score:
                user.city_max_score = city_last_score
            await session.commit()
            await session.refresh(user)

async def set_leaderboard_city():
    async with async_session() as session:
        result = await session.execute(
            select(City_Game.username, City_Game.city_max_score)
            .order_by(desc(City_Game.city_max_score))
            .limit(3)
        )
        return result.all()

async def set_leaderboard_bascetball():
    async with async_session() as session:
        result = await session.execute(
            select(Bascetball_game.username, Bascetball_game.bascetball_max_score)
            .order_by(desc(Bascetball_game.bascetball_max_score))
            .limit(3)
        )
        return result.all()
    
async def set_leaderboard_roll():
    async with async_session() as session:
        result = await session.execute(
            select(Roll_game.username, Roll_game.roll_max_score)
            .order_by(desc(Roll_game.roll_max_score))
            .limit(3)
        )
        return result.all()
    
async def set_leaderboard_football():
    async with async_session() as session:
        result = await session.execute(
            select(Football_game.username, Football_game.football__best_score)
            .order_by(asc(Football_game.football__best_score))
            .limit(3)
        )
        return result.all()


