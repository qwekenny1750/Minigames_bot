import os
import asyncio

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger, String, ForeignKey, Integer, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declarative_base

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

engine = create_async_engine(url=os.getenv('DATABASE_URL'))
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    phone: Mapped[str] = mapped_column(String(15), nullable=True)

class City_Game(Base):
    __tablename__ = "city_game"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    city_last_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    city_max_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    city_is_winner: Mapped[str] = mapped_column(String(32), default='NOT')

class Bascetball_game(Base):
    __tablename__ = "bascetball_game"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    bascetball_last_status: Mapped[str] = mapped_column(String(32), default='Ни разу не играл')
    bascetball_last_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    bascetball_max_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

class Roll_game(Base):
    __tablename__ = "roll_game"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    roll_last_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    roll_max_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

class Football_game(Base):
    __tablename__ = "football_game"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    football_last_status: Mapped[str] = mapped_column(String(32), default='Ни разу не играл')
    football_last_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    football__best_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Подключение успешно")

