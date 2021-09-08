"""FortiGate config generator toolkit"""
# question_box.py

import os
from tkinter import Button, Canvas, IntVar, Label, Radiobutton, Tk, messagebox

import PIL.Image
from PIL import ImageTk
from python_settings import settings


class FortiGUI():
    """GUI class"""

    def __init__(self):
        """Init class"""
        self.model = ""
        self.root = Tk()

    def on_closing(self):
        """Close window action"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.model = False
            self.root.destroy()

    def display_choice(self, prompt, options):
        """Ask for a platform"""

        os.environ["SETTINGS_MODULE"] = 'settings'

        current_dir = (os.path.dirname(os.path.realpath(__file__)))
        image_dir = os.path.join(current_dir, "image", "small_logo.png")

        self.root.geometry("300x200")
        self.root.resizable(width=False, height=False)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.wm_attributes('-toolwindow', 'True')
        self.root.title('FortiGen')

        self.root.configure(background=settings.COLOR)

        self.root.eval('tk::PlaceWindow . center')

        canvas = Canvas(self.root, width=300, height=200, bg=settings.COLOR)
        canvas.grid(columnspan=4, rowspan=4)

        #logo
        logo = PIL.Image.open(image_dir)
        logo = ImageTk.PhotoImage(logo)
        logo_label = Label(image=logo, borderwidth = 0)
        logo_label.image = logo
        logo_label.grid(column=1, row=0)

        if prompt:
            Label(self.root, text = prompt, background = settings.COLOR).grid(column=1, row=1)
        self.model = IntVar()
        for i, option in enumerate(options):
            Radiobutton(self.root, text=option, anchor = "center", background=settings.COLOR,
                        variable=self.model, value=i).grid(column=1, row = i+2)

        # Button(text="Submit", command=self.root.destroy).pack()
        Button(text = "Submit", background = settings.COLOR,
              command = self.root.destroy).grid(column = 1, row = 4)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

        if self.model:
            return options[self.model.get()]

        return False


def main():
    """Main"""

if __name__ == "__main__":
    main()
