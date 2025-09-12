from libraries import *
import API

window = Tk()
window.state("zoomed")
window.title("ESES Database")
icon = PhotoImage(file="ESES.png")
window.iconphoto(True, icon)
window.config(background="#ffda7c")

test_button = Button(window)
test_button.config(
                    text= "Add new member",
                    width=50,
                    height=50,
                    command= API.Create_member
            )

test_button.pack()

window.mainloop()