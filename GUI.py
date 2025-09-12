from libraries import *
import API

WIDTH = 1000
HEIGHT = 500
yVelocity = 30

def move_main_screen(event=None):
        main_screen_canvas.move(main_screen_logo, 0, -yVelocity)
        main_screen_canvas.move(main_screen_text, 0, -yVelocity)
        if main_screen_canvas.coords(main_screen_logo)[1] > -150:
                window.after(20, move_main_screen)
        else:
                main_screen_canvas.place_forget()

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
        window.unbind("<Return>")
        move_main_screen()
        fade_text()
        
        

window = Tk()
window.state("zoomed")
window.title("ESES Database")
icon = PhotoImage(file="ESES.png")
window.iconphoto(True, icon)
window.config(background="#ffda7c")


main_screen_canvas = Canvas(window, width=WIDTH, height=HEIGHT, background="#ffda7c", borderwidth=0, highlightthickness=0)
main_screen_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

original_logo = Image.open("ESES.png")
new_height = 250
new_width = 250
resized_logo = original_logo.resize((new_width, new_height), Image.Resampling.LANCZOS)
tk_logo = ImageTk.PhotoImage(resized_logo)

main_screen_logo = main_screen_canvas.create_image(150, 250, image=tk_logo, anchor=CENTER)
main_screen_text = main_screen_canvas.create_text(650, 250, text="Welcome to ESES Database", anchor=CENTER, font=("Courier New", 30))
press_enter = main_screen_canvas.create_text(500, 480, text="Press (Enter) to start", anchor=CENTER, font=("comic sans", 30), fill="red")
while True:
        fade_text()
        if window.bind("<Return>"):
                break
window.bind("<Return>", start_animation)


window.mainloop()