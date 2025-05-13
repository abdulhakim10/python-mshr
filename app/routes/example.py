from fastapi import APIRouter
# from app.databases.mysql.db_connector import DBConnector

router = APIRouter(prefix="/example", tags=["example"])

router = APIRouter()

# @router.get("/health/db")
# def check_db():
#     db = DBConnector(
#         host='127.0.0.1',
#         port='3307',
#         user='root',
#         password='rootpassword',
#         database='maisdev_msadmin'
#     )
#     if db.err_id:
#         return {"status": "fail", "error": db.err_id}
#     db.close()
#     return {"status": "ok"}
