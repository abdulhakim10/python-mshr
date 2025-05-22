from async_database import AsyncDatabase
from logger import Logger

import re

class Coa:
    vername = "Coa"
    version = "1.0.0"
    verdate = "250222"

    def __init__(self,db: AsyncDatabase, user_config=None):
        
        self.status = None
        self.message = None
        self.data = []
        self.total_data = 0
        self.total_record = 0

        self.db = db
        self.sysuser = user_config
        self.logger = Logger(filename="finance")

        self.sql_filters = None
        self.sql_params = []
        self.sql_conditions = []
        self.sql_debug = None
        self.sql_count = None
        self.sql_data = None
        self.sql_sort = None
        self.sql_limit = None
        self.sql_offset = None

        

    def _reset_data(self):
        self.data = []
        self.total_data = 0
        self.total_record = 0
        self.sql_filters = None
        self.sql_params = []
        self.sql_conditions = []
        self.sql_debug = []
        self.sql_count = None
        self.sql_data = None
        self.sql_sort = None
        return True

    async def _return_true(self, message=None):
        self.status = "success"
        self.message = message
        return True

    async def _return_false(self, message=None):
        self.status = "error"
        self.message = message
        await self.logger.error(f"appcode:{self.sysuser.appcode} uid:{self.sysuser.uid} message:{self.message}")
        return False

    async def _prepare_sql(self, filter):
        for attr, sql in self.sql_filters.items():
            value = getattr(filter, attr, None)
            if value:
                self.sql_conditions.append(sql)
                self.sql_params.append(value if attr != "search" else f"%{value}%")

        if not filter.id and not filter.code:
            if filter.deleted:
                self.sql_conditions += ("isdel=%s",)
                self.sql_params += (1,)
            elif filter.deactivated:
                self.sql_conditions += ("isdel=%s",)
                self.sql_params += (2,)
            else:
                self.sql_conditions += ("isdel=%s",)
                self.sql_params += (0,)

            if self.sysuser.branch:
                self.sql_conditions += ("(sid=0 OR sid=%s)",)
                self.sql_params += (self.sysuser.branch,)
            else:
                if filter.branch is not None and filter.branch != '':
                    self.sql_conditions += ("(sid=0 OR sid=%s)",)
                    self.sql_params += (filter.branch,)

        if self.sql_conditions:
            condition_str = " AND ".join(self.sql_conditions)

            if "WHERE" in self.sql_count.upper():
                self.sql_count += " AND " + condition_str
            else:
                self.sql_count += " WHERE " + condition_str

            if "WHERE" in self.sql_data.upper():
                self.sql_data += " AND " + condition_str
            else:
                self.sql_data += " WHERE " + condition_str

        if self.sql_sort:
            self.sql_data += self.sql_sort

        self.sql_debug = self.sql_data % tuple(map(repr, self.sql_params))
        return True

    async def _generate_account_code(self, branch=None):
        if branch is None:
            return await self._return_false(message="Missing branch")

        try:
            await self.db.begin()

            sql = "SELECT accno FROM sch WHERE id = %s FOR UPDATE"
            result = await self.db.execute_fetch(sql, (branch,))

            if result:
                accno = (result[0]['accno'] or 0) + 1
                code = f"{branch}{int(accno):06d}"

                sql_check = "SELECT COUNT(*) as info FROM fin_coa_type WHERE code = %s"
                existing_code = await self.db.fetch_info(sql_check, (code,))
                if existing_code > 0:
                    await self.db.rollback()
                    return await self._return_false("Account code already exists")

                sql_check = "SELECT COUNT(*) as info FROM fin_coa_item WHERE code = %s"
                existing_code = await self.db.fetch_info(sql_check, (code,))
                if existing_code > 0:
                    await self.db.rollback()
                    return await self._return_false("Account code already exists")

                sql_update = "UPDATE sch SET accno = %s WHERE id = %s"
                await self.db.execute_query(sql_update, (accno, branch))

                await self.db.commit()
                await self.logger.info(f"Generated account code: {code} for branch {branch}")
                return code
            else:
                await self.db.rollback()
                return await self._return_false(message=f"Branch {branch} not found.")
        except Exception as e:
            await self.db.rollback()
            return await self._return_false(message=f"Database error: {e}")


    def clean_object_value(self, obj, clean_all=None):
        for key, value in obj.__dict__.items():
            # clean_all = This will set any falsy value (like 0, "", [], False) to None.
            if clean_all:
                if not value:
                    setattr(obj, key, None)
            # else = This will keep 0
            else:
                if value == '' or value is None:
                    setattr(obj, key, None)

