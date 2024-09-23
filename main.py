import pyttsx3
import speech_recognition as sr
import wikipedia
import openai
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import threading

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function for text-to-speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening... (say 'stop' to end)")
        while True:
            try:
                audio = r.listen(source)
                command = r.recognize_google(audio)
                print(f"You said: {command}")
                if "stop" in command.lower():
                    speak("Stopping the assistant.")
                    break
                process_command(command)
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio. Trying again...")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

# Function to get the current date and time
def current_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# Function for mathematical calculations
def calculate(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

# Function to save text to a file
def save_text(text):
    with open("stored_paragraphs.txt", "a") as file:
        file.write(text + "\n\n")
    speak("The information has been saved.")

# Function to read stored paragraphs
def read_stored_texts():
    try:
        with open("stored_paragraphs.txt", "r") as file:
            content = file.read()
        if content:
            speak("Here are the stored paragraphs.")
            print(content)
            speak(content)
        else:
            speak("There are no stored paragraphs.")
    except FileNotFoundError:
        speak("No stored paragraphs found.")

# Function to search Wikipedia
def wikipedia_search(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        speak(summary)
        save_text(summary)  # Save the summary to file
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results. Please be more specific.")
    except Exception as e:
        speak("I couldn't find anything on Wikipedia.")
        print(e)

# Function to interact with OpenAI
def openai_interact(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        full_response = response['choices'][0]['message']['content']
        speak(full_response)
        save_text(full_response)  # Save the OpenAI response
    except Exception as e:
        speak("There was an error communicating with OpenAI.")
        print(e)

# Function to process commands
def process_command(command):
    if 'time' in command:
        time_message = f"The current time is {current_time()}."
        speak(time_message)
        print(time_message)
    elif 'wikipedia' in command:
        search_query = command.replace("wikipedia", "").strip()
        wikipedia_search(search_query)
    elif 'calculate' in command:
        expression = command.replace("calculate", "").strip()
        result = calculate(expression)
        result_message = f"The result is: {result}."
        speak(result_message)
        print(result_message)
    elif 'openai' in command:
        prompt = command.replace("openai", "").strip()
        openai_interact(prompt)
    elif 'read stored' in command:
        read_stored_texts()
    else:
        speak("Sorry, I didn't understand that command.")

# GUI Class
class AIAssistantGUI:
    def __init__(self, master):
        self.master = master
        master.title("AI Assistant")
        master.geometry("400x300")

        self.label = tk.Label(master, text="Welcome to your AI Assistant!")
        self.label.pack(pady=10)

        self.button_exit = tk.Button(master, text="Exit", command=self.master.quit)
        self.button_exit.pack(pady=5)

        # Start the listening thread
        threading.Thread(target=recognize_speech, daemon=True).start()

# Create the GUI
root = tk.Tk()
my_gui = AIAssistantGUI(root)
root.mainloop()
