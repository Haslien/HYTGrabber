import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from yt_dlp import YoutubeDL
from pytube import YouTube
from PIL import Image, ImageTk
import json

SETTINGS_FILE = 'userdata.json'

def save_settings(save_path, filetype):
    settings = {
        'save_path': save_path,
        'filetype': filetype
    }
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {'save_path': '', 'filetype': ''}

def download_video(url, output_folder, output_format):
    if output_format in ['mp3', 'wav']:
        ydl_opts = {
            'format': f'bestaudio/best',
            'outtmpl': os.path.join(output_folder, f'%(title)s'),
            'ffmpeg_location': 'ffmpeg/'
        }
        if output_format == 'mp3':
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        elif output_format == 'wav':
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }]

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    elif output_format == 'mp4':
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        try:
            stream.download(output_path=output_folder)
            messagebox.showinfo("Download Complete", "The video has been successfully downloaded.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during download:\n{str(e)}")

def download():
    url = url_entry.get()
    format_choice = format_var.get()
    save_folder = folder_entry.get()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    if not format_choice:
        messagebox.showerror("Error", "Please select a format.")
        return

    if not save_folder:
        messagebox.showerror("Error", "Please select a save folder.")
        return

    try:
        download_video(url, save_folder, format_choice)
        messagebox.showinfo("Success", f"The video has been successfully downloaded as {format_choice}.")
        save_settings(save_folder, format_choice)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during download:\n{str(e)}")

def browse_folder():
    folder_path = filedialog.askdirectory(initialdir='/path/to/default/folder')
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)
        save_settings(folder_path, format_var.get())

def open_website():
    import webbrowser
    webbrowser.open("http://www.mathias-haslien.no")

def init_ui():
    settings = load_settings()
    folder_entry.insert(0, settings['save_path'])
    format_var.set(settings['filetype'])

root = tk.Tk()
root.title("Hassy's YTGrabber")
root.geometry("600x400")
# Disable window resizing
root.resizable(False, False)

# Load the image file
image = Image.open("img/background.png")
background_image = ImageTk.PhotoImage(image)

#load icon
ico = Image.open('img/icon.png')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)

# Create a Label widget with the background image
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

custom_font = ('Arial', 14, 'bold')  # Font family, size, and style

# Add other widgets on top of the background
url_label = ttk.Label(root, text="YouTube URL:", font=custom_font)
url_label.place(relx=0.5, rely=0.35, anchor="center")
url_entry = ttk.Entry(root, width=50)
url_entry.place(relx=0.5, rely=0.40, anchor="center")

format_label = ttk.Label(root, text="Format:", font=custom_font)
format_label.place(relx=0.5, rely=0.47, anchor="center")
format_var = tk.StringVar()
mp3_radio = ttk.Radiobutton(root, text='MP3', variable=format_var, value='mp3')
mp3_radio.place(relx=0.4, rely=0.52, anchor="center")
wav_radio = ttk.Radiobutton(root, text='WAV', variable=format_var, value='wav')
wav_radio.place(relx=0.5, rely=0.52, anchor="center")
mp4_radio = ttk.Radiobutton(root, text='MP4', variable=format_var, value='mp4')
mp4_radio.place(relx=0.6, rely=0.52, anchor="center")

folder_label = ttk.Label(root, text="Save Folder:", font=custom_font)
folder_label.place(relx=0.5, rely=0.6, anchor="center")
folder_entry = ttk.Entry(root, width=50)
folder_entry.place(relx=0.5, rely=0.68, anchor="center")

browse_button = ttk.Button(root, text="Browse", command=browse_folder)
browse_button.place(relx=0.5, rely=0.76, anchor="center")

download_button = ttk.Button(root, text="Download", command=download)
download_button.pack(pady=20)
download_button.config(padding=(20, 10))  # Adjust the padding as needed
download_button.place(relx=0.5, rely=0.9, anchor="center")

# Create a button with the text www.mathias-haslien.no in red and bold font
button = tk.Button(root, text="www.mathias-haslien.no", font=('Arial', 12), fg='red', bd=0, command=open_website)

# Position the button at the bottom right corner
button.place(relx=1.0, rely=1.0, anchor='se')

# Initialize UI with loaded settings
init_ui()

root.mainloop()
