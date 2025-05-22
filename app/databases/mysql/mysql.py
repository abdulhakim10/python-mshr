from aiomysql import create_pool

mysql_pool = None  # Global variable to hold the connection pool

async def init_mysql_pool():
    global mysql_pool
    mysql_pool = await create_pool(
        host="localhost",
        port=3307,
        user="root",
        password="rootpassword",
        db="maisdev_msadmin",
    )
