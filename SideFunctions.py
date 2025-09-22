from libraries import *
from DB import *

db_session = SessionLocal()

def import_excel_file(filePath): # importing the data into th db
    try:
        excel_file_name = os.path.splitext(os.path.basename(filePath))[0]
        # Read Excel file
        data = pd.read_excel(
            filePath, dtype={"phone_number": str}, sheet_name=0, engine="openpyxl"
        )
        # ----------------------------------------------
        data = check_emails(data)
        data = modify_name(data)
        data = phone_num_registration(data)
        data = dates_registration(data)  # Calling dates regist. to register formatted reg and exp dates
        data = set_status(data)
        data = check_duplicates(data)  # Calling check dups to ensure no duplicate members get signed in
        new_excel_name = f"editied_{excel_file_name}.xlsx"
        data.to_excel(new_excel_name, index=False)

        API_URL = "http://127.0.0.1:8000/readExcel/"


        with builtins.open(new_excel_name, "rb") as f:
            files = {"file": f}
            r = requests.post(API_URL, files=files)

        if r.status_code == 200:
            return True
        else: 
            return False

    except Exception as e:
        print(f"An unexpected error has occurred: {e}")
        print("-" * 30)
    except FileNotFoundError:
        print("-" * 30)
        print(f"{excel_file_name} not found")
#------------------------------------------------------------        
def check_emails(data):
    try:
        if isinstance(data, pd.DataFrame):
            new_emails = []
            for email in data["member_email"].astype(str).tolist():
                if "@" in email:
                    new_emails.append(email)
                else:
                    email = "Not Provided"
                    new_emails.append(email)
            data["member_email"] = new_emails
            return data
        else:
            if data != "":
                if "@" in data:
                    return data
                else: 
                    return "Not Provided"
            else:
                return "Not Provided"
    except Exception as e:
        print(f"An unexpected error has occured: {e}")
        print("-" * 30)
#------------------------------------------------------------
def modify_name(data):
    names = data["member_name"].tolist()
    modified_names_lst = []
    for name in names:
        name_lst = []
        name_lst = name.split()
        modified_name = ""
        for part in name_lst:
            modified_name += part.lower().capitalize()
            modified_name += " "
        modified_name.strip()
        modified_names_lst.append(modified_name)

    data["member_name"] = modified_names_lst
    return data
#------------------------------------------------------------
def check_duplicates(data):  # A function to check on the duplicates by using users email
    try:
        all_members = db_session.query(Member).all()
        if isinstance(data, pd.DataFrame):
            data_lst = data[["member_email", "member_name"]].values.tolist()

            haveEmailLst = []
            noEmailLst = []
            indices_to_drop = []
            for email, name in data_lst:
                if email != "Not Provided":
                    haveEmailLst.append(email)
                else:
                    noEmailLst.append(name)

            
            for email in haveEmailLst:
                for member_info in all_members:
                    if email == member_info.member_email:
                        condition = data["member_email"] == email
                        indices_to_drop.extend(data.index[condition].values.tolist())
                    else:
                        continue

            for name in noEmailLst:
                for member_info in all_members:
                    if name and member_info.member_name and name.lower().strip() == (member_info.member_name).lower().strip():
                        condition = data["member_name"] == name
                        indices_to_drop.extend(data.index[condition].values.tolist())
                    else:
                        continue
        
            data = data.drop(indices_to_drop)
            return data
        
        elif isinstance(data, object):
            member_email = getattr(data, 'member_email', None)
            member_name = getattr(data, 'member_name', None) 
            found_counter = 0  # A counter to check on single member input

            if member_email != "Not Provided":
                for reg_email in all_members:
                    if member_email == reg_email.member_email:
                        found_counter += 1  # if the new member matches one or more email the counter will be incremented by 1
                    else:
                        continue
                if found_counter > 0:
                    return f"{member_name} is already in the database"  # Returning false to refuse the insertion of the new member
                else:
                    return f"Add {member_name}"  # Returning True to allow new member insertion in the db

            else:
                flag = True
                for char in member_name:
                    if char.isdigit():
                        flag = False
                    else:
                        continue
                if member_name.count(" ") >= 2 and flag == True:
                    for reg_name in all_members:
                        if member_name.lower().strip() == (reg_name.member_name).lower().strip():
                            found_counter += 1 
                        else:
                            continue
                    if found_counter > 0:
                        return f"{member_name} is already in the database"  # Returning false to refuse the insertion of the new member
                    else:
                        return f"Add {member_name}"  # Returning True to allow new member insertion in the db 
                else:
                    return "Please enter a valid name"
    except Exception as e:
        print(f"An unexcepted error has happened: {e}")
        print("-" * 30)
        return False

#------------------------------------------------------------
def phone_num_registration(data):
    try:
        if isinstance(data, pd.DataFrame):
            phone_lst = data["phone_number"].tolist()
            for number in range(len(phone_lst)):
                if phone_lst[number] == "Not Provided":
                    continue
                else:
                    digits_only = "".join([char for char in str(phone_lst[number]) if char.isdigit()])
                    if digits_only == "":
                        phone_lst[number] = "Not Provided"
                    else:
                        phone_lst[number] = digits_only
            data["phone_number"] = phone_lst
            return data
        else:
            phone_num = data
            if phone_num == "":
                phone_num = "Not Provided"
                return phone_num
            else:
                digits_only = "".join([char for char in str(phone_num) if char.isdigit()])
                if digits_only == "":
                    phone_num = "Not Provided"
                else:
                    phone_num = digits_only
                return phone_num
    except Exception as e:
        print(f"An unexpected error has occured: {e}")
        print("-" * 30)              
#------------------------------------------------------------
def dates_registration(data):
    try:
        if isinstance(data, pd.DataFrame):
            formatted_reg_dates_lst = []  # An empty lst for reg dates
            formatted_exp_dates_lst = []  # An empty lst for exp dates
            for date_str in data.get("reg_date", []):
                if not isinstance(date_str, str):
                    reg_date = datetime.today()
                    formatted_reg_date = reg_date.strftime("%d %m %Y")
                    exp_date = reg_date + timedelta(days=365)
                    formatted_exp_date = exp_date.strftime("%d %m %Y")
                    formatted_reg_dates_lst.append(formatted_reg_date)
                    formatted_exp_dates_lst.append(formatted_exp_date)
                    continue
                else:
                    try:
                        cleaned_date = sub(r'\D', " ", date_str)
                        day, month, year = [int(part) for part in cleaned_date.split()]
                        formatted_reg_date = datetime(year, month, day).strftime("%d %m %Y")  # formatting the reg date into a better form
                        formatted_exp_date = datetime(year + 1, month, day).strftime("%d %m %Y")  # formatting the exp date into a better form
                        formatted_reg_dates_lst.append(formatted_reg_date)  # Adding the reg. date into the lst
                        formatted_exp_dates_lst.append(formatted_exp_date) # Adding the exp. date into the lst
                    except (ValueError, TypeError):
                        reg_date = datetime.today()
                        formatted_reg_date = reg_date.strftime("%d %m %Y")
                        exp_date = reg_date + timedelta(days=365)
                        formatted_exp_date = exp_date.strftime("%d %m %Y")
                        formatted_reg_dates_lst.append(formatted_reg_date)
                        formatted_exp_dates_lst.append(formatted_exp_date)
                
            data["reg_date"] = formatted_reg_dates_lst
            data["exp_date"] = formatted_exp_dates_lst  # Adding a new column with the exp. dates     
            return data   
        

        elif isinstance(data, object):
            reg_date_str = getattr(data, 'reg_date', None)
            dates_lst = []  # An empty lst for reg dates
            if reg_date_str == "Not Provided" or reg_date_str is None or reg_date_str == "":
                reg_date = datetime.today()
                formatted_reg_date = reg_date.strftime("%d %m %Y")
                exp_date = reg_date + timedelta(days=365)
                formatted_exp_date = exp_date.strftime("%d %m %Y")
                dates_lst.append(formatted_reg_date)
                dates_lst.append(formatted_exp_date)
                return dates_lst
            else:
                try:
                    cleaned_date = sub(r'\D', " ", reg_date_str)
                    day, month, year = [int(part) for part in cleaned_date.split()]
                    formatted_reg_date = datetime(year, month, day).strftime("%d %m %Y")  # formatting the reg date into a better form
                    formatted_exp_date = datetime(year + 1, month, day).strftime("%d %m %Y")  # formatting the exp date into a better form
                    dates_lst.append(formatted_reg_date) # adding the reg date into the lst
                    dates_lst.append(formatted_exp_date)  # adding the exp date into the lst
                    return dates_lst
                except (ValueError, TypeError):
                    reg_date = datetime.today()
                    formatted_reg_date = reg_date.strftime("%d %m %Y")
                    exp_date = reg_date + timedelta(days=365)
                    formatted_exp_date = exp_date.strftime("%d %m %Y")
                    dates_lst.append(formatted_reg_date)
                    dates_lst.append(formatted_exp_date)
                    return dates_lst 
                
    except Exception as e:
        print(f"An unexpected error has occured: {e}")
        print("-" * 30)
        return None
#------------------------------------------------------------
def set_status(data):  # Setting the status for each user depending on the date
    try:
        current_date = datetime.now()
        
        if isinstance(data, pd.DataFrame):
            # Handle DataFrame input
            status_list = []
            for exp_date_str in data['exp_date']:
                # Parse the expiration date string into a datetime object
                exp_date = datetime.strptime(exp_date_str, "%d %m %Y")
                
                # Determine status based on date comparison
                if exp_date >= current_date:
                    status = "Active"
                else:
                    status = "Inactive"
                status_list.append(status)
            
            data['status'] = status_list
            return data
            
        elif isinstance(data, object):  # Use your actual Member class
            # Handle single Member object
            exp_date = getattr(data, "exp_date, None")
            if not data.exp_date:
                return "Inactive"  # Or whatever default you prefer
            
            exp_date = datetime.strptime(data.exp_date, "%d %m %Y")
            
            if exp_date >= current_date:
                return "Active"
            else:
                return "Inactive"
                
    except Exception as e:
        print(f"Error in set_status: {e}")
        return None
#------------------------------------------------------------
def reshape_arabic_text(data):# A function to to reshape the arabic text
    try:
        text_str = str(data)  # Ensuring that the data is string
        reshaped_text = arabic_reshaper.reshape(text_str)  # reshaping the arabic text
        final_text = get_display(reshaped_text)  # getting the proper display
        return final_text  # returning the final text for display
    except Exception as e:
        print(f"An unexpected error has occured: {e}")
#-------------------------------------------------------------
def show_all_members():
    members = db_session.query(Member).all()
    all_members = []
    for member in members:
        all_members.append(member.to_tuple())
    display_rows = []
    for row in all_members:
        processed_members = [reshape_arabic_text(cell) for cell in row]
        display_rows.append(processed_members)
    table = Member.__table__
    headers = table.columns.keys()    
    reshpaed_headers = [reshape_arabic_text(header) for header in headers]
    print(tabulate(display_rows, headers=reshpaed_headers, tablefmt='pipe'))
