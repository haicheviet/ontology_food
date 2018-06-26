from tkinter import *
import tkinter.messagebox as tm


class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master.title("Hệ thống tư vấn dinh dưỡng")
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        width = 280
        height = 140
        

        self.master.geometry("%dx%d" % (width, height))

        self.label_username = Label(self, text="Username:")
        self.label_password = Label(self, text="Password:")
        self.label_title = Label(self, text = "Welcome", font=("Arial", 20), anchor="center")
        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_title.grid(row=0, column = 1)
        self.label_username.grid(row=1, sticky=E)
        self.label_password.grid(row=2, sticky=E)
        self.entry_username.grid(row=1, column=1)
        self.entry_password.grid(row=2, column=1)

        self.checkbox = Checkbutton(self, text="Keep me logged in")
        self.checkbox.grid(columnspan=2)

        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)

        self.pack()

    def _login_btn_clicked(self):
        # print("Clicked")
        username = self.entry_username.get()
        password = self.entry_password.get()

        # print(username, password)

        if username == "john" and password == "password":
            tm.showinfo("Login info", "Welcome John")
        else:
            tm.showerror("Login error", "Incorrect username")


root = Tk()
lf = LoginFrame(root)
root.mainloop()