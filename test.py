private function getStaffData($uid)
    {
        try {
            if ($uid == "") return false;
            $sql = "SELECT * FROM usr WHERE uid='$uid'";



            $result = $this->DB->select($sql);

            $this->err_id = $this->DB->err_id;
            if ($this->err_id !== "") return;
            foreach ($result as $row) {
                $Data = new StaffData(); //create the object
                $Data->_id = "<reserved>";
                $Data->uid = $row['uid'] ? $row['uid'] : '';
                $Data->app_code = "<reserved>";
                $Data->branch_id = intval($row['sch_id']);
                $Data->id = $row['id'] ? $row['id'] : '';
                $Data->ic = $row['ic'] ? $row['ic'] : '';
                $Data->name = $row['name'] ? $row['name'] : '';
                $Data->email = $row['mel'] ? $row['mel'] : '';
                $Data->phone = $row['hp'] ? $row['hp'] : '';
                $Data->user_no = '<reserved>'; // not being used right now
                $Data->category = '<reserved>'; // not being used right now
                $Data->category_name = '<reserved>'; // not being used right now
                $Data->group = '<reserved>'; // not being used right now
                $Data->group_name = '<reserved>'; // not being used right now
                $Data->subgroup = '<reserved>'; // not being used right now
                $Data->subgroup_name = '<reserved>'; // not being used right now
                $Data->status = intval($row['status'] ? $row['status'] : '');
                $sql = "select prm,val, code from type where grp='usrstatus' and (sid=0 or sid='$this->branch_id') and val='$row[status]'";
                $result = $this->DB->select($sql);
                $Data->status_name = array_key_exists(0, $result) ? $result[0]['prm'] : "";
                $Data->is_delete = $row['isdel'];
                $Data->system_level = $row['syslevel'] ? $row['syslevel'] : '';
                $Data->user_type = 'staff';

                $system = new System();
                $system->create_at = $this->handleDate($row['ts'], 'get');
                $system->create_by = $row['adm'] ? $row['adm'] : '';
                $system->update_at = $this->handleDate($row['ts'], 'get');
                $system->update_by = $row['adm'] ? $row['adm'] : '';
                $system->delete_at = $this->handleDate($row['delts'], 'get');
                $system->delete_by = $row['delby'] ? $row['delby'] : '';
                $system->module = 'staff';
                // $system->firebase_id = '';
                $system->user_level = '';
                $Data->system = $system;



                //Personal info
                $personal = new Personal();
                $personal->full_name = $row['name'] ? $row['name'] : '';
                $personal->nick_name = $row['nick'] ? $row['nick'] : '';
                $personal->gender = isset($row['sex']) ? $row['sex'] : '';
                $personal->birth_date = $this->handleDate($row['bday'], 'get');
                $personal->race = $row['race'] ? $row['race'] : '';
                $personal->religion = $row['religion'] ? $row['religion'] : '';
                $personal->file_profile = $row['file'] ? $row['file'] : '';
                $personal->file_profile_path = '/content/staff/';
                $personal->file_profile_url = $row['file'] ? $this->root_url . '/content/staff/' . $row['file'] : "";
                $personal->primary_phone = $row['hp'] ? $row['hp'] : '';
                $personal->secondary_phone = '<reserved>';
                $personal->primary_email = $row['mel'] ? $row['mel'] : '';
                $personal->secondary_email = '<reserved>';
                $personal->citizen = $row['citizen'] ? $row['citizen'] : '';
                $personal->education = $row['edulevel'] ? $row['edulevel'] : '';
                $personal->marital = $row['marital'] ? $row['marital'] : '';
                $personal->birth_place = $row['bstate'] ? $row['bstate'] : '';

                $Data->personal = $personal;
                //Job info
                $job = new Job();
                $job->designation = $row['job'] ? $row['job'] : '';
                $job->division = $row['jobdiv'] ? $row['jobdiv'] : '';
                $job->status = $row['jobsta'] ? $row['jobsta'] : '';
                $job->level = '<reserved>';
                $job->grade = $row['joblvl'] ? $row['joblvl'] : '';
                $job->start_date = $this->handleDate($row['jobstart'], 'get');
                // $job->start_date = $row['jobstart'] ? date('d-m-Y', strtotime($row['jobstart'])) : null;
                $job->end_date = $this->handleDate($row['jobend'], 'get');
                // $job->end_date = $row['jobend'] ? date('d-m-Y', strtotime($row['jobend'])) : null;
                $job->confirm_date = $this->handleDate($row['jobconfirm'], 'get');
                // $job->confirm_date = $row['jobconfirm'] ? date('d-m-Y', strtotime($row['jobconfirm'])) : null;
                $job->contract_expiry = $this->handleDate($row['excontract'], 'get');
                // $job->contract_expiry = $row['excontract'] ? date('d-m-Y', strtotime($row['excontract'])) : null;
                $job->visa_expiry = $this->handleDate($row['exvisa'], 'get');
                // $job->visa_expiry = $row['exvisa'] ? date('d-m-Y', strtotime($row['exvisa'])) : null;
                $job->passport_expiry = $this->handleDate($row['expassport'], 'get');
                // $job->passport_expiry = $row['expassport'] ? date('d-m-Y', strtotime($row['expassport'])) : null;
                $job->permit_expiry = $this->handleDate($row['expermit'], 'get');
                $job->permit_expiry = $row['expermit'] ? date('d-m-Y', strtotime($row['expermit'])) : '';
                $job->salary = '<reserved>';
                $job->company = $this->company_name;
                $job->specialization = '<reserved>';
                $job->qualification = $row['edulevel'] ? $row['edulevel'] : '';
                $Data->job = $job;
               
        } catch (Throwable $e) {
            //if any error occurs, it will be handled here
            $err_id = $this->Err->handleException($e);
            $err_data = [
                'err_id' => $err_id
            ];
            $this->resBody(500, false, 'Internal Server Error', $err_data);
            return false;
        }
    }