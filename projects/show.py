from main import present_folder
import customtkinter
import os

class OptionFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        self.values = values
        self.buttons = []

        for i, value in enumerate(self.values):
            button = customtkinter.CTkButton(self, text=value, command=lambda:present_folder(value), height=80, width=80)
            button.pack(side="left", padx=10, pady=(10, 0))
            self.buttons.append(button)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gesture-Flow")
        self.geometry("900x1080")
        self.grid_columnconfigure(0)
        self.grid_rowconfigure(0, weight=1)

        options = os.listdir('images')
        self.option_frame = OptionFrame(self, "Present Options", options)
        #self.option_frame.grid(row=0, column=0, padx=10, pady=(10, 0), columnspan=5, rowspan=5)
        self.option_frame.pack(fill="both", expand=True, side="left")

        self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback)
        #self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    def button_callback(self):
        print("Button Pressed")

if __name__ == '__main__':
    app = App()
    app.mainloop()
