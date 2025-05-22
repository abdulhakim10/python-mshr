# Python import
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import aiomysql
import json
from app.utils.error import ErrorHandler


# Main object for this class. Use plain object for flexible design.
# This object will be used fetch information.
class User:
    def __init__(self):
        self.id = None  # MongoDB id
        self.uid = None  # System defined user id
        self.app_code = None  # App code (client specific code)
        self.branch_id = None  # Branch ID
        self.id = None  # DB auto id
        self.ic = None  # Identity card / plate number
        self.name = None  # Fullname
        self.email = None  # Main email address
        self.phone = None  # Main mobile number
        self.user_no = None  # User defined user id (e.g., Staff no, student no)
        self.category = None  # Reserved: Category code
        self.category_name = None  # Reserved: Category name
        self.group = None  # Reserved: Group code
        self.group_name = None  # Reserved: Group name
        self.subgroup = None  # SubGroup code/name => client
        self.subgroup_name = None  # SubGroup name => client
        self.status = None  # Active, Terminate, Resigned
        self.status_name = None  # Status name
        self.is_delete = None  # Is record deleted
        self.system_level = None  # USER / ADMIN
        self.user_type = None  # CLIENT, VENDOR, FUNNEL, etc.


# end: User
class System:
    def __init__(self):
        self.create_at = None  # Date created
        self.create_by = None  # Created by
        self.update_at = None  # Date updated
        self.update_by = None  # Updated by
        self.delete_at = None  # Date deleted
        self.delete_by = None  # Deleted by
        self.module = None  # Module name
        self.firebase_id = None  # Firebase ID (if applicable)
        self.user_level = None  # User level (if applicable)


# end: System
class Job:
    def __init__(self):
        self.designation = None  # Name of the position => Programmer
        self.division = None  # Division of job => Sales, Finance
        self.status = None  # Status of job => Permanent, Contract, Part time
        self.level = None  # Level of Job => Executive, Assistant, BOD
        self.start_date = None  # Date start job
        self.end_date = None  # Date terminate or resign
        self.confirm_date = None  # Date of confirmation
        self.contract_expiry = None  # Date of contract expired
        self.visa_expiry = None  # Date of visa expired
        self.passport_expiry = None  # Date of passport expired
        self.permit_expiry = None  # Date of permit expired
        self.salary = None  # Salary
        self.company = None  # Company name
        self.specialization = None  # Job specialization
        self.grade = None  # Grade => 42, 52 (government)
        self.qualification = None  # Educational or professional qualification


# end: Job
class Personal:
    def __init__(self):
        self.full_name = None  # Full name (can match user.name)
        self.nick_name = None  # Nickname or salutation name => Dato Ali Abu Bakar
        self.gender = None  # 0 = Female, 1 = Male
        self.birth_date = None  # Date of birth
        self.race = None  # Race => Malay, Chinese
        self.religion = None  # Religion => Islam, etc.
        self.file_profile = None  # Profile file name or ID
        self.file_profile_path = None  # File path
        self.file_profile_url = None  # Public URL to file
        self.primary_phone = None  # Primary phone number
        self.secondary_phone = None  # Secondary phone number
        self.primary_email = None  # Primary email
        self.secondary_email = None  # Secondary email
        self.citizen = None  # Citizenship => Malaysian, etc.
        self.education = None  # Highest education level
        self.marital = None  # Marital status
        self.birth_place = None  # Place of birth (state or city)
        # Reserved / commented out attributes
        # self.nationality = None
        # self.salary = None
        # self.job_position = None
        # self.job_level = None


# end: Personal
class AddressData:
    def __init__(self):
        self.line1 = None  # Address line 1
        self.line2 = None  # Address line 2
        self.line3 = None  # Deprecated: merge with line2
        self.city = None  # City name
        self.postcode = None  # Postcode number
        self.state = None  # State name
        self.country = None  # Country name
        self.district = None  # Reserve


# end: AddressData
class Address:
    def __init__(self):
        self.main = AddressData()  # Home, Mailing, Company (depends on app)
        self.address2 = AddressData()  # Alternate address
        self.address3 = AddressData()  # Alternate address


# end: Address
class Education:
    def __init__(self):
        self.level = None  # PHD, Master, Degree, Diploma, SPM
        self.school = None  # Name of institution
        self.result = None  # Result or grade
        self.program = None  # Program or major
        self.year_end = None  # Year of completion
        self.achievement = None  # Awards or recognition
        self.scholarship = None  # Scholarship info
        self.year_start = None  # Year of enrollment
        self.end_reason = None  # Reason for ending
        self.state = None  # State of study
        self.country = None  # Country of study


# end: Education
class WorkExperience:
    def __init__(self):
        self.id = None  # Work experience row ID
        self.job = None  # Job title => Programmer, Accountant
        self.company = None  # Company name
        self.year_start = None  # Start year
        self.division = None  # Job division
        self.level = None  # Job level
        self.year_end = None  # End year (if applicable)


# end: WorkExperience
class Children:
    def __init__(self):
        self.ic = None  # IC or ID
        self.name = None  # Full name
        self.birth_date = None  # Date of birth
        self.school = None  # School/university or company


# end: Children
class Family:
    def __init__(self):
        self.spouse_name = None  # Spouse name
        self.spouse_ic = None  # Spouse IC or ID
        self.spouse_phone = None  # Spouse phone
        self.spouse_email = None  # Spouse email
        self.spouse_job = None  # Spouse occupation
        self.spouse_company = None  # Spouse company
        self.father_name = None  # Father's name
        self.mother_name = None  # Mother's name
        self.children = []  # List of Children objects


# end: Family
class Contact:
    def __init__(self):
        # self.main = Personal()  # Uncomment if needed in future
        self.contact2 = Personal()  # E.g., Technical, Emergency contact
        self.contact3 = Personal()  # E.g., Sales contact


# end: Contact
class Bank:
    def __init__(self):
        self.bank_name = None  # Bank name
        self.account_name = None  # Name on the account (Payee Name)
        self.account_number = None  # Bank account number
        self.branch_name = None  # Branch name (e.g., USJ, Subang Jaya)
        # self.swift_code = None      # SWIFT/BIC code (optional, currently unused)


# end: Bank
class BankInfo:
    def __init__(self):
        self.id = None  # MongoDB ID or main ID
        self.uid = None  # Unique user ID
        self.main = Bank()  # Main bank info
        self.bank2 = Bank()  # Secondary bank info
        self.bank3 = Bank()  # Tertiary bank info


# end: BankInfo

# Object schema for Create/Update/Delete.
# Use the Pydantic model for validation and serialization.


class UserSchema(BaseModel):
    # id: Optional[str] = Field(
    #     default=None, title="MongoDB ID", description="MongoDB object ID"
    # )
    uid: Optional[str] = Field(
        default=None, title="UID", description="System-defined user ID"
    )
    # app_code: Optional[str] = Field(
    #     default=None, title="App Code", description="App/client code"
    # )
    branch_id: Optional[str] = Field(
        default=None, title="Branch ID", description="Branch identifier"
    )
    id: Optional[str] = Field(
        default=None, title="DB ID", description="Database auto-increment ID"
    )
    ic: Optional[str] = Field(
        default=None, title="IC", description="Identity card or plate number"
    )
    name: Optional[str] = Field(
        default=None, title="Full Name", description="Full user name"
    )
    email: Optional[str] = Field(
        default=None, title="Email", description="Main email address"
    )
    phone: Optional[str] = Field(
        default=None, title="Phone", description="Main mobile number"
    )
    user_no: Optional[str] = Field(
        default=None,
        title="User Number",
        description="User-defined number (e.g., staff ID)",
    )
    category: Optional[str] = Field(
        default=None, title="Category", description="Category code"
    )
    category_name: Optional[str] = Field(
        default=None, title="Category Name", description="Name of the category"
    )
    group: Optional[str] = Field(default=None, title="Group", description="Group code")
    group_name: Optional[str] = Field(
        default=None, title="Group Name", description="Name of the group"
    )
    subgroup: Optional[str] = Field(
        default=None, title="Subgroup", description="Subgroup code"
    )
    subgroup_name: Optional[str] = Field(
        default=None, title="Subgroup Name", description="Subgroup name"
    )
    status: Optional[str] = Field(
        default=None, title="Status", description="User status"
    )
    status_name: Optional[str] = Field(
        default=None, title="Status Name", description="Status description"
    )
    is_delete: Optional[str] = Field(
        default=None, title="Is Deleted", description="Soft delete flag"
    )
    login_status: Optional[str] = Field(
        default=None, title="Login Status", description="Login status"
    )
    system_level: Optional[str] = Field(
        default=None, title="System Level", description="USER / ADMIN"
    )
    # user_type: Optional[str] = Field(
    #     default=None, title="User Type", description="CLIENT, VENDOR, FUNNEL, etc."
    # )


# end: UserSchema


class FilterSchema(BaseModel):
    filter_branch_id: Optional[str] = "0"
    filter_delete: Optional[str] = ""
    filter_search: Optional[str] = ""
    filter_division: Optional[str] = ""
    filter_position: Optional[str] = ""
    filter_status: Optional[str] = ""
    filter_gender: Optional[str] = ""
    filter_user_status: Optional[str] = ""
    page_order: Optional[str] = "id"
    page_sort: Optional[str] = "desc"
    page_limit: Optional[int] = 10
    page_start: Optional[int] = 1


class SystemSchema(BaseModel):
    create_at: Optional[datetime] = Field(
        default=None, title="Created At", description="Creation date"
    )
    create_by: Optional[str] = Field(
        default=None, title="Created By", description="Creator ID"
    )
    update_at: Optional[datetime] = Field(
        default=None, title="Updated At", description="Last update date"
    )
    update_by: Optional[str] = Field(
        default=None, title="Updated By", description="Last updated by"
    )
    delete_at: Optional[datetime] = Field(
        default=None, title="Deleted At", description="Deletion date"
    )
    delete_by: Optional[str] = Field(
        default=None, title="Deleted By", description="Deleted by user"
    )
    module: Optional[str] = Field(
        default=None, title="Module", description="Module name"
    )
    firebase_id: Optional[str] = Field(
        default=None, title="Firebase ID", description="Firebase identifier"
    )
    user_level: Optional[str] = Field(
        default=None, title="User Level", description="User permission level"
    )


# end: SystemSchema
class JobSchema(BaseModel):
    designation: Optional[str] = Field(
        default=None, title="Designation", description="Job title"
    )
    division: Optional[str] = Field(
        default=None, title="Division", description="Job division"
    )
    status: Optional[str] = Field(
        default=None, title="Status", description="Employment status"
    )
    level: Optional[str] = Field(default=None, title="Level", description="Job level")
    start_date: Optional[str] = Field(
        default=None, title="Start Date", description="Start of employment"
    )
    end_date: Optional[str] = Field(
        default=None, title="End Date", description="End of employment"
    )
    confirm_date: Optional[str] = Field(
        default=None, title="Confirmation Date", description="Confirmation date"
    )
    contract_expiry: Optional[str] = Field(
        default=None, title="Contract Expiry", description="Contract expiration date"
    )
    visa_expiry: Optional[str] = Field(
        default=None, title="Visa Expiry", description="Visa expiration"
    )
    passport_expiry: Optional[str] = Field(
        default=None, title="Passport Expiry", description="Passport expiration"
    )
    permit_expiry: Optional[str] = Field(
        default=None, title="Permit Expiry", description="Permit expiration"
    )
    salary: Optional[float] = Field(
        default=None, title="Salary", description="Monthly salary"
    )
    company: Optional[str] = Field(
        default=None, title="Company", description="Company name"
    )
    specialization: Optional[str] = Field(
        default=None, title="Specialization", description="Job specialization"
    )
    grade: Optional[str] = Field(default=None, title="Grade", description="Job grade")
    qualification: Optional[str] = Field(
        default=None, title="Qualification", description="Educational qualification"
    )


# end: JobSchema
class PersonalSchema(BaseModel):
    full_name: Optional[str] = Field(
        default=None, title="Full Name", description="Person's full name"
    )
    nick_name: Optional[str] = Field(
        default=None, title="Nick Name", description="Nickname or salutation"
    )
    gender: Optional[str] = Field(
        default=None, title="Gender", description="0 = Female, 1 = Male"
    )
    birth_date: Optional[str] = Field(
        default=None, title="Birth Date", description="Date of birth"
    )
    race: Optional[str] = Field(
        default=None, title="Race", description="Race or ethnicity"
    )
    religion: Optional[str] = Field(
        default=None, title="Religion", description="Religion"
    )
    file_profile: Optional[str] = Field(
        default=None, title="Profile File", description="Profile file name or ID"
    )
    file_profile_path: Optional[str] = Field(
        default=None, title="Profile Path", description="Path to profile file"
    )
    file_profile_url: Optional[str] = Field(
        default=None, title="Profile URL", description="Public profile image URL"
    )
    primary_phone: Optional[str] = Field(
        default=None, title="Primary Phone", description="Primary phone number"
    )
    secondary_phone: Optional[str] = Field(
        default=None, title="Secondary Phone", description="Secondary phone"
    )
    primary_email: Optional[str] = Field(
        default=None, title="Primary Email", description="Main email address"
    )
    secondary_email: Optional[str] = Field(
        default=None, title="Secondary Email", description="Backup email address"
    )
    citizen: Optional[str] = Field(
        default=None, title="Citizenship", description="Citizenship status"
    )
    education: Optional[str] = Field(
        default=None, title="Education", description="Highest education level"
    )
    marital: Optional[str] = Field(
        default=None, title="Marital Status", description="Marital status"
    )
    birth_place: Optional[str] = Field(
        default=None, title="Birth Place", description="Place of birth (state/city)"
    )
    # Reserved / commented out attributes


class AddressDataSchema(BaseModel):
    line1: Optional[str] = Field(
        default=None, title="Address Line 1", description="Address line 1"
    )
    line2: Optional[str] = Field(
        default=None, title="Address Line 2", description="Address line 2"
    )
    line3: Optional[str] = Field(
        default=None, title="Address Line 3", description="Deprecated: merge with line2"
    )
    city: Optional[str] = Field(default=None, title="City", description="City name")
    postcode: Optional[str] = Field(
        default=None, title="Postcode", description="Postcode number"
    )
    state: Optional[str] = Field(default=None, title="State", description="State name")
    country: Optional[str] = Field(
        default=None, title="Country", description="Country name"
    )
    district: Optional[str] = Field(
        default=None, title="District", description="Reserved"
    )


# end: AddressDataSchema
class AddressSchema(BaseModel):
    main: Optional[AddressDataSchema] = Field(
        default=None, title="Main Address", description="Home, Mailing, Company address"
    )
    address2: Optional[AddressDataSchema] = Field(
        default=None, title="Alternate Address 1", description="Alternate address"
    )
    address3: Optional[str] = Field(
        default=None, title="Alternate Address 2", description="Alternate address"
    )


# end: AddressSchema
class EducationSchema(BaseModel):
    level: Optional[str] = Field(
        default=None, title="Level", description="Education level"
    )
    school: Optional[str] = Field(
        default=None, title="School", description="Institution name"
    )
    result: Optional[str] = Field(
        default=None, title="Result", description="Grade or result"
    )
    program: Optional[str] = Field(
        default=None, title="Program", description="Program or major"
    )
    year_start: Optional[int] = Field(
        default=None, title="Year Start", description="Year of enrollment"
    )
    year_end: Optional[int] = Field(
        default=None, title="Year End", description="Year of completion"
    )
    achievement: Optional[str] = Field(
        default=None, title="Achievement", description="Awards or recognition"
    )
    scholarship: Optional[str] = Field(
        default=None, title="Scholarship", description="Scholarship info"
    )
    end_reason: Optional[str] = Field(
        default=None, title="End Reason", description="Reason for ending"
    )
    state: Optional[str] = Field(
        default=None, title="State", description="State of study"
    )
    country: Optional[str] = Field(
        default=None, title="Country", description="Country of study"
    )


# end: EducationSchema
class WorkExperienceSchema(BaseModel):
    id: Optional[str] = Field(
        default=None, title="ID", description="Work experience ID"
    )
    job: Optional[str] = Field(default=None, title="Job", description="Job title")
    company: Optional[str] = Field(
        default=None, title="Company", description="Company name"
    )
    year_start: Optional[int] = Field(
        default=None, title="Start Year", description="Year started"
    )
    year_end: Optional[int] = Field(
        default=None, title="End Year", description="Year ended"
    )
    division: Optional[str] = Field(
        default=None, title="Division", description="Job division"
    )
    level: Optional[str] = Field(default=None, title="Level", description="Job level")


# end: WorkExperienceSchema
class ChildrenSchema(BaseModel):
    ic: Optional[str] = Field(default=None, title="IC", description="IC or ID")
    name: Optional[str] = Field(default=None, title="Name", description="Full name")
    birth_date: Optional[datetime] = Field(
        default=None, title="Birth Date", description="Date of birth"
    )
    school: Optional[str] = Field(
        default=None, title="School", description="School, university, or company"
    )


# end: ChildrenSchema


class FamilySchema(BaseModel):
    spouse_name: Optional[str] = Field(
        default=None, title="Spouse Name", description="Name of the spouse"
    )
    spouse_ic: Optional[str] = Field(
        default=None, title="Spouse IC", description="IC or ID of the spouse"
    )
    spouse_phone: Optional[str] = Field(
        default=None, title="Spouse Phone", description="Phone number of the spouse"
    )
    spouse_email: Optional[str] = Field(
        default=None, title="Spouse Email", description="Email of the spouse"
    )
    spouse_job: Optional[str] = Field(
        default=None, title="Spouse Job", description="Occupation of the spouse"
    )
    spouse_company: Optional[str] = Field(
        default=None, title="Spouse Company", description="Company of the spouse"
    )
    father_name: Optional[str] = Field(
        default=None, title="Father Name", description="Father's name"
    )
    mother_name: Optional[str] = Field(
        default=None, title="Mother Name", description="Mother's name"
    )
    children: Optional[list[ChildrenSchema]] = Field(
        default=None, title="Children", description="List of children"
    )


# end: FamilySchema
class ContactSchema(BaseModel):
    contact2: Optional[PersonalSchema] = Field(
        default=None, title="Contact 2", description="Technical or emergency contact"
    )
    contact3: Optional[PersonalSchema] = Field(
        default=None, title="Contact 3", description="Sales contact"
    )


# end: ContactSchema
class BankSchema(BaseModel):
    bank_name: Optional[str] = Field(
        default=None, title="Bank Name", description="Bank name"
    )
    account_name: Optional[str] = Field(
        default=None, title="Account Name", description="Payee or account holder's name"
    )
    account_number: Optional[str] = Field(
        default=None, title="Account Number", description="Bank account number"
    )
    branch_name: Optional[str] = Field(
        default=None, title="Branch Name", description="Name of the bank branch"
    )


# end: BankSchema
class BankInfoSchema(BaseModel):
    id: Optional[str] = Field(
        default=None, title="ID", description="MongoDB ID or main ID"
    )
    uid: Optional[str] = Field(
        default=None, title="User ID", description="Unique user ID"
    )
    main: Optional[BankSchema] = Field(
        default=None, title="Main Bank", description="Main bank info"
    )
    bank2: Optional[BankSchema] = Field(
        default=None, title="Bank 2", description="Secondary bank info"
    )
    bank3: Optional[BankSchema] = Field(
        default=None, title="Bank 3", description="Tertiary bank info"
    )


# end: BankInfoSchema
# The main processor class for this module.
# This class will be used to process the request and response.
class UserProfile(
    User,
    System,
    Job,
    Personal,
    AddressData,
    Address,
    Education,
    WorkExperience,
    Children,
    Family,
    Contact,
    Bank,
    BankInfo,
):
    # Declare direct main table for this class.
    # This table will be used for all the CRUD operation automatically
    main_table = "usr"

    def __init__(self, db):
        self.err_id = None  # Initialize err_id attribute
        self.Err = (
            ErrorHandler()
        )  # Initialize Err attribute (ensure it's set later or inherited)
        self.total_count = 0  # Initialize total_count attribute
        self.total_data = 0  # Initialize total_data attribute
        self.db = db
        # self.sysuser = sysuser

    # Map the "main_table" fields with object in this module.
    # Important for easy manage. Single place to change the table operation
    def _main_table_mapping(
        self,
        request: UserSchema,
        address: AddressSchema,
        personal: PersonalSchema,
        job: JobSchema,
        system: SystemSchema,
        family: FamilySchema,
    ):
        """Map the fields of the main table to the object fields."""

        return {
            "uid": request.uid,
            "id": request.id,
            "sch_id": request.branch_id,
            "name": request.name,
            "ic": request.ic,
            "hp": request.phone,
            "mel": request.email,
            "syslevel": request.system_level,
            "jobdiv": job.division,
            "jobsta": job.status,
            "login_sta": request.login_status,
            "login_ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "login_period": datetime("%Y-%m-%d %H:%M:%S"),
            "resettokenexpiration": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "password_set": "1",
            "status": request.status,
            "ts": system.create_at,
            "adm": system.create_by,
            "delts": system.delete_at,
            "delby": system.delete_by,
            "nick": personal.nick_name,
            "sex": personal.gender,
            "bday": personal.birth_date,
            "race": personal.race,
            "religion": personal.religion,
            "file": personal.file_profile,
            "isdel": request.is_delete,
            "citizen": personal.citizen,
            "edulevel": personal.education,
            "marital": personal.marital,
            "bstate": personal.birth_place,
            "job": job.designation,
            "joblvl": job.level,
            "jobstart": job.start_date,
            "jobend": job.end_date,
            "jobconfirm": job.confirm_date,
            "excontract": job.contract_expiry,
            "exvisa": job.visa_expiry,
            "expassport": job.passport_expiry,
            "expermit": job.permit_expiry,
            "addr": address.main.line1,
            "addr1": address.main.line2,
            "addr2": address.main.line3,
            "city": address.main.city,
            "pcode": address.main.postcode,
            "state": address.main.state,
            "country": address.main.country,
            "mailaddr": address.address2.line1,
            "mailaddr2": address.address2.line2,
            "mailaddr3": address.address2.line3,
            "mailcity": address.address2.city,
            "mailpcode": address.address2.postcode,
            "mailstate": address.address2.state,
            "mailcountry": address.address2.country,
            "spname": family.spouse_name,
            "spic": family.spouse_ic,
            "spjob": family.spouse_job,
            "spcomp": family.spouse_company,
            "sptel": family.spouse_phone,
            "json_data": json.dumps({"father_name": family.father_name, "mother_name": family.mother_name}),
        } 

    # end: _main_table_mapping

    def to_dict(self, obj):
        """Helper to safely convert custom objects to a dictionary."""
        if hasattr(obj, "__dict__"):
            return {
                k: (self.to_dict(v) if hasattr(v, "__dict__") else v)
                for k, v in obj.__dict__.items()
                if not k.startswith("_")
            }
        elif isinstance(obj, list):
            return [self.to_dict(item) for item in obj]
        return obj

    async def _return_true(self, message, data=None):
        return {
            "success": True,
            "message": message,
            "status_code": 200,
            "data": data,
        }

    async def _return_false(self, message, error=None, data=None):
        return {
            "success": False,
            "message": message,
            "status_code": 400 if not error else 500,
            "error": error,
            "data": self.to_dict(data) if data else None,
        }

    async def fetch_user(self, request: FilterSchema):
        filters = []
        params = {}

        # Filtering
        filters.append("isdel = %(isdel)s")
        params["isdel"] = (
            request.filter_delete if request.filter_delete is not None else 0
        )

        if request.filter_branch_id:
            filters.append("sch_id = %(branch_id)s")
            params["branch_id"] = request.filter_branch_id
        if request.filter_division:
            filters.append("jobdiv = %(division)s")
            params["division"] = request.filter_division
        if request.filter_position:
            filters.append("job = %(position)s")
            params["position"] = request.filter_position
        if request.filter_status:
            filters.append("jobsta = %(status)s")
            params["status"] = request.filter_status
        if request.filter_gender:
            filters.append("sex = %(gender)s")
            params["gender"] = request.filter_gender
        if request.filter_user_status:
            filters.append("status = %(user_status)s")
            params["user_status"] = request.filter_user_status

        if request.filter_search:
            filters.append(
                """(name LIKE %(search)s OR ic LIKE %(search)s OR mel LIKE %(search)s)"""
            )
            params["search"] = f"%{request.filter_search}%"

        # Compose WHERE clause
        where_clause = "WHERE " + " AND ".join(filters) if filters else ""

        # Sorting and pagination
        sort_column = request.page_order or "id"
        sort_direction = request.page_sort or "DESC"
        order_clause = f"ORDER BY {sort_column} {sort_direction}"

        limit = request.page_limit or 10
        offset = (request.page_start - 1) * limit if request.page_start else 0

        params["limit"] = limit
        params["offset"] = offset

        limit_offset_clause = "LIMIT %(limit)s OFFSET %(offset)s"

        total_users_sql = """
            SELECT COUNT(*) AS total_staff_count FROM usr WHERE isdel = 0 AND status = 0 AND sch_id = %s"""
        sql_data = f"""
            SELECT uid, id, sch_id, name, ic, hp, mel, syslevel, jobdiv, jobsta, status, ts, adm, delts, delby,
                   nick, sex, bday, race, religion, file, citizen, edulevel, marital, bstate,
                   job, joblvl, jobstart, jobend, jobconfirm, excontract, exvisa, expassport, expermit,
                   isdel, addr, addr1, addr2, city, pcode, state, country,
                   mailaddr, mailaddr2, mailaddr3, mailcity, mailpcode, mailstate, mailcountry, spname, spic, spjob, spcomp, sptel, spjob, json_data
            FROM usr
            {where_clause}
            {order_clause}
            {limit_offset_clause}
        """
        # try:
        #     async with self.db.cursor(aiomysql.DictCursor) as cursor:
        #         await cursor.execute(sql_data, params)
        #         result = await cursor.fetchall()
        try:
            async with self.db.cursor(aiomysql.DictCursor) as cursor:
                # Execute the total count query
                await cursor.execute(total_users_sql, (request.filter_branch_id,))
                total_result = await cursor.fetchone()
                total_count = total_result["total_staff_count"]

                # Now execute the data query
                await cursor.execute(sql_data, params)
                result = await cursor.fetchall()

            if not result:
                return await self._return_false(message="Record not found")

            users = []

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
                obj.status = row["status"] if row["status"] else 0
                obj.is_delete = row["isdel"]
                obj.system_level = row["syslevel"] if row["syslevel"] else ""
                obj.user_type = "sataff"
                obj.system = System()
                obj.system.create_at = row["ts"]
                obj.system.create_by = row["adm"]
                obj.system.update_at = row["ts"]
                obj.system.update_by = row["adm"]
                obj.system.delete_at = row["delts"]
                obj.system.delete_by = row["delby"]
                obj.system.module = "staff"
                obj.system.firebase_id = ""
                obj.system.user_level = ""

                obj.personal = Personal()
                obj.personal.full_name = row["name"]
                obj.personal.nick_name = row["nick"]
                obj.personal.gender = row["sex"]
                obj.personal.birth_date = row["bday"]
                obj.personal.race = row["race"]
                obj.personal.religion = row["religion"]
                obj.personal.file_profile = row["file"]
                obj.personal.file_profile_path = "/content/staff/"
                obj.personal.file_profile_url = row["file"] if row["file"] else ""
                obj.personal.primary_phone = row["hp"]
                obj.personal.secondary_phone = "<reserved>"
                obj.personal.primary_email = row["mel"]
                obj.personal.secondary_email = "<reserved>"
                obj.personal.citizen = row["citizen"]
                obj.personal.education = row["edulevel"]
                obj.personal.marital = row["marital"]
                obj.personal.birth_place = row["bstate"]

                obj.job = Job()
                obj.job.designation = row["job"]
                obj.job.division = row["jobdiv"]
                obj.job.status = row["jobsta"]
                obj.job.level = "<reserved>"
                obj.job.grade = row["joblvl"]
                obj.job.start_date = row["jobstart"]
                obj.job.end_date = row["jobend"]
                obj.job.confirm_date = row["jobconfirm"]
                obj.job.contract_expiry = row["excontract"]
                obj.job.visa_expiry = row["exvisa"]
                obj.job.passport_expiry = row["expassport"]
                obj.job.permit_expiry = row["expermit"]
                obj.job.salary = "<reserved>"
                obj.job.specialization = "<reserved>"
                obj.job.qualification = row["edulevel"]
                obj.address = Address()
                obj.address.main = AddressData()
                obj.address.main.line1 = row["addr"]
                obj.address.main.line2 = row["addr1"]
                obj.address.main.line3 = row["addr2"]
                obj.address.main.city = row["city"]
                obj.address.main.postcode = row["pcode"]
                obj.address.main.state = row["state"]
                obj.address.main.country = row["country"]
                obj.address.address2 = AddressData()
                obj.address.address2.line1 = row["mailaddr"]
                obj.address.address2.line2 = row["mailaddr2"]
                obj.address.address2.line3 = row["mailaddr3"]
                obj.address.address2.city = row["mailcity"]
                obj.address.address2.postcode = row["mailpcode"]
                obj.address.address2.state = row["mailstate"]
                obj.address.address2.country = row["mailcountry"]
                obj.address.address2.district = "<reserved>"
                obj.address.address3 = "<reserved>"
                # education
                obj.family = Family()
                obj.family.spouse_name = row["spname"]
                obj.family.spouse_ic = row["spic"]
                obj.family.spouse_job = row["spjob"]
                obj.family.spouse_company = row["spcomp"]
                obj.family.spouse_phone = row["sptel"]
                obj.family.spouse_email = "<reserved>"
                json_data = row["json_data"]
                if json_data:
                    try:
                        jd = json.loads(json_data)
                        obj.family.father_name = jd.get("father_name", "") or ""
                        obj.family.mother_name = jd.get("mother_name", "") or ""
                    except json.JSONDecodeError:
                        pass
                obj.family.children = []
                # Append data
                users.append(obj)
                self.total_count = total_count
                self.total_data = len(users)

                # print(users)

            return await self._return_true(
                message="Staff list data fetched successfully",
                data={
                    "total_count": self.total_count,
                    "total_data": self.total_data,
                    "data": users,
                },
            )

        except (ValueError, KeyError) as e:
            self.err_id = str(e)
            return await self._return_false(
                message="Internal Server Error", error=str(e)
            )

    async def create_user(
        self,
        request: UserSchema,
        address: AddressSchema,
        personal: PersonalSchema,
        job: JobSchema,
        system: SystemSchema,
        family: FamilySchema
    ):
        # Map the request data to the main table
        data = self._main_table_mapping(request, address, personal, job, system, family)
        # Insert the data into the database
        sql = f"""
            INSERT INTO {self.main_table} ({', '.join(data.keys())})
            VALUES ({', '.join(['%s'] * len(data))})
        """
        # "INSERT INTO usr (uid, pass, " . implode(', ', $columns) . ") VALUES ('$uid', md5('12345'),'" . implode("','", $values) . "')";
        try:
            async with self.db.cursor() as cursor:
                await cursor.execute(sql, tuple(data.values()))
                await self.db.commit()
                return await self._return_true(
                    message="User created successfully", data=data
                )
        except Exception as e:
            self.err_id = str(e)
            return await self._return_false(
                message="Failed to create user", error=str(e)
            )