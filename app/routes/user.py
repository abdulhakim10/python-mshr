from fastapi import APIRouter
from app.databases.database import get_connection
from app.services.staff_services import Staff
from app.services.user_test import CoaUserManager

router = APIRouter()

app_info = {
    "user_id": "1004",
    "app_name": "EBOSS",
    "sch_id": "0",
    "user_sid": "0",
    "system_level": "ACL01",
    "system_access": "full",
    "url": "https://testcorp.com/app"
}

# @router.get("/users")
# async def get_users():
#     conn = await get_connection()
#     async with conn.cursor() as cur:
#         await cur.execute("SELECT * FROM client")
#         result = await cur.fetchall()
#     conn.close()
#     return result
@router.get("/staff")
async def get_staff():
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM usr")
        result = await cur.fetchall()
    conn.close()
    return result
@router.get("/staff_list")
async def get_staff_list():
    conn = await get_connection()  # must return an aiomysql.Connection
    staff_service = Staff(db=conn)
    result = await staff_service.staff_list()
    return result

@router.get("/users")
async def get_users():
    conn = await get_connection()
    user_test = CoaUserManager(db=conn)
    result = await user_test.fetch_user()
    # Debug print
    # from pprint import pprint
    # pprint(result)
    # print("TYPES:")
    # for k, v in result.items():
    #     print(f"{k}: {type(v)}")
    return result