#imports

from tkinter import *
from PIL import ImageTk, Image
import os

#working functions
def resize_images(images, size):
    resized_images = []
    for img in images:
        resized_img = img.resize(size)
        resized_images.append(ImageTk.PhotoImage(resized_img))
    return resized_images

def rotate_img():
    global counter
    img_label.config(image=img_array[counter % len(img_array)])
    counter = counter + 1

def prev_item():
    global counter
    if counter > 1:
        img_label.config(image=img_array[counter - 2])
        counter = counter - 1

def open_grid_view():
    grid_window = Toplevel(root)
    grid_window.title('Grid View')
    grid_window.geometry('800x600')

    canvas = Canvas(grid_window)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(grid_window, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    scrollbar_x = Scrollbar(grid_window, orient=HORIZONTAL, command=canvas.xview)
    scrollbar_x.pack(side=BOTTOM, fill=X)

    canvas.configure(yscrollcommand=scrollbar.set, xscrollcommand=scrollbar_x.set)

    frame = Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor='nw')

    for i, img in enumerate(grid_resized_img_array):
        row = i // 4
        col = i % 4
        img_label = Label(frame, image=img)
        img_label.grid(row=row, column=col, padx=10, pady=10)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox('all'))

    def mouse_scroll(event):
        if event.delta:
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1

            canvas.yview_scroll(move, "units")

    frame.bind('<Configure>', on_configure)
    canvas.bind_all("<MouseWheel>", mouse_scroll)
    
#welcome box func
def show_welcome_and_open_window():
    show_welcome()
    root.after(2000, open_main_window)  # Open the main window after 2 seconds

def show_welcome():
    welcome_window = Toplevel(root)
    welcome_window.title('Welcome to Wallpapers')
    welcome_window.geometry('400x200')

    welcome_label = Label(welcome_window, text="Welcome to Wallpapers!\nClick 'VIEW WALLPAPERS' to start viewing.", font=("Helvetica", 16))
    welcome_label.pack(expand=True)

#main window
def open_main_window():
    global img_label
    root.deiconify()  # Show the main window
    root.title('Wallpaper Anime')
    root.geometry('650x750')
    root.configure(background='black')

    img_label = Label(root, image=img_array[0])
    img_label.pack(pady=(20, 20))

# BUTTON
    next_btn = Button(root, text='NEXT WALLPAPER', font=25, fg='black', bg='yellow', width=18, height=2, command=rotate_img)
    next_btn.pack(side=RIGHT)

    prev_btn = Button(root, text='PREV WALLPAPER', font=25, fg='black', bg='yellow', width=18, height=2, command=prev_item)
    prev_btn.pack(side=LEFT)

    grid_btn = Button(root, text='Grid View', font=20, fg='black', bg='green', width=16, height=2, command=open_grid_view)
    grid_btn.pack(side=LEFT)

    exit_btn = Button(root, text='Exit Program', font=20, fg='black', bg='red', width=16,height=2, command=exit_program)
    exit_btn.pack(side=RIGHT)
    
#closing window
def exit_program():
    root.destroy()

counter = 1
root = Tk()
root.withdraw()  # Hide the main window initially
files = os.listdir('wallpapers')

# IMG for main window
main_img_array = []
for file in files:
    img = Image.open(os.path.join('wallpapers', file))
    main_img_array.append(img)

# IMG for grid view
grid_img_array = main_img_array.copy()

# Resizing images for the main window
img_array = resize_images(main_img_array, (565, 665))

# Resizing images for the grid view window
grid_resized_img_array = resize_images(grid_img_array, (200, 200))

show_welcome_and_open_window()
root.mainloop()