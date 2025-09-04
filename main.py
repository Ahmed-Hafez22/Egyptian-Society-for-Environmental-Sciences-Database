# other python files
from SideFunctions import *
from libraries import *
from DB import *
# Main
show_all_members()
# flag = True
# while flag == True:
#     try:
#         show_menu()
#         operation_choice = take_user_input()
#         if operation_choice == 1:
#             import_excel_file()
#         elif operation_choice == 2:
#             register_new_member()
#         elif operation_choice == 3:
#             show_members()
#         elif operation_choice == 4:
#             check_member_info()
#         elif operation_choice == 5:
#             edit_member_info()
#         elif operation_choice == 6:
#             delete_member()
#         elif operation_choice == 7:
#             flag = False
#         else:
#             print("Invalid Choice")
#     except Exception as e:
#         print(f"An unexpected error has Occured: {e}") #Prevent Error
# Close Database Connection
# con.commit()
# con.close()