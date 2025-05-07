class DataFilter:
    def __init__(self):
        self.filter_uid = None                # user data by uid
        self.filter_delete = None            # list deleted data
        self.filter_all_year = None          # bypass date filters
        self.filter_branch_id = None         # list by center id
        self.filter_start_date = None        # list by start date
        self.filter_end_date = None          # list by end date
        self.filter_search = None            # search by name, tid, ref
        self.filter_division = None          # filter by division
        self.filter_position = None          # filter by position
        self.filter_status = None            # filter by status
        self.filter_gender = None            # filter by gender
        self.filter_user_status = None       # filter by user status
        self.filter_date = None              # custom filter by exact date
        # self.filter_unpaid = None          # you can add this if needed later

class DataPaginate:
    def __init__(self):
        self.page_limit = None     # Limit number of rows, e.g. 10
        self.page_start = None     # Offset, e.g. start from row 20
        self.page_order = None     # Column to order by, e.g. "id"
        self.page_sort = None      # Sort direction: "asc" or "desc"
        self.form_type = None      # Optional: could be used to vary pagination behavior

class StandardProperties:
    version = "0.1"      # Class version number (static)
    verdate = "231130"   # Class version date (static)

    def __init__(self):
        self.user_id = None           # ID of the user accessing the class
        self.branch_id = None         # Branch ID
        self.user_branch_id = None    # User's branch ID
        self.app_name = None          # Application name
        self.root_url = None          # Root URL
        self.host = None              # Hostname
        self.sys_dir = None           # System directory path
        self.system_level = None      # Access level
        self.system_access = None     # Access permissions
        self.company_name = None      # Company name
        self.DB = None                # Database connection instance
        self.Err = None               # Error handler instance
        self.err_id = None            # Error ID
        self.debug = False            # Enable/disable debug
