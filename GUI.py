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

original_logo = Image.open("ESES.png")
new_logo_height = 250
new_logo_width = 250
resized_logo = original_logo.resize((new_logo_width, new_logo_height), Image.Resampling.LANCZOS)
tk_logo = ImageTk.PhotoImage(resized_logo)

main_screen_frame = Frame(window, width=screen_width, height=screen_height, background="#ffda7c")


quick_canvas = Canvas(window, width=WIDTH, height=HEIGHT, background="#ffda7c", borderwidth=0, highlightthickness=0)
quick_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

main_screen_logo = quick_canvas.create_image(150, 250, image=tk_logo, anchor=CENTER)
main_screen_text = quick_canvas.create_text(650, 250, text="Welcome to ESES Database", anchor=CENTER, font=("Courier New", 30))
press_enter = quick_canvas.create_text(500, 480, text="Click to start", anchor=CENTER, font=("comic sans", 30), fill="red")

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
    window.unbind("<Button-1>")
    move_main_screen()
    fade_text_permanently()
    main_screen_frame.pack(fill="both", expand=True)  # Ensure frame fills window


window.bind("<Button-1>", start_animation)
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
    
    for i in range(20):
        main_screen_frame.rowconfigure(i, weight=0)
    for i in range(7):
        main_screen_frame.columnconfigure(i, weight=0)
    
def remove_msg(msg):
    main_screen_frame.after(3000, lambda: msg.grid_remove())

def show_eses_label():
    eses_label = Label(main_screen_frame, text="ESES Database", font=("courier new", 30), bg="#ffda7c", anchor="center")
    eses_label.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(10,0))
    
def show_label(text):
    label = Label(main_screen_frame,
          text=text,
          font=("Arial", 30),
          bg="#ffda7c").grid(row=1, column=0, padx=(10,0),  sticky="nw")
    

def create_treeview_table(lst, style_name):
        columns = lst[0]  # Header row
        style = ttk.Style()
        style.configure("Treeview",
                        background="#ffda7c",
                        fieldbackground = "#ffda7c")
        tree = ttk.Treeview(main_screen_frame, columns=columns, show="headings", style=style_name)
        
        # Define column headings and widths
        column_widths = [15, 150, 200, 120, 120, 120, 80]  # Adjust as needed
        
        for i, col in enumerate(columns):
            tree.heading(col, text=col)
            tree.column(col, width=column_widths[i], minwidth=50)
        
        # Add data rows (skip header row)
        for row_data in lst[1:]:
            tree.insert("", "end", values=row_data)
        
        # Add scrollbars
        v_scrollbar = Scrollbar(main_screen_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=v_scrollbar.set)
        
        # Grid everything
        tree.grid(row=2, column=0, columnspan=len(lst[0]), sticky="nsew")
        v_scrollbar.grid(row=2, column=len(lst[0]), sticky="ns", pady=(0,2))
        

def style_treeView():
    style = ttk.Style()
    style.theme_use('clam')
        
    style.configure("Custom.Treeview",
                    background="#ffda7c",
                    fieldbackground = "#ffda7c",
                    rowheight= 25)
        
    style.configure("Custom.Treeview.Heading",
                    background="#ffda7c",        # Header bg
                    foreground="black",          # Header text
                    font=('Arial', 12, 'bold'))
    return "Custom.Treeview"

def show_operation_menu():
    clean_container()
    main_screen_frame.columnconfigure(0, weight=1)
    show_eses_label()
    show_label("Operations List:-")

    buttons_data = [
        ("1-Import Excel File", import_excel_file, 2),
        ("2-Register New Member", regist_new_member, 3),
        ("3-Show Members", show_members, 4),
        ("4-Search for Member", search_for_member, 5),
        ("5-Edit Member Info", edit_member_info, 6),
        ("6-Delete Member", delete_member, 7)
    ]

    buttons = {}

    for button_text, button_command, button_row in buttons_data:
        button = Button(main_screen_frame,
               text=button_text,
               bg="#ffda7c",
               relief="flat",
               font=("oswald", 25),
               activebackground= "#fac84a",
               command=button_command
               )
        button.grid(row=button_row, column=0, padx=(30,0), pady=(10,0), sticky="nw")
        hover_enter, hover_leave = create_hover_functions(button, "#fce5aa", "#ffda7c")
        button.bind("<Enter>", hover_enter)
        button.bind("<Leave>", hover_leave)
        buttons[button_text] = button
        
def import_excel_file(event=None):
    clean_container()
    main_screen_frame.columnconfigure(0, weight=1)  # Button column - don't expand
    main_screen_frame.columnconfigure(1, weight=0)  # Message column - don't expand
    main_screen_frame.columnconfigure(2, weight=0)  # Message column - don't expand
    main_screen_frame.columnconfigure(3, weight=1)  # Message column - don't expand
    show_eses_label()
    show_label("Import Excel File:")
    def open_excel_file(event=None):

        filePath = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if filePath:
            status = SideFunctions.import_excel_file(filePath)
            excel_file_name = os.path.splitext(os.path.basename(filePath))[0]
            if status == True:
                msg = Label(main_screen_frame, text=excel_file_name+" got added sucessfully", font=("calibri", 20), bg="#ffda7c", fg="green")
                msg.grid(row=2, column=0,columnspan=2, sticky="w", padx=(300,0))
                remove_msg(msg)
            else:
                msg = Label(main_screen_frame, text=excel_file_name+" didn't get added", font=("calibri", 20), bg="#ffda7c", fg="red")
                msg.grid(row=2, column=0, columnspan=2, sticky="w", padx=(300,0))
                remove_msg(msg)


    buttons_data = [
        ("Choose a file", open_excel_file, 2),
        ("Return", show_operation_menu, 3)
    ]

    buttons = {}

    for button_text, button_command, button_row in buttons_data:
        button = Button(main_screen_frame,
                        text=button_text,
                        bg="#ffda7c",
                        relief="groove",
                        activebackground="#fac84a",
                        font=("oswald", 25),
                        command=button_command)
        button.grid(row=button_row, column=0, padx=(40,0), pady=(10,0), sticky="nw")
        hover_enter, hover_leave = create_hover_functions(button, "#fce5aa", "#ffda7c")
        button.bind("<Enter>", hover_enter)
        button.bind("<Leave>", hover_leave)
        buttons[button_text] = button


def regist_new_member(event = None):
    clean_container()
    main_screen_frame.columnconfigure(0, weight=0)
    main_screen_frame.columnconfigure(1, weight=0)
    main_screen_frame.columnconfigure(3, weight=1)
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
        new_member_dict["member_name"] = SideFunctions.modify_name(new_member_dict["member_name"]) 

        request = requests.post(API_URL, json=new_member_dict, timeout=10)

        if request.text == f"\"{new_member_dict["member_name"]} got added successfully\"":
            msg = Label(main_screen_frame,
                        text=new_member_dict["member_name"]+" got added successfully",
                        bg="#ffda7c",
                        fg="green",
                        font=("arial", 15))
            msg.grid(row=6, column=1, pady=(10,0), sticky="w")
            remove_msg(msg)
        elif request.text == f"\"{new_member_dict["member_name"]} is already in the database\"":
            msg = Label(main_screen_frame,
                        text=new_member_dict["member_name"] + " is already in the database",
                        font=("Arial", 18),
                        bg="#ffda7c",
                        fg="red",
                        state="normal")
            msg.grid(row=6, column=1, pady=(10,0), sticky="w")
            remove_msg(msg)
        elif request.text == f"\"Please enter a valid name\"":
            msg = Label(main_screen_frame,
                                text="Please enter a valid name",
                                font=("arial", 15),
                                bg="#ffda7c",
                                fg="red",
                                state="normal")
            msg.grid(row=6, column=1, pady=(10,0), sticky="w")
            remove_msg(msg)
        else:
            msg = Label(main_screen_frame,
                        text=new_member_dict["member_name"] + " didn't get added",
                        font=("Arial", 18),
                        bg="#ffda7c",
                        fg= "red",
                        state="normal")
            msg.grid(row=6, column=1, pady=(10,0), sticky="w")
            remove_msg(msg)

    show_eses_label()
    
    show_label("Register New Member:")
    
    fields = [
        ("Member Name:",          2),
        ("Phone Number:",         3),
        ("Registration Date:",    4),
        ("Member Email:",         5)
    ]
    
    entries = {}
    labels = {}
    
    for label_text, row in fields:
        label = Label(main_screen_frame, text=label_text, background="#ffda7c", font=("Arial", 15))
        label.grid(row=row, column=0, pady=5, sticky="w", padx=(30,0))  
        labels[label_text] = label

        
        entry = Entry(main_screen_frame, font=15, width=20)
        entry.grid(row=row, column=0, pady=5, sticky="e") 
        entries[label_text] = entry
    

    buttons_data = [
        ("Submit", submit_new_member_info, 100),
        ("Return", show_operation_menu, 200)
    ]
    buttons = {}

    for button_text, button_command, button_xpading in buttons_data:
        button = Button(main_screen_frame,
                        text=button_text,
                        relief="groove",
                        font=("oswald", 15),
                        command=button_command,
                        bg="#ffda7c",
                        activebackground="#fac84a")
        button.grid(row=6, column=0, padx=(button_xpading, 0), pady=(10,0), sticky="w")
        hover_enter, hover_leave = create_hover_functions(button, "#fce5aa", "#ffda7c")
        button.bind("<Enter>", hover_enter)
        button.bind("<Leave>", hover_leave)
        buttons[button_text]= button

def show_members(event=None):
    clean_container()
    API_URL = "http://127.0.0.1:8000/Show-Members"
    request = requests.get(API_URL)
    members = request.json()

    main_screen_frame.columnconfigure(0, weight=0)

    lst_of_all_members = [
        ("ID", "Member Name", "Email", "Phone Number", "Registration Date", "Expiration Date", "Status"),
    ]
    for member in members:
        lst_of_all_members.append(tuple(member.values()))

    show_eses_label()
    show_label("All Members:")
    tree_style = style_treeView()
    create_treeview_table(lst_of_all_members, tree_style)
    
    returnButton = Button(main_screen_frame,
                        text="Return",
                        relief="groove",
                        font=("oswald", 15),
                        command=show_operation_menu,
                        bg="#ffda7c",
                        activebackground="#fac84a")
    hover_enter, hover_leave = create_hover_functions(returnButton, "#fce5aa", "#ffda7c")
    returnButton.bind("<Enter>", hover_enter)
    returnButton.bind("<Leave>", hover_leave)
    returnButton.grid(row=3, column=0)
    main_screen_frame.grid_rowconfigure(2, weight=1)
    main_screen_frame.grid_columnconfigure(0, weight=1)


def search_for_member(mode="search", event=None):
    clean_container()
    main_screen_frame.columnconfigure(0, weight=0)
    main_screen_frame.columnconfigure(1, weight=0)
    main_screen_frame.columnconfigure(3, weight=1)
    show_eses_label()
    show_label("Search for Member:")
    fields = [
       ("Member First Name:", 2)
   ]
    
    for text, row_pos in fields:
        label = Label(main_screen_frame, text=text, background="#ffda7c", font=("Arial", 15))
        label.grid(row=row_pos, column=0, pady=5, sticky="w", padx=(30, 0))  

        entry = Entry(main_screen_frame, font=15, width=20)
        entry.grid(row=row_pos, column=0, pady=5, sticky="e", padx=(220, 0))

    def search(event=None):
        member_name = entry.get()
        member_name = member_name.capitalize().strip()
        API_URL = f"http://127.0.0.1:8000//Search-for-Member/Member_name?member_name={member_name}"
        request = requests.get(API_URL)
        response = request.json()
        lst_of_members = [
            ("ID", "Member Name", "Email", "Phone Number", "Registration Date", "Expiration Date", "Status"),
        ]
        for member in response:
            lst_of_members.append(tuple(member.values()))
        
        clean_container()
        show_eses_label()
        show_label("Members with the Same First Name:")

        tree_style = style_treeView()
        create_treeview_table(lst_of_members, tree_style)
        main_screen_frame.grid_rowconfigure(2, weight=1)
        main_screen_frame.grid_columnconfigure(0, weight=1)
        if mode == "search":
            returnButton = Button(main_screen_frame,
                        text="Return",
                        relief="groove",
                        font=("oswald", 15),
                        command=search_for_member,
                        bg="#ffda7c",
                        activebackground="#fac84a")
            hover_enter, hover_leave = create_hover_functions(returnButton, "#fce5aa", "#ffda7c")
            returnButton.bind("<Enter>", hover_enter)
            returnButton.bind("<Leave>", hover_leave)
            returnButton.grid(row=3, column=0)
        else:
            nextButton = Button(main_screen_frame,
                                text="Next",
                                relief="groove",
                                font=("oswald", 15),
                                command= lambda: edit_member_info(1),
                                bg="#ffda7c",
                                activebackground="#fac84a")
            hover_enter, hover_leave = create_hover_functions(nextButton, "#fce5aa", "#ffda7c")
            nextButton.bind("<Enter>", hover_enter)
            nextButton.bind("<Leave>", hover_leave)
            nextButton.grid(row=3, column=0)
    
    buttons_data = [
        ("Search", search, 100),
        ("Return", show_operation_menu, 200)
    ]
    buttons = {}
    for button_text, button_command, x_padding in buttons_data:
        button = Button(main_screen_frame,
                        text=button_text,
                        relief="groove",
                        font=("oswald", 15),
                        command=button_command,
                        bg="#ffda7c",
                        activebackground="#fac84a")
        button.grid(row=3, column=0, padx=(x_padding, 0), pady=(10, 0), sticky="w")
        hover_enter, hover_leave = create_hover_functions(button, "#fce5aa", "#ffda7c")
        button.bind("<Enter>", hover_enter)
        button.bind("<Leave>", hover_leave)
        buttons[button_text] = button

def edit_member_info(value = 0, event=None):
    if value == 0:
        search_for_member(mode="edit")
    else:
        clean_container()
        show_eses_label()
        show_label("Edit Member Info:")
        main_screen_frame.columnconfigure(0, weight=0)
        main_screen_frame.columnconfigure(1, weight=0)
        main_screen_frame.columnconfigure(3, weight=1)

        def edit(event=None):
            member_id = entries["ID:"].get()
            API_URL = f"http://127.0.0.1:8000/Update-Member/Member_id?member_id={member_id}"

            edited_dict = {
                "member_name" : entries["Member Name:"].get(),
                "phone_number" : entries["Phone Number:"].get(),
                "reg_date" : entries["Registration Date:"].get(),
                "member_email" : entries["Member Email:"].get()
            }

            request = requests.put(API_URL, json=edited_dict)

            name = (request.text).removeprefix("\"").removesuffix("\"")

            if member_id == None:
                print("hi")

            if request.status_code == 200:
                msg = Label(main_screen_frame,
                            text=name + "'s info was edited successfully",
                            font=("Arial", 18),
                            bg="#ffda7c",
                            fg="green")
                msg.grid(row=7, column=1, sticky="w", pady=(10,0))
                remove_msg(msg)
            else:
                msg = Label(main_screen_frame,
                            text=name + "'s info didn't get edited",
                            font=("Arial", 18),
                            bg="#ffda7c",
                            fg="red")
                msg.grid(row=7, column=1, sticky="w", pady=(10,0))
                remove_msg(msg)

        fields_data = [
            ("ID:", 2),
            ("Member Name:", 3),
            ("Phone Number:", 4),
            ("Registration Date:", 5),
            ("Member Email:", 6)
        ]
        entries = {}
        labels = {}

        for label_text, row in fields_data:
            label = Label(main_screen_frame, text=label_text, background="#ffda7c", font=("Arial", 15))
            label.grid(row=row, column=0, pady=5, sticky="w", padx=(30,0))  
            labels[label_text] = label

        
            entry = Entry(main_screen_frame, font=15, width=20)
            entry.grid(row=row, column=0, pady=5, sticky="e", padx=(210,0)) 
            entries[label_text] = entry
        
        buttons_data = [
            ("Edit", edit, 100),
            ("Return", show_operation_menu, 200)
        ]
        buttons = {}
        for button_text, button_command, x_padding in buttons_data:
            button = Button(main_screen_frame,
                            text=button_text,
                            relief="groove",
                            font=("oswald", 15),
                            command=button_command,
                            bg="#ffda7c",
                            activebackground="#fac84a")
            button.grid(row=7, column=0, padx=(x_padding, 0), pady=(10, 0), sticky="w")
            hover_enter, hover_leave = create_hover_functions(button, "#fce5aa", "#ffda7c")
            button.bind("<Enter>", hover_enter)
            button.bind("<Leave>", hover_leave)
            buttons[button_text] = button
        
def delete_member(event=None):
    clean_container()
    main_screen_frame.columnconfigure(0, weight=0)
    main_screen_frame.columnconfigure(1, weight=0)
    main_screen_frame.columnconfigure(3, weight=1)
    show_eses_label()
    show_label("Delete Member:")

    def delete():
        member_id = entry.get()
        API_URL = f"http://127.0.0.1:8000/Delete-Member/{member_id}"
        request = requests.delete(API_URL)
        name = (request.text).removeprefix("\"").removesuffix("\"")

        if request.status_code == 200:
            msg = Label(main_screen_frame,
                        text=name + " got deleted successfully",
                        font=("Arial", 18),
                        bg="#ffda7c",
                        fg="green")
            msg.grid(row=3, column=1, pady=(10,0))
            remove_msg(msg)
        else:
            msg = Label(main_screen_frame,
                        text=name + "didn't get deleted",
                        font=("Arial", 18),
                        bg="#ffda7c",
                        fg="red")
            msg.grid(row=3, column=1, pady=(10,0))
            remove_msg(msg)

    entry = Entry(main_screen_frame, font=15, width=20)
    entry.grid(row=2, column=0, sticky="e", padx=(150,0))
    label = Label(main_screen_frame, text="Member ID:", background="#ffda7c", font=("Arial", 15))
    label.grid(row=2, column=0, sticky="w", padx=(30,0))

    buttons_data = [
        ("Delete", delete, 100),
        ("Return", show_operation_menu, 200)
    ]
    buttons = {}

    for button_text, button_command, x_padding in buttons_data:
        button = Button(main_screen_frame,
                        text=button_text,
                        relief="groove",
                        font=("oswald", 15),
                        command=button_command,
                        bg="#ffda7c",
                        activebackground="#fac84a")
        button.grid(row=3, column=0, padx=(x_padding, 0), pady=(10, 0), sticky="w")
        hover_enter, hover_leave = create_hover_functions(button, "#fce5aa", "#ffda7c")
        button.bind("<Enter>", hover_enter)
        button.bind("<Leave>", hover_leave)
        buttons[button_text] = button
window.mainloop()