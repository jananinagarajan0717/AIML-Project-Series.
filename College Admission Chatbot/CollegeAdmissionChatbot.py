import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
import json

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class CollegeAdmissionChatbot:
    def __init__(self):
        self.load_responses()
        self.context = {}
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.response_templates = {
            "admission procedure": "I see you're interested in the admission procedure. As mentioned, it involves filling out the application form, submitting required documents, and attending an interview if shortlisted.",
            "requirements": "Regarding the requirements, remember that a high school diploma, standardized test scores, and recommendation letters are essential.",
            "deadlines": "About the deadlines, please note that the application deadlines are as follows: Fall - July 31, Spring - December 15, Summer - April 30.",
            "unknown": "Can you please clarify your question?"
        }

    def load_responses(self):
        with open('Responses.json', 'r') as file:
            self.responses = json.load(file)
    
    def preprocess(self, sentence):
        tokens = word_tokenize(sentence)
        tokens = [self.lemmatizer.lemmatize(word.lower()) for word in tokens if word.isalpha() and word.lower() not in self.stop_words]
        return tokens
    
    def get_response(self, query):
        tokens = self.preprocess(query)
        
        # Basic keyword matching for simplicity
        if any(token in tokens for token in ["hi", "hello", "hey"]):
            return np.random.choice(self.responses["greetings"])
        elif any(token in tokens for token in ["procedure", "process"]):
            return self.responses["admission_procedure"][0]
        elif any(token in tokens for token in ["requirement", "criteria"]):
            return self.responses["requirements"][0]
        elif any(token in tokens for token in ["deadline", "last date"]):
            return self.responses["deadlines"][0]
        else:
            return self.responses["default"][0]

    def update_context(self, user_input):
        if "admission procedure" in user_input:
            self.context['last_query'] = "admission procedure"
        elif "requirements" in user_input:
            self.context['last_query'] = "requirements"
        elif "deadlines" in user_input:
            self.context['last_query'] = "deadlines"
        else:
            self.context['last_query'] = "unknown"

    def provide_personalized_response(self):
        last_query = self.context.get('last_query', 'unknown')
        return self.response_templates.get(last_query, "Can you please clarify your question?")

    def fetch_real_time_info(self, query):
        # Simulate fetching real-time data
        if "real-time" in query:
            return "This is simulated real-time data about college admissions."
        return None

class CollegeAdmissionChatbotGUI:
    def __init__(self, master):
        self.master = master
        master.title("College Admission Chatbot")
        master.state("zoomed")  # Maximize window

        # Define colors for dark theme
        self.background_color = "#000000"  # Dark background color
        self.text_color = "#71C671"         # Chat text color
        self.input_background_color = "#4b5263"  # Dark background color for input box
        self.input_text_color = "#CCCCCC"   # Light text color for input box
        self.button_color = "#4b5263"       # Dark button color
        self.button_text_color = "#CCCCCC"  # Light text color for buttons

        # Load and resize background image
        self.original_bg_image = Image.open("background_image.png")  # Replace with your background image path
        self.bg_image = ImageTk.PhotoImage(self.original_bg_image)
        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(fill="both", expand=True)

        self.master.bind("<Configure>", self.resize_bg_image)

        self.create_gui()
        self.chatbot = CollegeAdmissionChatbot()

    def create_gui(self):
        self.master.config(bg=self.background_color)

        self.chat_display = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=80, height=20, bg=self.background_color, fg=self.text_color, font=("Cascadia Code", 14))
        self.chat_display.config(state=tk.DISABLED)

        self.entry_frame = tk.Frame(self.master, bg=self.background_color)
        self.user_input = tk.Entry(self.entry_frame, width=80, bg=self.input_background_color, fg=self.input_text_color)
        self.user_input.pack(side=tk.LEFT, padx=10)
        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message, bg=self.button_color, fg=self.button_text_color)
        self.send_button.pack(side=tk.RIGHT)

        self.master.bind('<Return>', self.send_message)
        
        # Center the chat display and input frame
        self.update_layout()

    def resize_bg_image(self, event):
        # Resize background image to fit window size
        self.bg_image_resized = self.original_bg_image.resize((event.width, event.height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image_resized)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        self.update_layout()

    def send_message(self, event=None):
        message = self.user_input.get().lower()  # Convert input to lowercase for case insensitivity
        if message in ['exit', 'quit', 'bye', 'thank you']:
            self.display_message("College Admission Chatbot: Goodbye!\n")
            self.user_input.delete(0, tk.END)
            return
        self.chatbot.update_context(message)
        real_time_response = self.chatbot.fetch_real_time_info(message)
        if real_time_response:
            response = real_time_response
        else:
            response = self.chatbot.get_response(message)
            if response == self.chatbot.responses["default"][0]:  # If default response, try personalized response
                response = self.chatbot.provide_personalized_response()
        self.display_message(f"You: {message}\n")
        self.display_message(f"College Admission Chatbot: {response}\n")
        self.user_input.delete(0, tk.END)

    def display_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def update_layout(self):
        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()

        # Position the chat display
        chat_display_width = self.chat_display.winfo_reqwidth()
        chat_display_height = self.chat_display.winfo_reqheight()
        chat_display_x = (window_width - chat_display_width) // 2
        chat_display_y = (window_height - chat_display_height) // 2 - 50
        self.canvas.create_window(chat_display_x, chat_display_y, window=self.chat_display, anchor="nw")

        # Position the entry frame
        entry_frame_width = self.entry_frame.winfo_reqwidth()
        entry_frame_height = self.entry_frame.winfo_reqheight()
        entry_frame_x = (window_width - entry_frame_width) // 2
        entry_frame_y = chat_display_y + chat_display_height + 20
        self.canvas.create_window(entry_frame_x, entry_frame_y, window=self.entry_frame, anchor="nw")

if __name__ == "__main__":
    root = tk.Tk()
    app = CollegeAdmissionChatbotGUI(root)
    root.mainloop()
