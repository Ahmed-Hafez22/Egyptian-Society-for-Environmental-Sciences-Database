from libraries import *
import API
import SideFunctions

WIDTH = 1000
HEIGHT = 500
yVelocity = 30

window = Tk()
window.state("zoomed")
window.title("ESES Database")
icon = PhotoImage(file="ESES.png")
window.iconphoto(True, icon)
window.config(background="#ffda7c")

screen_width = window.winfo_screenwidth()-50
screen_height = window.winfo_screenheight()-100


main_screen_frame = Frame(window, width=WIDTH, height=HEIGHT, background="#ffda7c")
main_screen_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

original_logo = Image.open("ESES.png")
new_logo_height = 250
new_logo_width = 250
resized_logo = original_logo.resize((new_logo_width, new_logo_height), Image.Resampling.LANCZOS)
tk_logo = ImageTk.PhotoImage(resized_logo)

quick_canvas = Canvas(window, width=WIDTH, height=HEIGHT, background="#ffda7c")
quick_canvas.place(relx=05., rely=0.5, anchor=CENTER)

main_screen_logo = quick_canvas.create_image(150, 250, image=tk_logo, anchor=CENTER)
main_screen_text = quick_canvas.create_text(650, 250, text="Welcome to ESES Database", anchor=CENTER, font=("Courier New", 30))
press_enter = quick_canvas.create_text(500, 480, text="Press (Enter) to start", anchor=CENTER, font=("comic sans", 30), fill="red")

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
    quick_canvas.itemconfig(press_enter, fill=color)
    window.after(25, _animate_color, from_rgb, to_rgb, next_dir, steps, step + 1)
    
def fade_text_permanently(step=0, steps=10):
    """Handles the final fade-out of the text after Enter is pressed."""
    if step > steps: return
    start_rgb, end_rgb = ((255, 0, 0), (255, 218, 124))
    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * step / steps)
    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * step / steps)
    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * step / steps)
    color = f"#{r:02x}{g:02x}{b:02x}"
    quick_canvas.itemconfig(press_enter, fill=color)
    window.after(25, fade_text_permanently, step + 1)
    

def move_main_screen(event=None):
        quick_canvas.move(main_screen_logo, 0, -yVelocity)
        quick_canvas.move(main_screen_text, 0, -yVelocity)
        if quick_canvas.coords(main_screen_logo)[1] > -150:
                window.after(20, move_main_screen)
        else:
                quick_canvas.place_forget()
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
                quick_canvas.itemconfig(press_enter, fill=color)

                # Schedule next step
                window.after(50, fade_text, step + 1, steps)

def start_animation(event=None):
    global is_fading
    if not is_fading: return # Prevent accidental double-press
    is_fading = False
    window.unbind("<Return>")
    move_main_screen()
    fade_text_permanently()

window.bind("<Return>", start_animation)
pulse_text()

def create_hover_functions(button_widget, hover_color, leave_color):
    def on_enter(event=None):
        button_widget.config(background=hover_color)

    def on_leave(event=None):
        button_widget.config(background=leave_color)

    return on_enter, on_leave
    
def clean_container():
    for widget in main_screen_frame.winfo_children():
        widget.destroy() 



def show_operation_menu():
    clean_container()
    Label(main_screen_frame,text="ESES Database", font=("courier new", 30), bg="#ffda7c").grid(row=0, column=0, columnspan=4)
    operationsList = Label(main_screen_frame,text="Operations List:-", font=("Calibri", 30))
    operationsList.grid(row=0, column=0)
        

        
def import_excel_file(event=None):
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
                msg = import_excel_file_canvas.create_text(300, 250, text= excel_file_name + " got added successfully", font=("Arial", 18), state="normal")
                import_excel_file_canvas.after(3000, lambda: import_excel_file_canvas.itemconfig(msg, state="hidden"))
            else:
                msg = import_excel_file_canvas.create_text(300, 250, text= excel_file_name + " didn't get added", font=("Arial", 18), state="normal")
                import_excel_file_canvas.after(3000, lambda: import_excel_file_canvas.itemconfig(msg, state="hidden"))


    chooseFileButton = Button(window, background="#ffda7c", 
                              font=("oswald", 25), activebackground="#fac84a",
                              text="Choose a file",
                              command=open_excel_file,
                              relief="groove")
    returnToMainMenuButton = Button(window, background="#ffda7c",
                                    font=("oswald", 25),
                                    activebackground="#fac84a",
                                    text="Return",
                                    relief="groove")
    
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

        reg_date_str = entries["Registration Date:"].get()
        if reg_date_str:
            try:
                cleaned_reg_date = sub(r'\D', " ", reg_date_str)
                day, month, year = [int(part) for part in cleaned_reg_date.split()]
                reg_date = datetime(year, month, day).strftime("%d %m %Y")
            except(ValueError, TypeError):
                reg_date = datetime.now().strftime("%d %m %Y")     
        else:
            reg_date = datetime.now().strftime("%d %m %Y") 
        
        new_member_dict = {
            "member_name" : entries["Member Name:"].get(),
            "phone_number" : entries["Phone Number:"].get(),
            "member_email" : entries["Member Email:"].get(),
            "reg_date" : reg_date
        }
        
        if new_member_dict["member_name"] == "":
            regist_new_member_canvas.create_text(380, 390, text="No info submitted", font=("Arial", 18))
        else:
            request = requests.post(API_URL, json=new_member_dict)

        if request.text == f"\"{new_member_dict["member_name"]} got added successfully\"":
            msg = regist_new_member_canvas.create_text(400, 390, 
                                                       text=new_member_dict["member_name"] + " got add successfully",
                                                       font=("Arial", 18),
                                                       state="normal")
            regist_new_member_canvas.after(3000, lambda: regist_new_member_canvas.itemconfig(msg, state="hidden"))
            
        elif request.text == f"\"{new_member_dict["member_name"]} is already in the database\"":
            msg = regist_new_member_canvas.create_text(430, 390,
                                                       text=new_member_dict["member_name"] + " is already in the database",
                                                       font=("Arial", 18),
                                                       state="normal")
            regist_new_member_canvas.after(3000, lambda: regist_new_member_canvas.itemconfig(msg, state="hidden"))
            
        else:
            msg = regist_new_member_canvas.create_text(400, 390,
                                                       text=new_member_dict["member_name"] + " didn't get added",
                                                       font=("Arial", 18),
                                                       state="normal")
            regist_new_member_canvas.after(3000, lambda: regist_new_member_canvas.itemconfig(msg, state="hidden"))


    regist_new_member_canvas = Canvas(window, width=screen_width, height=screen_height, background="#ffda7c")
    regist_new_member_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    newMember_frame = Frame(regist_new_member_canvas, bg="#ffda7c")
    regist_new_member_canvas.create_window((0,0), width=screen_width, height=screen_height, window=newMember_frame, anchor="nw")
    
    ESES_label = Label(newMember_frame, text="ESES Database", font=("courier new", 30), background="#ffda7c")
    ESES_label.grid(row=0, column=2, columnspan=4, sticky="ew")
    
    reg_label = Label(newMember_frame, text="Register a new member:-", font=("calibri", 25), background="#ffda7c")
    reg_label.grid(row=1, column=0)
    
    fields = [
        ("Member Name:",          2),
        ("Phone Number:",         3),
        ("Registration Date:",    4),
        ("Member Email:",         5)
    ]
    
    entries = {}
    labels = {}
    
    for label_text, row in fields:
        label = Label(newMember_frame, text=label_text, background="#ffda7c", font=("Arial", 15))
        label.grid(row=row, column=0, pady=5)
        labels[label_text] = label
        
        entry = Entry(newMember_frame, font=(15), width=20)
        entry.grid(row=row, column=1, pady=5)
        entries[label_text] = entry
    
    
    submit_button = Button(newMember_frame,
                           text="Submit",
                           relief="groove",
                           font=("oswald", 15),
                           command=submit_new_member_info,
                           activebackground="#fac84a",
                           background="#ffda7c",
                           )
    
    returnToMainMenuButton = Button(newMember_frame,
                                    text="Return",
                                    relief="groove",
                                    font=("oswald", 15),
                                    background="#ffda7c",
                                    activebackground="#fac84a")
    
    hover_enter_submitButton, hover_leave_submitButton = create_hover_functions(submit_button, "#fce5aa", "#ffda7c")
    hover_enter_returnButton, hover_leave_returnButton = create_hover_functions(returnToMainMenuButton, "#fce5aa", "#ffda7c")
    
    returnToMainMenuButton.bind("<Enter>", hover_enter_returnButton)
    returnToMainMenuButton.bind("<Leave>", hover_leave_returnButton)
    
    submit_button.bind("<Enter>", hover_enter_submitButton)
    submit_button.bind("<Leave>", hover_leave_submitButton)

    
    






window.mainloop()