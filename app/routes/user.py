from fastapi import APIRouter, Depends, Body
from app.databases.database import get_connection
from app.services.staff_services import Staff
from app.services.user_service import UserProfile
from app.services.user_service import (
    FilterSchema,
    UserSchema,
    AddressDataSchema,
    PersonalSchema,
    JobSchema,
    SystemSchema,
    AddressSchema,
    FamilySchema,
    EducationSchema,
    WorkExperienceSchema,
)

router = APIRouter()

app_info = {
    "user_id": "1004",
    "app_name": "EBOSS",
    "sch_id": "0",
    "user_sid": "0",
    "system_level": "ACL01",
    "system_access": "full",
    "url": "https://testcorp.com/app",
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




# @router.get("/staff_list")
# async def get_staff_list():


#     conn = await get_connection()  # must return an aiomysql.Connection
#     staff_service = Staff(db=conn)
#     result = await staff_service.staff_list()
#     return result
@router.get("/staff_list")
async def list_staff(
    division: str = None,
    search: str = None,
    page_start: int = 1,
    page_limit: int = 10,
    page_order: str = "id",
    page_sort: str = "asc",
    db=Depends(get_connection),  # type: ignore
):
    filter_data = {
        "filter_division": division,
        "filter_search": search,
    }

    paginate_data = {
        "page_start": page_start,
        "page_limit": page_limit,
        "page_order": page_order,
        "page_sort": page_sort,
    }
    # staff_service = Staff(db=db)
    result = await Staff(db=db).get_filtered_staff(
        db=db, filter_data=filter_data, paginate_data=paginate_data
    )
    return result


@router.post("/users")
async def get_users(request: FilterSchema):
    conn = await get_connection()
    user_test = UserProfile(db=conn)
    result = await user_test.fetch_user(request)
    # # Debug print
    # from pprint import pprint
    # pprint(result)
    # print("TYPES:")
    # for k, v in result.items():
    #     print(f"{k}: {type(v)}")
    return result


@router.post("/create_user")
async def create_user(
    user: UserSchema = Body(...),
    address: AddressSchema = Body(...),
    personal: PersonalSchema = Body(...),
    job: JobSchema = Body(...),
    system: SystemSchema = Body(...),
    family: FamilySchema = Body(...),
):
    conn = await get_connection()
    user_profile = UserProfile(db=conn)
    result = await user_profile.create_user(
        user, address, personal, job, system, family
    )
    # Debug print
    from pprint import pprint

    pprint(result)
    print("TYPES:")
    for k, v in result.items():
        print(f"{k}: {type(v)}")
    return result
