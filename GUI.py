from libraries import *
import API

WIDTH = 1000
HEIGHT = 500
yVelocity = 30

def show_operation_menu():
        Operation_menu = Canvas(window, width=1500, height=820, background="#ffda7c")
        Operation_menu.place(relx=0.5, rely=0.5, anchor=CENTER)
        Operation_menu_esesDB = Operation_menu.create_text(750, 30, text="ESES Database", font=("courier new", 30))
        Operation_menu_operationList = Operation_menu.create_text(150, 100, text="Operations List:- ", font=("calibri", 30))
        import_excel_file_button = Button(Operation_menu, width=50 ,height=50, background="ffda7c", text="1-Import Excel File")
        import_excel_file_button.pack()
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
        
        

window = Tk()
window.state("zoomed")
window.title("ESES Database")
icon = PhotoImage(file="ESES.png")
window.iconphoto(True, icon)
window.config(background="#ffda7c")


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