import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from ipywidgets import widgets, VBox

# Initialize the main application window
root = tk.Tk()
root.title('Traffic Signal Allocation System')

# Function to upload and display an image
def upload_image():
    global img, img_display, canvas
    file_path = filedialog.askopenfilename()
    img = cv2.imread(file_path)
    img_display = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
    canvas.create_image(20, 20, anchor='nw', image=img_display)
    canvas.pack()

# Function to apply Canny edge detection and display the result
def apply_canny():
    global img, img_display, canvas
    if img is not None:
        edges = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 100, 200)
        img_display = ImageTk.PhotoImage(image=Image.fromarray(edges))
        canvas.create_image(20, 20, anchor='nw', image=img_display)
        canvas.pack()
    else:
        messagebox.showerror("Error", "Please upload an image first.")

# Function to count white pixels and display the result
def count_pixels():
    global img, sample_pixels, reference_pixels
    if img is not None:
        white_pixels = np.sum(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) == 255)
        sample_pixels = white_pixels
        reference_pixels = white_pixels  # Assuming reference_pixels is the same as sample_pixels for this example
        pixel_count_label.config(text=f'White Pixels: {white_pixels}')
    else:
        messagebox.showerror("Error", "Please upload an image first.")

# Function to allocate signal time based on traffic density
def allocate_time():
    global sample_pixels, reference_pixels
    if 'sample_pixels' in globals() and 'reference_pixels' in globals():
        avg = (sample_pixels / reference_pixels) * 100
        if avg >= 90:
            allocation_label.config(text="Traffic is very high. Allocation green signal time: 60 secs")
        elif 85 < avg < 90:
            allocation_label.config(text="Traffic is high. Allocation green signal time: 50 secs")
        elif 75 < avg <= 85:
            allocation_label.config(text="Traffic is moderate. Allocation green signal time: 40 secs")
        elif 50 < avg <= 75:
            allocation_label.config(text="Traffic is low. Allocation green signal time: 30 secs")
        else:
            allocation_label.config(text="Traffic is very low. Allocation green signal time: 20 secs")
    else:
        messagebox.showerror("Error", "Please count the pixels first.")

# Create a canvas to display images
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()

# Add buttons to the GUI
upload_button = tk.Button(root, text='Upload Image', command=upload_image)
upload_button.pack()

canny_button = tk.Button(root, text='Apply Canny', command=apply_canny)
canny_button.pack()

count_button = tk.Button(root, text='Count Pixels', command=count_pixels)
count_button.pack()

allocate_button = tk.Button(root, text='Allocate Time', command=allocate_time)
allocate_button.pack()

# Label to display the count of white pixels
pixel_count_label = tk.Label(root, text='White Pixels: ')
pixel_count_label.pack()

# Label to display the signal allocation time
allocation_label = tk.Label(root, text='Signal Allocation Time: ')
allocation_label.pack()

# Run the application
root.mainloop()