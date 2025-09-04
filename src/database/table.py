"""anda tidak perlu run ini di main.

fungsi ini khusus di gunakan untuk inisialisasi database, semisal pada saat migrasi atau testing.
kita pakai alembic untuk migrasi, tapi kita perlu buat tabel pada saat testing.
jadi fungsi ini di panggil pada saat testing.
atau jika anda ingin inisialisasi database secara manual, bisa pakai ini juga.

"""
# NOTE : anda tidak perlu run ini di main

from loguru import logger
from sqlalchemy import inspect
from src.models import Base


# Create tables helper
async def create_tables(engine):  # noqa: ANN001
    """Create all database tables.

    This function creates all tables defined in the SQLAlchemy models.
    """
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: Base.metadata.create_all(sync_conn, checkfirst=True)
        )
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
        logger.info(f"Tables after create_tables: {tables}")
