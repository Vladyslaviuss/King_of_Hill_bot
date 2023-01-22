from sqlalchemy.engine import URL

postgres_url: URL = URL.create(
    'postgresql+asyncpg',
    username='postgres',
    password='qwerty',
    host='localhost',
    database='hilldb',
    port=5432
)