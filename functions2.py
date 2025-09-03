from libraries import *
from DB import *

db_session = SessionLocal()

def import_excel_file(): # importing the data into th db
    try:
        base_folder = (
            r"F:\Programming\projects\Egyptian-Society-for-Environmental-Sciences-Database"  # A base folder to search for the excel file
        )
        excel_file_name = input(
            "Enter the Excel file name: "
        )  # taking the name of the excel file
        excel_file = (
            excel_file_name + ".xlsx"
        )  # Adding the extension to the name of the excel file
        excel_file_final = path.join(
            base_folder, excel_file
        )  # Joinning out the base folder with the excel file name to make a full path
        sheet_name_locally = input(
            "Enter the sheet name: "
        )  # Taking the name of the Sheet where the data is stored
        data = pd.read_excel(
            excel_file_final, dtype={"phone_number": str}, sheet_name=sheet_name_locally
        )
        # ----------------------------------------------
        data = check_emails(data)
        data = check_duplicates(data)  # Calling check dups to ensure no duplicate members get signed in
        data = phone_num_registration(data)
        data = dates_registration(data)  # Calling dates regist. to register formatted reg and exp dates
        data = set_status(data)
        new_excel_name = "editied " + excel_file
        data.to_excel(new_excel_name, index=False) 
        print("-" * 30)
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
def check_duplicates(data):  # A function to check on the duplicates by using users email
    try:
        all_members = db_session.query(Member).all()
        if isinstance(data, pd.DataFrame):  # An if statement
            indices_to_drop = []# An empty list which will be filled later with the index of the duplicated names to drop them from the dataframe
            emails_lst = data[["member_email", "member_name"]].values.tolist()  # putting the new emails in a list to operate on them
            potential_mem_emails = []
            no_mem_email_lst = []
            for email in range(len(emails_lst)):
                if emails_lst[email][0] != "Not Provided":
                    potential_mem_emails.append(emails_lst[email][0])
                else:
                    no_mem_email_lst.append(emails_lst[email][1])
                    continue
            for pot_email in potential_mem_emails:# An outer for loop to iterate reg members on each new member
                for reg_email in all_members:  # An inner for loop to iterate reg members on each new member
                    if (pot_email == reg_email.member_email):  # If statement if the potential email matches a reg. email its indexing will be stored in an list
                        condition = data["member_email"] == pot_email # The condition to get the potential email index
                        indices_to_drop.extend(data[condition].index.tolist()) # Adding the indices to the empty lst
                    else:
                        continue
                    
            for no_member in no_mem_email_lst:
                for reg_member in all_members:
                    if no_member == reg_member.member_name:
                        condition = data["member_name"] == no_member
                        indices_to_drop.extend(data[condition].index.tolist())
            data = data.drop(indices_to_drop)  # Dropping duplicated rows
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
                    return False  # Returning false to refuse the insertion of the new member
                else:
                    return True  # Returning True to allow new member insertion in the db
                
            else:
                for reg_name in all_members:
                    if member_name == reg_name.member_name:
                        found_counter += 1 
                    else:
                        continue
                if found_counter > 0:
                    return False  # Returning false to refuse the insertion of the new member
                else:
                    return True  # Returning True to allow new member insertion in the db 
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
                    formatted_reg_dates_lst.append("Not Provided")
                    formatted_exp_dates_lst.append("Not Provided")
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
                        formatted_reg_dates_lst.append("Not Provided")
                        formatted_exp_dates_lst.append("Not Provided")
                
            data["reg_date"] = formatted_reg_dates_lst
            data["exp_date"] = formatted_exp_dates_lst  # Adding a new column with the exp. dates     
            return data   
        else:
            dates_lst = []  # An empty lst for reg dates
            if data == "":
                dates_lst.append("Not Provided")
                dates_lst.append("Not Provided")
            else:
                try:
                    cleaned_date = sub(r'\D', " ", data)
                    day, month, year = [int(part) for part in cleaned_date.split()]
                    formatted_reg_date = datetime(year, month, day).strftime("%d %m %Y")  # formatting the reg date into a better form
                    formatted_exp_date = datetime(year + 1, month, day).strftime("%d %m %Y")  # formatting the exp date into a better formdates_lst.append(formatted_reg_date)
                    dates_lst.append(formatted_reg_date) # adding the reg date into the lst
                    dates_lst.append(formatted_exp_date)  # adding the exp date into the lst
                    return dates_lst
                except (ValueError, TypeError):
                    dates_lst.append("Not Provided")  
                    dates_lst.append("Not Provided")
                    return dates_lst 
    except Exception as e:
        print(f"An unexpected error has occured: {e}")
        print("-" * 30)
        return None
#------------------------------------------------------------
def set_status(data):  # Setting the status for each user depending on the date
    try:
        current_date = datetime.now().strftime("%d %m %Y")
        status_lst = []
        if isinstance(data, pd.DataFrame):
            for date in data['exp_date']:
                if not isinstance(date, str) or date == "Not Provided":
                    status = "Not Provided"
                    status_lst.append(status)
                    continue
                if date > current_date:
                    status = "Active"
                    status_lst.append(status)
                elif date < current_date:
                    status = "Inactive"
                    status_lst.append(status)
            data['status'] = status_lst
            return data
    except Exception as e:
        print(f"An unexpected error has occured: {e}")
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