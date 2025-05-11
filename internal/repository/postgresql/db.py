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
                    password TEXT NOT NULL,
                    gmail TEXT UNIQUE NOT NULL,
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
                    userid BIGINT NOT NULL REFERENCES users(userid) ON DELETE CASCADE,
                    status order_status NOT NULL DEFAULT 'created',
                    added_time TIMESTAMP NOT NULL DEFAULT now(),
                    updated_time TIMESTAMP
                );
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS cart (
                    cartid BIGSERIAL PRIMARY KEY,
                    userid BIGINT NOT NULL UNIQUE REFERENCES users(userid) ON DELETE CASCADE,
                    added_time TIMESTAMP NOT NULL DEFAULT now()
                );
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS cart_items (
                    itemid BIGSERIAL PRIMARY KEY,
                    cartid BIGINT NOT NULL REFERENCES cart(cartid) ON DELETE CASCADE,
                    productid BIGINT NOT NULL REFERENCES product(productid) ON DELETE CASCADE,
                    quantity INTEGER NOT NULL CHECK (quantity > 0),
                    UNIQUE (cartid, productid)
                );
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS category (
                    categoryid BIGSERIAL PRIMARY KEY,
                    categoryname TEXT UNIQUE NOT NULL
                );
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS product (
                    productid BIGSERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    info TEXT,
                    price BIGINT NOT NULL,
                    volume_ml FLOAT NOT NULL,
                    categoryid BIGINT REFERENCES category(categoryid) ON DELETE CASCADE,
                    UNIQUE (name, volume_ml)
                );
            """)
    except Exception as e:
        logger.error(f'init_db error: {e}')