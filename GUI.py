from libraries import *
import API
import SideFunctions


def create_hover_functions(button_widget, hover_color, leave_color):
    def on_enter(event=None):
        button_widget.config(background=hover_color)

    def on_leave(event=None):
        button_widget.config(background=leave_color)

    return on_enter, on_leave

WIDTH = 1000
HEIGHT = 500
yVelocity = 30

def show_operation_menu():
        global Operation_menu 
        Operation_menu = Canvas(window, width=screen_width, height=screen_height, background="#ffda7c")
        Operation_menu.place(relx=0.5, rely=0.5, anchor=CENTER)
        Operation_menu.create_text((screen_width/2), 30, text="ESES Database", font=("courier new", 30))
        Operation_menu.create_text(150, 100, text="Operations List:- ", font=("calibri", 30))
        import_excel_file_button = Button(Operation_menu, background="#ffda7c", text="1-Import Excel File", font=("oswald", 20), relief="flat", activebackground="#fac84a", command=import_excel_file)
        hover_enter_importExcelButton, hover_leave_importExcelButton = create_hover_functions(import_excel_file_button, "#fce5aa", "#ffda7c") 
        import_excel_file_button.bind("<Enter>", hover_enter_importExcelButton)
        import_excel_file_button.bind("<Leave>", hover_leave_importExcelButton)
        Operation_menu.create_window(155, 160, window=import_excel_file_button)
        register_new_member = Button(Operation_menu, background="#ffda7c", text="2-Register New Member", font=("Oswald", 20), relief="flat", activebackground="#fac84a", command=regist_new_member)
        hover_enter_registNewMemberButton, hover_leave_registNewMemberButton = create_hover_functions(register_new_member, "#fce5aa", "#ffda7c")
        Operation_menu.create_window(190, 220, window=register_new_member)
        register_new_member.bind("<Enter>", hover_enter_registNewMemberButton)
        register_new_member.bind("<Leave>", hover_leave_registNewMemberButton)
        

is_fading = True

def pulse_text(fade_direction="out"):
    """Continuously fades the 'press_enter' text in and out."""
    if not is_fading: return
    start_rgb, end_rgb = ((255, 0, 0), (255, 218, 124))
    if fade_direction == "out":
        _animate_color(start_rgb, end_rgb, "in")
    else:
        _animate_color(end_rgb, start_rgb, "out")

def _animate_color(from_rgb, to_rgb, next_dir, steps=10, step=0):
    """Helper function for the pulse animation."""
    if not is_fading or step > steps:
        window.after(400, pulse_text, next_dir) # Pause before reversing
        return
    r = int(from_rgb[0] + (to_rgb[0] - from_rgb[0]) * step / steps)
    g = int(from_rgb[1] + (to_rgb[1] - from_rgb[1]) * step / steps)
    b = int(from_rgb[2] + (to_rgb[2] - from_rgb[2]) * step / steps)
    color = f"#{r:02x}{g:02x}{b:02x}"
    main_screen_canvas.itemconfig(press_enter, fill=color)
    window.after(25, _animate_color, from_rgb, to_rgb, next_dir, steps, step + 1)
    
def fade_text_permanently(step=0, steps=10):
    """Handles the final fade-out of the text after Enter is pressed."""
    if step > steps: return
    start_rgb, end_rgb = ((255, 0, 0), (255, 218, 124))
    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * step / steps)
    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * step / steps)
    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * step / steps)
    color = f"#{r:02x}{g:02x}{b:02x}"
    main_screen_canvas.itemconfig(press_enter, fill=color)
    window.after(25, fade_text_permanently, step + 1)
    

def move_main_screen(event=None):
        main_screen_canvas.move(main_screen_logo, 0, -yVelocity)
        main_screen_canvas.move(main_screen_text, 0, -yVelocity)
        if main_screen_canvas.coords(main_screen_logo)[1] > -150:
                window.after(20, move_main_screen)
        else:
                main_screen_canvas.place_forget()
                show_operation_menu()

def fade_text(step=0, steps=3):
        if step <= steps:
                # Start and end colors
                start_rgb = (255, 0, 0)        # Red
                end_rgb   = (255, 218, 124)    # #ffda7c

                # Interpolate between start and end
                r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * step / steps)
                g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * step / steps)
                b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * step / steps)

                # Convert to hex color
                color = f"#{r:02x}{g:02x}{b:02x}"
                main_screen_canvas.itemconfig(press_enter, fill=color)

                # Schedule next step
                window.after(50, fade_text, step + 1, steps)

def start_animation(event=None):
    global is_fading
    if not is_fading: return # Prevent accidental double-press
    is_fading = False
    window.unbind("<Return>")
    move_main_screen()
    fade_text_permanently()
        
def import_excel_file(event=None):
    Operation_menu.place_forget()
    import_excel_file_canvas = Canvas(window, width=screen_width, height=screen_height, background="#ffda7c")
    import_excel_file_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    import_excel_file_canvas.create_text((screen_width/2), 30, text="ESES Database", font=("courier new", 30))
    import_excel_file_canvas.create_text(150, 100, text="Import excel file:", font=("calibri", 30))

    def open_excel_file(event=None):
        filePath = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if filePath:
            status = SideFunctions.import_excel_file(filePath)
            excel_file_name = os.path.splitext(os.path.basename(filePath))[0]
            if status == True:
                import_excel_file_canvas.create_text(300, 250, text= excel_file_name + " got added successfully", font=("Arial", 18))
            else:
                import_excel_file_canvas.create_text(300, 250, text= excel_file_name + " didn't get added", font=("Arial", 18))


    def return_to_main_menu(event=None):
        import_excel_file_canvas.place_forget()
        Operation_menu.place(relx=0.5, rely=0.5, anchor=CENTER)

    chooseFileButton = Button(window, background="#ffda7c", font=("oswald", 25), activebackground="#fac84a", text="Choose a file", command=open_excel_file, relief="groove")
    returnToMainMenuButton = Button(window, background="#ffda7c", font=("oswald", 25), activebackground="#fac84a", text="Return", command=return_to_main_menu, relief="groove")
    import_excel_file_canvas.create_window(200, 180, window=chooseFileButton)
    import_excel_file_canvas.create_window(160, 320, window=returnToMainMenuButton)
    hover_enter_chooseFileButton, hover_leave_chooseFileButton = create_hover_functions(chooseFileButton, "#fce5aa", "#ffda7c")
    chooseFileButton.bind("<Enter>", hover_enter_chooseFileButton)
    chooseFileButton.bind("<Leave>", hover_leave_chooseFileButton)
    hover_enter_returnButton, hover_leave_returnButton = create_hover_functions(returnToMainMenuButton, "#fce5aa", "#ffda7c")
    returnToMainMenuButton.bind("<Enter>", hover_enter_returnButton)
    returnToMainMenuButton.bind("<Leave>", hover_leave_returnButton)


def regist_new_member(event = None):

    def submit_new_member_info(event = None):

        API_URL = "http://127.0.0.1:8000/Create-Member"

        new_member_dict = {
            "member_name" : member_name_entry.get(),
            "phone_number" : phone_numebr_entry.get(),
            "member_email" : member_email_entry.get(),
            "reg_date" : reg_date_entry.get()
        }

        request = requests.post(API_URL, json=new_member_dict)

        if request.status_code == 200:
            regist_new_member_canvas.create_text(400, 400, text=new_member_dict["member_name"] + " got add successfully", font=("Arial", 18))
        else:
            error_msg = request.text  # Get the error details from the server
            regist_new_member_canvas.create_text(400, 400, text=new_member_dict["member_name"] + " didn't get added", font=("Arial", 18))


    Operation_menu.place_forget()
    regist_new_member_canvas = Canvas(window, width=screen_width, height=screen_height, background="#ffda7c")
    regist_new_member_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    regist_new_member_canvas.create_text((screen_width/2), 30, text="ESES Database", font=("courier new", 30))
    regist_new_member_canvas.create_text(200, 100, text="Register new member:", font=("calibri", 30))
    member_name_entry = Entry(regist_new_member_canvas, font=(15))
    regist_new_member_canvas.create_text(150, 170, text="Member Name:", font=("Arial", 20))
    regist_new_member_canvas.create_window(330, 170, window=member_name_entry, width=160, height=25)
    phone_numebr_entry = Entry(regist_new_member_canvas, font=(15))
    regist_new_member_canvas.create_text(150, 220, text="Phone Number:", font=("Arial", 20))
    regist_new_member_canvas.create_window(330, 220, window=phone_numebr_entry, width=160, height=25)
    reg_date_entry = Entry(regist_new_member_canvas, font=(15))
    regist_new_member_canvas.create_text(165, 270, text="Registration Date:", font=("Arial", 20))
    regist_new_member_canvas.create_window(360, 270, window=reg_date_entry, width=160, height=25)
    member_email_entry = Entry(regist_new_member_canvas, font=(15))
    regist_new_member_canvas.create_text(140, 320, text="Member Email:", font=("Arial", 20))
    regist_new_member_canvas.create_window(360, 320, window=member_email_entry, width=250, height=25)
    submit_button = Button(regist_new_member_canvas, text="Submit", relief="groove", font=("oswald", 15),  command=submit_new_member_info, activebackground="#fac84a", background="#ffda7c")
    hover_enter_submitButton, hover_leave_submitButton = create_hover_functions(submit_button, "#fce5aa", "#ffda7c")
    submit_button.bind("<Enter>", hover_enter_submitButton)
    submit_button.bind("<Leave>", hover_leave_submitButton)
    regist_new_member_canvas.create_window(100, 390, window=submit_button)

    
    



window = Tk()
window.state("zoomed")
window.title("ESES Database")
icon = PhotoImage(file="ESES.png")
window.iconphoto(True, icon)
window.config(background="#ffda7c")

screen_width = window.winfo_screenwidth()-50
screen_height = window.winfo_screenheight()-100


main_screen_canvas = Canvas(window, width=WIDTH, height=HEIGHT, background="#ffda7c", borderwidth=0, highlightthickness=0)
main_screen_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

original_logo = Image.open("ESES.png")
new_logo_height = 250
new_logo_width = 250
resized_logo = original_logo.resize((new_logo_width, new_logo_height), Image.Resampling.LANCZOS)
tk_logo = ImageTk.PhotoImage(resized_logo)

main_screen_logo = main_screen_canvas.create_image(150, 250, image=tk_logo, anchor=CENTER)
main_screen_text = main_screen_canvas.create_text(650, 250, text="Welcome to ESES Database", anchor=CENTER, font=("Courier New", 30))
press_enter = main_screen_canvas.create_text(500, 480, text="Press (Enter) to start", anchor=CENTER, font=("comic sans", 30), fill="red")

window.bind("<Return>", start_animation)
pulse_text()


window.mainloop()