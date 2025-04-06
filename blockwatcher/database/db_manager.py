import asyncpg

class DatabaseManager:
    def __init__(self, db_url):
        self.db_url = db_url
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.db_url)
        print("✅ Connected to PostgreSQL")

    async def close(self):
        if self.pool:
            await self.pool.close()
            print("🔌 PostgreSQL Connection Closed")

    async def create_tables(self):
        if not self.pool:
            print("⚠️ Connection pool not initialized. Call connect() first.")
            return

        queries = [
            """
            CREATE TABLE IF NOT EXISTS pending_transactions (
                tx_hash TEXT PRIMARY KEY,
                token TEXT,
                from_address TEXT NOT NULL,
                to_address TEXT NOT NULL,
                value NUMERIC NOT NULL,
                gas BIGINT NOT NULL,
                gas_price BIGINT NOT NULL,
                timestamp TIMESTAMPTZ DEFAULT NOW()
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS tokens (
                token_address TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                symbol TEXT NOT NULL,
                decimals INTEGER NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS token_prices (
                token_address TEXT NOT NULL,
                price_usd NUMERIC NOT NULL,
                timestamp TIMESTAMPTZ DEFAULT NOW(),
                PRIMARY KEY (token_address, timestamp)
            );
            """
        ]

        async with self.pool.acquire() as conn:
            for query in queries:
                await conn.execute(query)
        print("📌 Database tables created (if not exist)")

    async def store_pending_tx(self, tx_hash, token, from_address, to_address, value, gas, gas_price):
        if not self.pool:
            print("⚠️ Connection pool not initialized. Call connect() first.")
            return

        query = """
        INSERT INTO pending_transactions (tx_hash, token, from_address, to_address, value, gas, gas_price)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        ON CONFLICT (tx_hash) DO NOTHING;
        """
        async with self.pool.acquire() as conn:
            await conn.execute(
                query, tx_hash, token, from_address, to_address, value, gas, gas_price
            )
        print(f"✅ Stored Pending Transaction: {tx_hash}")

    async def store_token_metadata(self, token_address, name, symbol, decimals):
        if not self.pool:
            print("⚠️ Connection pool not initialized. Call connect() first.")
            return
        query = """
        INSERT INTO tokens (token_address, name, symbol, decimals)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (token_address) DO NOTHING;
        """
        async with self.pool.acquire() as conn:
            await conn.execute(
                query, token_address, name, symbol, decimals
            )

    async def store_token_price(self, token_address, price_usd):
        if not self.pool:
            print("⚠️ Connection pool not initialized. Call connect() first.")
            return

        query = """
        INSERT INTO token_prices (token_address, price_usd)
        VALUES ($1, $2)
        ON CONFLICT (token_address, timestamp) DO NOTHING;
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, token_address, price_usd)
        print(f"💰 Stored Price for {token_address[:8]}...: ${price_usd}")

    async def get_token_metadata(self, token_address):
        if not self.pool:
            print("⚠️ Connection pool not initialized. Call connect() first.")
            return None

        query = """
        SELECT name, symbol, decimals
        FROM tokens
        WHERE token_address = $1;
        """
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow(query, token_address)
            if result:
                return token_address, result['name'], result['symbol'], result['decimals']
            else:
                return None
            
    async def get_token_price(self, token_address):
        if not self.pool:
            print("⚠️ Connection pool not initialized. Call connect() first.")
            return None

        query = """
        SELECT price_usd, timestamp
        FROM token_prices
        WHERE token_address = $1
        ORDER BY timestamp DESC
        LIMIT 1;
        """
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow(query, token_address)
        if result:
            price_usd = result['price_usd']
            timestamp = result['timestamp']
            return price_usd, timestamp
        return None