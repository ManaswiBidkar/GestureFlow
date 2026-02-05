from main import present
from tkinter import filedialog
import os
from tkinter import Button


def open_file_dialog(window):
    file_path = filedialog.askopenfilename(
        title="Select a PowerPoint file",
        filetypes=[("PowerPoint Files", "*.pptx")]
    )
    if file_path:
        print(f"Selected file: {file_path}")
        # Call the function from another file with the selected file path
        window.destroy()
        present(file_path, os.path.isdir(file_path))


def open_folder(window, folder_name):
    window.destroy()
    present(folder_name, True)


def get_open_folder(window, folder_name):
    def opener():
        open_folder(window, folder_name)
    return opener


def show_folder_icons(window, canvas, folder_image, folders):
    disp = 0
    for i, folder in enumerate(folders):
        folder_icon_button = Button(
            image=folder_image,
            borderwidth=0,
            highlightthickness=0,
            command=get_open_folder(window, folder),
            relief="flat"
        )
        folder_icon_button.place(
            x=177.0+disp,
            y=211.0,
            width=178.0,
            height=163.0
        )

        canvas.create_text(
            191.0+disp,
            395.0,
            anchor="nw",
            text=folder,
            fill="#000000",
            font=("Inter", 25 * -1)
        )
        disp += 255
