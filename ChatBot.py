import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import nltk
from nltk.chat.util import Chat, reflections

# Download the NLTK data required
nltk.download('punkt')

# Define pairs for the chatbot responses
basic_pairs = [
    (r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']),
    (r'how are you?', ['I am fine, thank you. How can I help you today?', 'Doing well, thank you!']),
    (r'what is your name?', ['You can call me Pluto.']),
    (r'tell me about yourself', ['I am a simple chatbot reated to assist you.']),
    (r'bye|goodbye', ['Goodbye! Have a great day.', 'It was nice talking to you! Have a great day.']),
]

# Create a chatbot for basic interactions
basic_chatbot = Chat(basic_pairs, reflections)

class ChatBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pluto - Chatbot")

        # Maximize window
        self.root.state('zoomed')

        # Define colors for dark theme
        self.background_color = "#282c34"  # Dark background color
        self.text_color = "#ffffff"         # White text color
        self.input_background_color = "#3e4451"  # Dark background color for input box
        self.input_text_color = "#d0d0d0"   # Light text color for input box
        self.button_color = "#4b5263"       # Dark button color
        self.button_text_color = "#ffffff"  # Light text color for buttons

        # Load and resize background image
        self.original_bg_image = Image.open("background.jpg")  # Replace with your background image path
        self.bg_image = ImageTk.PhotoImage(self.original_bg_image)
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)

        self.root.bind("<Configure>", self.resize_bg_image)

        self.create_gui()

        # Variables to track context
        self.context = {}

        # Questions to ask user
        self.questions = [
            "What's your name?",
            "How old are you?",
            "What's your favorite color?"
        ]
        self.current_question_index = 0

        # Start with a greeting
        self.display_message("Pluto", "Hello! How can I assist you today?")

    def create_gui(self):
        self.root.config(bg=self.background_color)

        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=20, bg=self.background_color, fg=self.text_color, font=("Cascadia Code", 14))
        self.chat_display.config(state=tk.DISABLED)

        self.entry_frame = tk.Frame(self.root, bg=self.background_color)
        self.user_input = tk.Entry(self.entry_frame, width=80, bg=self.input_background_color, fg=self.input_text_color)
        self.user_input.pack(side=tk.LEFT, padx=10)
        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message, bg=self.button_color, fg=self.button_text_color)
        self.send_button.pack(side=tk.RIGHT)

        self.root.bind('<Return>', self.send_message)
        
        # Center the chat display and input frame
        self.update_layout()

    def resize_bg_image(self, event):
        # Resize background image to fit window size
        self.bg_image_resized = self.original_bg_image.resize((event.width, event.height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image_resized)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        self.update_layout()

    def update_layout(self):
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

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

    def send_message(self, event=None):
        user_message = self.user_input.get().strip()
        self.user_input.delete(0, tk.END)

        if user_message:
            self.display_message("You", user_message)
            self.handle_user_response(user_message)

    def handle_user_response(self, user_message):
        # Handle initial basic interactions
        bot_response = basic_chatbot.respond(user_message)
        
        # If the bot response is not from the basic interactions, proceed with user-specific questions
        if bot_response not in [response for _, responses in basic_pairs for response in responses]:
            if self.current_question_index < len(self.questions):
                self.context[self.questions[self.current_question_index]] = user_message
                self.current_question_index += 1
                self.ask_question()
            else:
                self.respond_using_context(user_message)
        else:
            self.display_message("Pluto", bot_response)

    def ask_question(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.display_message("Pluto", question)
        else:
            self.display_message("Pluto", "Thank you for answering my questions!")

    def respond_using_context(self, user_message):
        if "What's your name?" in self.context:
            bot_response = f"{self.context['What\'s your name?']}! You said your favorite color is {self.context['What\'s your favorite color?']}, right?"
        else:
            bot_response = "Thank you for the information"        
        self.display_message("Pluto", bot_response)

    def display_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()
