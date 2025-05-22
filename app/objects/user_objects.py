class User:
    def __init__(self):
        self._id = None            # MongoDB id
        self.uid = None            # System defined user id
        self.app_code = None       # App code (client specific code)
        self.branch_id = None      # Branch ID
        self.id = None             # DB auto id
        self.ic = None             # Identity card / plate number
        self.name = None           # Fullname
        self.email = None          # Main email address
        self.phone = None          # Main mobile number
        self.user_no = None        # User defined user id (e.g., Staff no, student no)
        self.category = None       # Reserved: Category code
        self.category_name = None  # Reserved: Category name
        self.group = None          # Reserved: Group code
        self.group_name = None     # Reserved: Group name
        self.subgroup = None       # SubGroup code/name => client
        self.subgroup_name = None  # SubGroup name => client
        self.status = None         # Active, Terminate, Resigned
        self.status_name = None    # Status name
        self.is_delete = None      # Is record deleted
        self.system_level = None   # USER / ADMIN
        self.user_type = None      # CLIENT, VENDOR, FUNNEL, etc.

class System:
    def __init__(self):
        self.create_at = None      # Date created
        self.create_by = None      # Created by
        self.update_at = None      # Date updated
        self.update_by = None      # Updated by
        self.delete_at = None      # Date deleted
        self.delete_by = None      # Deleted by
        self.module = None         # Module name
        self.firebase_id = None  # Firebase ID (if applicable)
        self.user_level = None      # User level (if applicable)

class Job:
    def __init__(self):
        self.designation = None      # Name of the position => Programmer
        self.division = None         # Division of job => Sales, Finance
        self.status = None           # Status of job => Permanent, Contract, Part time
        self.level = None            # Level of Job => Executive, Assistant, BOD
        self.start_date = None       # Date start job
        self.end_date = None         # Date terminate or resign
        self.confirm_date = None     # Date of confirmation
        self.contract_expiry = None  # Date of contract expired
        self.visa_expiry = None      # Date of visa expired
        self.passport_expiry = None  # Date of passport expired
        self.permit_expiry = None    # Date of permit expired
        self.salary = None           # Salary
        self.company = None          # Company name
        self.specialization = None   # Job specialization
        self.grade = None            # Grade => 42, 52 (government)
        self.qualification = None    # Educational or professional qualification

class Personal:
    def __init__(self):
        self.full_name = None         # Full name (can match user.name)
        self.nick_name = None         # Nickname or salutation name => Dato Ali Abu Bakar
        self.gender = None            # 0 = Female, 1 = Male
        self.birth_date = None        # Date of birth
        self.race = None              # Race => Malay, Chinese
        self.religion = None          # Religion => Islam, etc.
        self.file_profile = None      # Profile file name or ID
        self.file_profile_path = None # File path
        self.file_profile_url = None  # Public URL to file
        self.primary_phone = None     # Primary phone number
        self.secondary_phone = None   # Secondary phone number
        self.primary_email = None     # Primary email
        self.secondary_email = None   # Secondary email
        self.citizen = None           # Citizenship => Malaysian, etc.
        self.education = None         # Highest education level
        self.marital = None           # Marital status
        self.birth_place = None       # Place of birth (state or city)
        # Reserved / commented out attributes
        # self.nationality = None
        # self.salary = None
        # self.job_position = None
        # self.job_level = None

class AddressData:
    def __init__(self):
        self.line1 = None          # Address line 1
        self.line2 = None          # Address line 2
        self.line3 = None          # Deprecated: merge with line2
        self.city = None           # City name
        self.postcode = None       # Postcode number
        self.state = None          # State name
        self.country = None        # Country name
        self.district = None       # Reserve


class Address:
    def __init__(self):
        self.main = AddressData()     # Home, Mailing, Company (depends on app)
        self.address2 = AddressData() # Alternate address
        self.address3 = AddressData() # Alternate address

class Education:
    def __init__(self):
        self.level = None         # PHD, Master, Degree, Diploma, SPM
        self.school = None        # Name of institution
        self.result = None        # Result or grade
        self.program = None       # Program or major
        self.year_end = None      # Year of completion
        self.achievement = None   # Awards or recognition
        self.scholarship = None   # Scholarship info
        self.year_start = None    # Year of enrollment
        self.end_reason = None    # Reason for ending
        self.state = None         # State of study
        self.country = None       # Country of study

class WorkExperience:
    def __init__(self):
        self.id = None            # Work experience row ID
        self.job = None           # Job title => Programmer, Accountant
        self.company = None       # Company name
        self.year_start = None    # Start year
        self.division = None      # Job division
        self.level = None         # Job level
        self.year_end = None      # End year (if applicable)

class Children:
    def __init__(self):
        self.ic = None            # IC or ID
        self.name = None          # Full name
        self.birth_date = None    # Date of birth
        self.school = None        # School/university or company


class Family:
    def __init__(self):
        self.spouse_name = None      # Spouse name
        self.spouse_ic = None        # Spouse IC or ID
        self.spouse_phone = None     # Spouse phone
        self.spouse_email = None     # Spouse email
        self.spouse_job = None       # Spouse occupation
        self.spouse_company = None   # Spouse company
        self.father_name = None      # Father's name
        self.mother_name = None      # Mother's name
        self.children = []           # List of Children objects

class Contact:
    def __init__(self):
        # self.main = Personal()  # Uncomment if needed in future
        self.contact2 = Personal()  # E.g., Technical, Emergency contact
        self.contact3 = Personal()  # E.g., Sales contact

class Bank:
    def __init__(self):
        self.bank_name = None         # Bank name
        self.account_name = None      # Name on the account (Payee Name)
        self.account_number = None    # Bank account number
        self.branch_name = None       # Branch name (e.g., USJ, Subang Jaya)
        # self.swift_code = None      # SWIFT/BIC code (optional, currently unused)


class BankInfo:
    def __init__(self):
        self._id = None               # MongoDB ID or main ID
        self.uid = None               # Unique user ID
        self.main = Bank()            # Main bank info
        self.bank2 = Bank()           # Secondary bank info
        self.bank3 = Bank()           # Tertiary bank info

# {
#   "id": "30",
#   "uid": "21052025",
#   "branch_id": "0",
#   "ic": "20250521",
#   "name": "Test User",
#   "email": "test@email.com",
#   "phone": "234567890",
#   "user_no": "",
#   "category": "",
#   "category_name": "",
#   "group": "A",
#   "group_name": "ML",
#   "subgroup": "",
#   "subgroup_name": "sting",
#   "status": "0",
#   "status_name": "",
#   "is_delete": "0",
#   "login_status": "0",
#   "system_level": "ACL01",
# }