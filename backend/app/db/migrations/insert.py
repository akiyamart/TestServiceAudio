from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession


from ..models import (
    AdminOrm, 
)
from ..engine import async_session
from ...dependencies.hasher import Hasher

admins_data: list[dict] = [
    {
        "login": "admin",
        "password_hash": "admin",
    }
]

async def table_exists(session: AsyncSession, table_name: str) -> bool:
    result = await session.execute(
        text(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = :table_name)"),
        {"table_name": table_name}
    )
    return result.scalar()

async def insert_admins(session: AsyncSession):
    if not await table_exists(session, "users"):
        print("Table 'users' not found, skip data insertion")
        return

    stmt = select(AdminOrm).limit(1)
    if not ((await session.execute(stmt)).scalar_one_or_none()):
        for obj_data in admins_data:
            hashed_password = Hasher.get_password_hash(obj_data["password_hash"])
            admin_data = {
                "login": obj_data["login"],
                "password_hash": hashed_password
            }
            session.add(AdminOrm(**admin_data))
        await session.flush()


async def insert_data(test_mode: bool) -> None:
    async with async_session() as session:
        if test_mode:
            pass
        else:
            pass
        await insert_admins(session=session)
        await session.commit()
