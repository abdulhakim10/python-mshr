import os
from fastapi import FastAPI
import uvicorn

from app.routes import example
from app.routes import user

app = FastAPI()
# app.include_router(
#     route_coa.router, prefix="/api/v1/finance", tags=['finance']
# )
app.include_router(example.router)
app.include_router(user.router)

from app.services.staff_services import Staff

# Sample app_info and payload
app_info = {
    "user_id": 1,
    "app_name": "HRApp",
    "sid": 10,
    "user_sid": 10,
    "system_level": "admin",
    "system_access": "full",
    "cust_name": "TestCorp",
    "url": "https://testcorp.com/app"
}

payload = {
    "personal": {"name": "Ali"},
    "address": {"city": "Kuala Lumpur"},
    "job": {"position": "Manager"},
}

# Dummy DB class with .select()
class DummyDB:
    def select(self, query):
        print(f"Running query: {query}")
        return [{"bos_config": '{"TIMEZONE":"Asia/Kuala_Lumpur"}'}]

# Initialize staff handler
# staff = Staff(app_info=app_info, db=DummyDB(), data=payload)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        log_level="debug",
        reload=True,
    )