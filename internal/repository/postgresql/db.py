import asyncpg
from internal.core import config
from internal.core.logging import logger

async def create_pool():
    try:
        pool = await asyncpg.create_pool(
            user=config.settings.DB_USER,
            password=config.settings.DB_PASS,
            database=config.settings.DB_NAME,
            host=config.settings.DB_HOST,
            port=config.settings.DB_PORT,
            min_size=1,
            max_size=10
        )
        return pool
    except Exception as e:
        logger.error(f'create_pool error: {e}')


async def init_db(pool):
    try:
        async with pool.acquire() as conn:
            await conn.execute("""DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'order_status') THEN
                        CREATE TYPE order_status AS ENUM ('created','accepted','in_progress','on_the_way','delivered','cancelled');
                    END IF;
                END$$;
                """)
            await conn.execute("""DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'roles') THEN
                        CREATE TYPE roles AS ENUM ('admin', 'user', 'superadmin');
                    END IF;
                END$$;
                """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    userid SERIAL PRIMARY KEY,
                    full_name TEXT,
                    password TEXT,
                    gmail TEXT UNIQUE,
                    added_time TIMESTAMP DEFAULT now(),
                    role roles DEFAULT 'user'
                );
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_status (
                    userid BIGINT PRIMARY KEY REFERENCES users(userid) ON DELETE CASCADE,
                    is_verified BOOLEAN DEFAULT FALSE
                );
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_tokens (
                    userid BIGINT PRIMARY KEY REFERENCES users(userid) ON DELETE CASCADE,
                    refresh_token TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT now(),
                    expires_at TIMESTAMP
                );
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    orderid BIGSERIAL PRIMARY KEY,
                    userid BIGINT REFERENCES users(userid),
                    status order_status DEFAULT 'created',
                    added_time TIMESTAMP NOT NULL DEFAULT now(),
                    updated_time TIMESTAMP
                );
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS basket (
                    basketid BIGSERIAL PRIMARY KEY,
                    userid BIGINT UNIQUE REFERENCES users(userid) ON DELETE CASCADE,
                    added_time TIMESTAMP NOT NULL DEFAULT now()
                );
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS category (
                    categoryid BIGSERIAL PRIMARY KEY,
                    categoryname TEXT UNIQUE
                );
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS product (
                    productid BIGSERIAL PRIMARY KEY,
                    name TEXT,
                    info TEXT,
                    price BIGINT,
                    volume_ml FLOAT,
                    categoryid BIGINT REFERENCES category(categoryid) ON DELETE CASCADE,
                    UNIQUE (name, volume_ml)
                );
            """)
    except Exception as e:
        logger.error(f'init_db error: {e}')