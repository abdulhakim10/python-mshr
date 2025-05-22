import os, json
from datetime import datetime
import aiomysql
from app.utils.error import ErrorHandler

# from app.databases.mysql.db_connector import DBConnector
from app.objects.user_objects import User, Job, Personal, System
from app.objects.common_objects import DataFilter, DataPaginate, StandardProperties

class StaffData(User):
    def __init__(self):
        super().__init__()
        self.system = None
        self.personal = None
        self.address = None
        self.family = None
        self.job = None
        self.education = None
        self.work_experience = None

class Staff(DataPaginate, DataFilter, StandardProperties):
    def __init__(self, db=None, data=None):
        super().__init__()  # Initialize parent classes
        DataPaginate.__init__(self)
        DataFilter.__init__(self)
        StandardProperties.__init__(self)

        self.Data = StaffData()
        self.payload = data
        self.total_data = 0
        self.total_count = 0
        self.msg = ""
        self.success = False
        self.status_code = 200

        # App metadata (placeholders)
        # self.user_id = app_info.get("uid") if app_info else None
        # self.branch_id = app_info.get("sch_id") if app_info else None
        # self.user_branch_id = app_info.get("user_sid") if app_info else None
        # self.app_name = app_info.get("app_name") if app_info else None
        # self.root_url = app_info.get("url") if app_info else None
        # self.system_level = app_info.get("syslevel") if app_info else None
        # self.system_access = app_info.get("system_access") if app_info else None
        self.DB = db
        self.Err = ErrorHandler()  # Placeholder
        self.err_id = ""
        self.debug = False

        # Parse and apply incoming data (commented out in original)
        # if data:
        #     self.set_data_from_payload(data)

        # self.get_timezone() (commented out in original)

    # def set_data_from_payload(self, data):
    #     for key, value in data.items():
    #         if hasattr(self.Data, key):
    #             setattr(self.Data, key, value)
    #         elif hasattr(self, key):
    #             setattr(self, key, value)

    # def get_timezone(self):
    #     if not self.DB or not self.branch_id:
    #         return
    #     query = f"SELECT bos_config FROM sch WHERE sid={int(self.branch_id)}"
    #     result = self.DB.select(query)
    #     if result:
    #         config = json.loads(result[0].get("bos_config", "{}"))
    #         os.environ["TZ"] = config.get("TIMEZONE", "Asia/Kuala_Lumpur")

    # def handle_date(self, date_str, mode="get"):
    #     if not date_str:
    #         return None
    #     try:
    #         date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    #         return date_obj.strftime("%d-%m-%Y") if mode == "get" else date_str
    #     except ValueError:
    #         return None


    async def staff_list(self):
        filters = []

        # Apply filters from DataFilter
        if self.filter_delete is not None:
            filters.append(f"isdel = {int(self.filter_delete)}")
        else:
            filters.append("isdel = 0")

        if self.filter_branch_id:
            filters.append(f"sch_id = '{self.filter_branch_id}'")

        if self.filter_division:
            filters.append(f"jobdiv = '{self.filter_division}'")

        if self.filter_position:
            filters.append(f"job = '{self.filter_position}'")

        if self.filter_status:
            filters.append(f"jobsta = '{self.filter_status}'")

        if self.filter_gender:
            filters.append(f"sex = '{self.filter_gender}'")

        if self.filter_user_status:
            filters.append(f"status = '{self.filter_user_status}'")

        if self.filter_search:
            search = self.filter_search
            filters.append(f"(name LIKE '%{search}%' OR ic LIKE '%{search}%' OR mel LIKE '%{search}%')")

        # Compose WHERE clause
        where_clause = " AND ".join(filters)
        if where_clause:
            where_clause = f"WHERE {where_clause}"

        # Compose sorting and pagination
        sort_column = self.page_order or "id"
        sort_direction = self.page_sort or "desc"
        order_clause = f"ORDER BY {sort_column} {sort_direction}"

        limit_clause = f"LIMIT {self.page_limit}" if self.page_limit else ""
        offset_clause = ""
        if self.page_limit and self.page_start:
            offset = self.page_limit * (self.page_start - 1)
            offset_clause = f"OFFSET {offset}"

        # Final SQL
        sql_data = f"""
            SELECT uid, id, sch_id, name, ic, hp, mel, syslevel, jobdiv, jobsta, status, ts, adm, delts, delby,
                   nick, sex, bday, race, religion, file, citizen, edulevel, marital, bstate,
                   job, joblvl, jobstart, jobend, jobconfirm, excontract, exvisa, expassport, expermit,
                   isdel
            FROM usr
            {where_clause}
            {order_clause}
            {limit_clause}
            {offset_clause}
        """

        # Fetch data
        params = []
        async with self.DB.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(sql_data)
            result = await cursor.fetchall()

        for row in result:
            obj = User()
            obj.id = row["id"]
            obj.uid = row["uid"]
            obj.app_code = "<reserved>"
            obj.branch_id = row["sch_id"]
            obj.ic = row["ic"]
            obj.name = row["name"]
            obj.email = row["mel"]
            obj.phone = row["hp"]
            obj.user_no = "<reserved>"
            obj.category = "<reserved>"
            obj.category_name = "<reserved>"
            obj.group = "<reserved>"
            obj.group_name = "<reserved>"
            obj.subgroup = "<reserved>"
            obj.subgroup_name = "<reserved>"
            obj.status = int(row["status"]) if row.get("status") else 0
            obj.is_delete = row["isdel"]
            obj.system_level = row.get("syslevel", "")
            obj.user_type = "staff"

            # System object
            system = System()
            system.create_at = row["ts"]
            system.create_by = row["adm"]
            system.update_at = row["ts"]
            system.update_by = row["adm"]
            system.delete_at = row["delts"]
            system.delete_by = row["delby"]
            system.module = "staff"
            obj.system = system

            # Personal object
            personal = Personal()
            personal.full_name = row["name"]
            personal.nick_name = row.get("nick", "")
            personal.gender = row.get("sex", "")
            personal.birth_date = row.get("bday", "")
            personal.race = row.get("race", "")
            personal.religion = row.get("religion", "")
            personal.file_profile = row.get("file", "")
            personal.file_profile_path = "/content/staff/"
            personal.file_profile_url = (
                f"{self.root_url}/content/staff/{row['file']}"
                if row.get("file") else ""
            )
            personal.primary_phone = row["hp"]
            personal.primary_email = row["mel"]
            personal.citizen = row.get("citizen", "")
            personal.education = row.get("edulevel", "")
            personal.marital = row.get("marital", "")
            personal.birth_place = row.get("bstate", "")
            obj.personal = personal

            # Job object
            job = Job()
            job.designation = row.get("job", "")
            job.division = row.get("jobdiv", "")
            job.status = row.get("jobsta", "")
            job.grade = row.get("joblvl", "")
            job.start_date = row.get("jobstart", "")
            job.end_date = row.get("jobend", "")
            job.confirm_date = row.get("jobconfirm", "")
            job.contract_expiry = row.get("excontract", "")
            job.visa_expiry = row.get("exvisa", "")
            job.passport_expiry = row.get("expassport", "")
            job.permit_expiry = row.get("expermit", "")
            job.qualification = row.get("edulevel", "")
            obj.job = job

            self.total_data += 1
            total = self.total_data
            
            params.append(obj)

        return {"total_data": total, "message": "Staff list data fetched successfully", "data": params}

    async def get_filtered_staff(self,db, filter_data: dict, paginate_data: dict):
        staff_service = Staff(db=db)
        # Apply filter data
        for key, value in filter_data.items():
            if hasattr(staff_service, key):
                setattr(staff_service, key, value)
         # Apply pagination data
        for key, value in paginate_data.items():
            if hasattr(staff_service, key):
                setattr(staff_service, key, value)
        return await staff_service.staff_list()

   