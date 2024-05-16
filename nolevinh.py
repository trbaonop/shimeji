import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser as wb
import os
import random
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import threading
import sys

# Initialize the text-to-speech engine
friday = pyttsx3.init()
voice = friday.getProperty('voices')
friday.setProperty('voice', voice[0].id)

def speak(audio):
    print("nô lệ vinh said:", audio)
    friday.say(audio)
    friday.runAndWait()

def time():
    Time = datetime.datetime.now().strftime('%I:%M %p')
    speak(Time)

def welcome():
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("good morning master bảo")
    elif 12 <= hour < 17:
        speak("good afternoon master bảo")
    else:
        speak("good night master bảo")
    speak("How can I help you?")

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en')
            print("master Bảo said:", query)
            return query
        except Exception as e:
            print("Say that again please... Master Bảo")
            return ""

def process_command(query):
    if "google" in query:
        speak("What should I search Master?")
        search = command().lower()
        url = f"https://www.google.com.vn/search?q={search}"
        wb.get().open(url)
        speak(f"Here is your {search} on Google")
    elif "youtube" in query:
        speak("What should I search Master?")
        search = command().lower()
        url = f"https://www.youtube.com/search?q={search}"
        wb.get().open(url)
        speak(f"Here is your {search} on YouTube")
    elif "music" in query:
        url = f"https://soundcloud.com/to-n-69830107/v1-nh-c-trung-mix-remix"
        wb.get().open(url)
        speak("Here is your music")
    elif "facebook" in query:
        url = f"https://www.facebook.com/"
        wb.get().open(url)
        speak("Here is your Facebook")
    elif "open video one" in query:
        video1 = r"E:\tap trinh\test\video\video1.mp4"
        os.startfile(video1)
    elif "open video two" in query:
        video2 = r"E:\tap trinh\test\video\video2.mp4"
        os.startfile(video2)
    elif "time" in query:
        time()
    elif "off" in query:
        speak("nô lệ vinh out, goodbye master")
        root.quit()  # Close the Tkinter window
        sys.exit()  # Exit the program immediately
    else:
        speak(f"Performing {query} action")
        shimeji.change_animation(shimeji.get_animation_by_command(query))

class Shimeji:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-topmost', True)  # Always on top
        self.root.overrideredirect(True)  # No border
        self.root.geometry('128x128+100+100')  # Size and position
        self.root.wm_attributes('-transparentcolor', 'white')  # Set transparency color
        
        self.canvas = tk.Canvas(root, width=128, height=128, bg='white', highlightthickness=0)
        self.canvas.pack()
        
        # Load GIFs
        self.idle = self.load_gif('asset/idle.gif')
        self.appear = self.load_gif('asset/appear.gif')
        self.disappear = self.load_gif('asset/disappear.gif')
        self.move_gif = self.load_gif('asset/move.gif')
        
        self.animations = {
            "idle": self.idle,
            "appear": self.appear,
            "disappear": self.disappear,
            "move": self.move_gif
        }
        
        self.images = self.idle  # Start with idle animation
        self.photo_images = [ImageTk.PhotoImage(img) for img in self.images]  # Store PhotoImage objects
        self.image_index = 0
        self.x, self.y = 100, 645  # Initial position
        self.dx, self.dy = 5, 0  # Initial movement direction (only horizontal)
        self.flipped_images = False
        self.update_image()
        self.move()
        
        # Start random action loop
        self.root.after(5000, self.random_action)  # Perform a random action every 5 seconds

    def load_gif(self, filepath):
        gif = Image.open(filepath)
        frames = [frame.convert("RGBA").resize((128, 128), Image.Resampling.LANCZOS) for frame in ImageSequence.Iterator(gif)]
        return frames

    def flip_images(self, frames):
        flipped_frames = [frame.transpose(Image.Transpose.FLIP_LEFT_RIGHT) for frame in frames]
        return flipped_frames

    def update_image(self):
        self.canvas.delete('all')
        self.canvas.create_image(64, 64, image=self.photo_images[self.image_index])
        self.image_index = (self.image_index + 1) % len(self.photo_images)
        self.root.after(100, self.update_image)  # Change image every 100ms

    def move(self):
        self.x += self.dx
        
        screen_width = self.root.winfo_screenwidth()
        
        if self.x < 0 or self.x > screen_width - 128:
            self.dx *= -1  # Change horizontal direction
            self.flipped_images = not self.flipped_images  # Toggle flipped state
            self.update_animation_direction()

        self.root.geometry(f'128x128+{self.x}+{self.y}')
        self.root.after(50, self.move)  # Move every 50ms

    def update_animation_direction(self):
        if self.flipped_images:
            self.images = self.flip_images(self.images)
        else:
            self.images = self.flip_images(self.images)  # Revert to original
        self.photo_images = [ImageTk.PhotoImage(img) for img in self.images]  # Update PhotoImage objects

    def change_animation(self, animation):
        if self.flipped_images:
            self.images = self.flip_images(animation)
        else:
            self.images = animation
        self.photo_images = [ImageTk.PhotoImage(img) for img in self.images]  # Update PhotoImage objects
        self.image_index = 0

    def get_animation_by_command(self, command):
        # Define animations for different commands
        if "move" in command:
            return self.move_gif
        elif "idle" in command:
            return self.idle
        elif "appear" in command:
            return self.appear
        elif "disappear" in command:
            return self.disappear
        else:
            return self.idle  # Default to idle animation

    def random_action(self):
        actions = [self.move_gif, self.idle, self.disappear + self.appear]
        random_action = random.choice(actions)
        self.change_animation(random_action)
        self.root.after(random.randint(3000, 10000), self.random_action)  # Schedule next random action

def start_voice_recognition():
    while True:
        query = command().lower()
        if query:
            process_command(query)

if __name__ == "__main__":
    root = tk.Tk()
    shimeji = Shimeji(root)
    welcome()
    
    # Start the voice recognition in a separate thread to keep GUI responsive
    voice_thread = threading.Thread(target=start_voice_recognition)
    voice_thread.daemon = True
    voice_thread.start()

    root.mainloop()
