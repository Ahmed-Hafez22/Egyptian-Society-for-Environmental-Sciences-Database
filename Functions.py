from libraries import *
from Database import *


# Functions
def show_menu():  # A function to print out the menu
    print("Welcome to Egyptian Society for Environmental Sciences's Database!!")
    print("--------------------------------------------------------------------")
    print(
        "Operation List:\n1-Import Excel File\n2-Register a New Member\n3-Show Members\n4-Check Member Information\n5-Edit Member Information\n6-Delete member\n7-Exit"
    )


def take_user_input():  # A function to store teh user input
    userChoice = int(input("Choose an operation: "))
    print("-" * 10)
    return userChoice


def import_excel_file(): # importing the data into th db
    try:
        base_folder = (
            r"C:\Work\Programming\Egyptian-Society-for-Environmental-Sciences-Database"  # A base folder to search for the excel file
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


def show_members(): # Printing out the members
    try:
        print(
            "How would you like to sort the members:\n1-Alphabetically\n2-By Status\n3-By Expiration Date"
        )
        task_choice = (
            take_user_input()
        )  # Storing user input to start sorting out the members to print them out

        if task_choice == 1:
            print("1-Asecnding\n2-Descending")
            order_choice = take_user_input()  # Storing the way of sorting ASEC or DESC
            if order_choice == 1:
                query = "SELECT * FROM members_info ORDER BY member_name"
            else:
                query = "SELECT * FROM members_info ORDER BY member_name DESC"

        elif task_choice == 2:
            print("1-Asecnding\n2-Descending")
            order_choice = take_user_input()  # Storing the way of sorting ASEC or DESC
            if order_choice == 1:
                query = "SELECT * FROM members_info ORDER BY status"
            else:
                query = "SELECT * FROM members_info ORDER BY status DESC"

        elif task_choice == 3:
            print("1-Expired\n2-About to Expire")
            order_choice = take_user_input()  # Storing the way of sorting ASEC or DESC
            if order_choice == 1:
                query = " SELECT * FROM members_info WHERE expiration_date < DATE('now')"
            else:
                query = "SELECT * FROM members_info WHERE expiration_date >= DATE('now') AND expiration_date <= DATE('now', '+12 month') ORDER BY expiration_date"
        else:
            print("Invalid Choice!!")  # Handling error if user entered an invalid choice
        rows = cur.execute(query).fetchall()  # fetching all of the users in the database
        display_rows = (
            []
        )  # An empty lst which will be filled after processing the rows to ensure Arabic names get printed out correctly
        for row in rows:  # A loop to iterate through all the users info
            proccessed_rows = [
                reshape_arabic_text(cell) for cell in row
            ]  # Processing cell by cell in each row
            display_rows.append(proccessed_rows)  # adding processed rows into the lst

        headers = [
            description[0] for description in cur.description
        ]  # Getting the headers of the table
        reshaped_headers = [
            reshape_arabic_text(h) for h in headers
        ]  # Reshaping the headers of the table to ensure clear arabic names

        print(
            tabulate(display_rows, headers=reshaped_headers, tablefmt="pipe")
        )  # Printing out the names in a clear Table
        print("-" * 30)
    except Exception as e:
        print(f"An unexpected error has occured: {e}")
         

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
     
def check_duplicates(data):  # A function to check on the duplicates by using users email
    try:
        registered_emails = cur.execute("SELECT email FROM members_info").fetchall()  # Fetching out all the users email from the table
        registered_names = cur.execute("SELECT member_name FROM members_info").fetchall()
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
                for reg_email in registered_emails:  # An inner for loop to iterate reg members on each new member
                    if (pot_email == reg_email[0]):  # If statement if the potential email matches a reg. email its indexing will be stored in an list
                        condition = data["member_email"] == pot_email # The condition to get the potential email index
                        indices_to_drop.extend(data[condition].index.tolist()) # Adding the indices to the empty lst
                    else:
                        continue
                    
            for no_member in no_mem_email_lst:
                for reg_member in registered_names:
                    if no_member == reg_member[0]:
                        condition = data["member_name"] == no_member
                        indices_to_drop.extend(data[condition].index.tolist())
            data = data.drop(indices_to_drop)  # Dropping duplicated rows
            return data
        else:
            found_counter = 0  # A counter to check on single member input
            if data[2] != "Not Provided":
                for reg_email in registered_emails:
                    if data[2] == reg_email[0]:
                        found_counter += 1  # if the new member matches one or more email the counter will be incremented by 1
                    else:
                        continue
                if found_counter > 0:
                    print("-" * 30)
                    print(
                        "Member is already registered"
                    )  # Telling the user the member is already in the db
                    print("-" * 30)
                    return False  # Returning false to refuse the insertion of the new member
                else:
                    print("-" * 30)
                    print(
                        "Member got added successfully"
                    )  # Telling the user the member got added Successfully
                    print("-" * 30)
                    return True  # Returning True to allow new member insertion in the db
            else:
                for reg_name in registered_names:
                    if data[0] == reg_name[0]:
                        found_counter += 1
                    else:
                        continue
                if found_counter > 0:
                    print("-" * 30)
                    print(
                        "Member is already registered"
                    )  # Telling the user the member is already in the db
                    print("-" * 30)
                    return False  # Returning false to refuse the insertion of the new member
                else:
                    print("-" * 30)
                    print(
                        "Member got added successfully"
                    )  # Telling the user the member got added Successfully
                    print("-" * 30)
                    return True  # Returning True to allow new member insertion in the db 
    except Exception as e:
        print(f"An unexcepted error has happened: {e}")
        print("-" * 30)


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
                        formatted_reg_date = datetime(year, month, day).strftime("%Y-%m-%d")  # formatting the reg date into a better form
                        formatted_exp_date = datetime(year + 1, month, day).strftime("%Y-%m-%d")  # formatting the exp date into a better form
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
                    formatted_reg_date = datetime(year, month, day).strftime("%Y-%m-%d")  # formatting the reg date into a better form
                    formatted_exp_date = datetime(year + 1, month, day).strftime("%Y-%m-%d")  # formatting the exp date into a better formdates_lst.append(formatted_reg_date)
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

def set_status(data):  # Setting the status for each user depending on the date
    try:
        current_date = datetime.now().strftime("%Y-%m-%d")
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


def reshape_arabic_text(data):# A function to to reshape the arabic text
    try:
        text_str = str(data)  # Ensuring that the data is string
        reshaped_text = arabic_reshaper.reshape(text_str)  # reshaping the arabic text
        final_text = get_display(reshaped_text)  # getting the proper display
        return final_text  # returning the final text for display
    except Exception as e:
        print(f"An unexpected error has occured: {e}")

def register_new_member():  # A function to add single new member
    try:
        lst_of_req = ["name", "phone number", "registration day", "email"]  # Lst of requirements to iterate through it
        lst_of_fullfiled_req = []  # An empty lst to fill it with the req
        for i in range(len(lst_of_req)):  # For loop iterating throught the req lst to ask the user to input the req
            lst_of_fullfiled_req.append(input(f"Enter member's {lst_of_req[i]}: "))  # Taking the user input and appending them directly to the empty lst
        lst_of_fullfiled_req.extend(dates_registration(lst_of_fullfiled_req[2]))# Sending the unformatted date to a function to formate it and get the exp date
        lst_of_fullfiled_req[1] = phone_num_registration(lst_of_fullfiled_req[1])
        lst_of_fullfiled_req[3] = check_emails(lst_of_fullfiled_req[3])
        lst_of_fullfiled_req.pop(2)  # pop the old date
        if (check_duplicates(lst_of_fullfiled_req) == True):  # Sending the data to if the member isn't in the db to add them
            cur.executemany(
                """
                                INSERT INTO members_info(member_name, phone_number, email, registration_date, expiration_date)
                                VALUES (?, ?, ?, ?, ?)
                            """,
                (lst_of_fullfiled_req,),
            )
        set_status()  # Setting the new member status
        con.commit()  # commiting the changes to the db
    except Exception as e:
        print(f"An unexpected error has occured: {e}")


def check_member_info():  # A function to check on the members info
    try:
        wanted_member = input(
            "Enter the member name: "
        ).strip()  # Taking the first name from the user
        print("=" * 50)
        search_pattern = f"{wanted_member} %"  # Setting a search pattern
        pot_members = cur.execute(
            """SELECT *
                                    FROM members_info
                                    WHERE member_name LIKE ? OR member_name = ?""",
            (search_pattern, wanted_member),
        ).fetchall()  # Fetching out all the members with the similar first name
        display_member = (
            []
        )  # An empty lst which will be filled after processing the rows to ensure Arabic names get printed out correctly
        for member in pot_members:
            processed_members = [
                reshape_arabic_text(mem_cell) for mem_cell in member
            ]  # Process each cell
            display_member.append(
                processed_members
            )  # Add the proccessed rows to the empty ls
        headers = [description[0] for description in cur.description]  # Getting the headers
        reshaped_headers = [reshape_arabic_text(h) for h in headers]  # Reshape the heades
        print(
            tabulate(display_member, headers=reshaped_headers, tablefmt="pipe")
        )  # printing out the name
        print("-" * 30)
        return [search_pattern, wanted_member]
    except Exception as e:
        print(f"An unexpected error has occured: {e}")

def edit_member_info(): # A function to edit users info
    try:
        wanted_mem = check_member_info()  # Calling the check member info to show the members with similar names to choose their ID
        ids = cur.execute("SELECT id FROM members_info WHERE member_name LIKE (?) OR member_name = (?)",
                          (wanted_mem[0], wanted_mem[1]))
        ids_Tuple = ids.fetchall()
        ids_lst = [item[0] for item in ids_Tuple]
        member_choice = int(
            input("Choose Member ID: ")
        )  # Taking user input of the wanted ID
        if member_choice in ids_lst:
            cur.execute("SELECT * FROM members_info LIMIT 1")
            headers = [
                description[0] for description in cur.description
            ]  # getting the headers so the user can choose what info to change
            headers_without_id = headers[1:]  # Getting all of the headers except for the id
            for i in range(
                len(headers_without_id)
            ):  # A loop to iterate through all the headers
                print(f"{i+1}. {headers_without_id[i]}")
            info_choice = int(
                input("Choose the info you want to edit: ")
            )  # Taking user input for the info number

            if info_choice == 1:  # Changing user name
                edit = input("Enter the new name: ")
                query = "UPDATE members_info SET member_name = (?) WHERE id = (?)"
                if edit != "":
                    cur.execute(query, (edit, member_choice))
                else:
                    edit = "Not Provided"
                    cur.execute(query, (edit, member_choice))
                print("-" * 30)
                print("Name got changed correctly")
                print("-" * 30)

            elif info_choice == 2:  # Changing user phone number
                edit = input("Enter the new phone number: ")
                query = "UPDATE members_info SET phone_number = (?) WHERE id = (?)"
                if edit != "":
                    cur.execute(query, (edit, member_choice))
                else:
                    print(edit)
                    cur.execute(query, (edit, member_choice))
                print("-" * 30)
                print("Phone Number got changed successfully")
                print("-" * 30)

            elif info_choice == 3:  # Changing user reg date and exp date
                edit = input("Enter the new registration date: ")
                query = "UPDATE members_info SET (registration_date, expiration_date) = (?, ?) WHERE id = (?)"
                binding = ()
                if edit != "":
                    edits_lst = dates_registration(edit)
                    binding = (edits_lst[0], edits_lst[1], member_choice)
                    cur.execute(query, binding)
                    set_status()
                else:
                    binding = ("Not Provided", "Not Provided", member_choice)
                    cur.execute(query, binding)
                    set_status()
                print("-" * 30)
                print("Registration and Expiration dates got changed successfully")
                print("-" * 30)

            elif info_choice == 4:  # Changing user exp date only
                edit = input("Enter the new expiration date: ")
                query = "UPDATE members_info SET expiration_date = (?) WHERE id = (?)"
                if edit != "":
                    day, month, year = [sec for sec in edit.split()]
                    formatted_exp_date = datetime(year, month, day).strftime("%Y-%m-%d")    
                    cur.execute(query, (formatted_exp_date, member_choice))
                    set_status()
                else:
                    edit = "Not Provided"
                    cur.execute(query, (edit, member_choice))
                    set_status()
                print("-" * 30)
                print("Expiration date got changed successfully")
                print("-" * 30)

            elif info_choice == 5:  # Changing user status
                edit = int(input("Choose the status:\n1-Active\n2-Inactive\n3-Not Provided\nChoice: "))
                if edit == 1:
                    query = "UPDATE members_info SET status = 'Active' WHERE id = (?)"
                    cur.execute(query, member_choice)
                    print("-" * 30)
                    print("New status was set correctly")
                    print("-" * 30)
                elif edit == 2:
                    query = "UPDATE members_info SET status = 'Inactive' WHERE id = (?)"
                    cur.execute(query, (member_choice,))
                    print("-" * 30)
                    print("New status was set correctly")
                    print("-" * 30)
                elif edit == 3:
                    query = "UPDATE members_info SET status = 'Not Provided' WHERE id = (?)"
                    cur.execute(query, (member_choice,))
                else:
                    print("-" * 30)
                    print("Invalid Choice")
                    print("-" * 30)

            elif info_choice == 6:  # Chaning user email
                query = "UPDATE members_info SET email = (?) WHERE id = (?)"
                edit = input("Enter the new email: ")
                if edit != "":
                    edit = check_emails(edit)
                    cur.execute(query, (edit, member_choice))
                else:
                    edit = "Not Provided"
                    cur.execute(query, (edit, member_choice))
                print("-" * 30)
                print("Email got changed successfully")
                print("-" * 30)
            else:
                print("-" * 30)
                print("Invalid Choice")
                print("-" * 30)
            con.commit()
        else:
            print("ID is not in the wanted list")
    except Exception as e:
        print(f"An unexpected Error has occured: {e}")

def delete_member():
    wanted_mem = check_member_info()  # Calling the check member info to show the members with similar names to choose their ID
    ids = cur.execute("SELECT id FROM members_info WHERE member_name LIKE (?) OR member_name = (?)",
                    (wanted_mem[0], wanted_mem[1]))
    ids_Tuple = ids.fetchall()
    ids_lst = [item[0] for item in ids_Tuple]
    member_choice = int(input("Choose Member ID: "))  # Taking user input of the wanted ID
    if member_choice in ids_lst:
        name = cur.execute("SELECT member_name FROM members_info WHERE id = (?)", (member_choice,)).fetchone()
        print(f"{name[0]} got deleted Successfully")
        cur.execute("DELETE FROM members_info WHERE id = (?)", (member_choice,))
    else:

        print("Id isn't in the wanted list")
