import speech_recognition as sr
import pyttsx3
import tkinter as tk
import datetime
from tkinter import messagebox
import wikipedia
import webbrowser

engine = pyttsx3.init()

def speak(text):
  """Converts text to speech and speaks it out loud."""
  engine.say(text)
  engine.runAndWait()

def get_audio():
  """Records audio from the microphone, recognizes speech, and returns the text."""
  recognizer = sr.Recognizer()
  with sr.Microphone() as source:
    print("Listening...")
    try:
      audio = recognizer.listen(source, timeout=1.5)  # Reduced timeout for faster response
    except sr.WaitTimeoutError:
      print("Sorry, I timed out. Please speak again.")
      return None
    except sr.UnknownValueError:
      print("Sorry, I didn't understand that. Please rephrase your request.")
      return None

  try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)
    return text.lower()  # Convert to lowercase for case-insensitive commands
  except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return None

def process_command(command):
  """Processes the user's voice command."""
  if command in ("quit", "exit"):
    window.destroy()  # Close the GUI window
  elif "time" in command:
    time = datetime.datetime.now().strftime('%I:%M %p')
    speak(time)
  elif "date" in command:
    today = datetime.date.today()
    date_formatted = today.strftime('%B %d, %Y')  # Format the date
    speak(f"Today's date is {date_formatted}.")
  elif "youtube" in command:
    video = command.split("play ")[-1] if "play" in command else command.split("youtube ")[-1]
    speak('Opening Youtube')
    webbrowser.open('www.youtube.com')  # Search Youtube for the video
  elif "open website" in command:
    website = command.split("open website ")[-1]
    speak('Opening website')
    webbrowser.open('https://www.wikipedia.org/')  # Open the website directly (assumes valid URL)
  elif "wikipedia" in command:
    person_name = command.split("wikipedia ")[-1]
    summary = wikipedia.summary(person_name, sentences=2)
    speak(summary)
  else:
    speak("I'm still under development, but I can't perform that action yet.")

def button_click():
  """Callback function for the GUI button."""
  command = get_audio()
  if command:
    process_command(command)

# Create the GUI window
engine = pyttsx3.init() 
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 
window = tk.Tk()
window.title("Voice Assistant")

# Create a button to activate speech recognition
button = tk.Button(window, text="Start Listening", command=button_click)
button.pack()

# Keep the window open and listen for commands
window.mainloop()
