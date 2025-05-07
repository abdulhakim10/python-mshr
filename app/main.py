from fastapi import FastAPI

from app.routers import example

app = FastAPI()

app.include_router(example.router)

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
staff = Staff(app_info=app_info, db=DummyDB(), data=payload)
print(staff.Data.personal)
print(staff.Data.address)
print(staff.Data.job)
