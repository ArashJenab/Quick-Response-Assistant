import tkinter as tk
from tkinter import ttk
import openai

class Var:
    codeVer     = "v1.8" # Define the code version as a string
    app_width   = 450 #Default window width
    
var = Var()
    

# Function to handle API request and generate the response
def generate_response():
    style = style_var.get()
    comformat = comformat_var.get()
    respformat = respformat_var.get()
    original_message = original_message_input.get("1.0", tk.END).strip()
    what_to_respond = response_input.get("1.0", tk.END).strip()

    if original_message:
        prompt = (
            f"You are tasked with responding to a communication in the style of '{style}' "
            f"with a tone '{respformat}' and in the format of '{comformat}'. "
            f"Here's what you need to say: '{what_to_respond}'. "
            f"Original message: '{original_message}'."
        )
    else:
        prompt = (
            f"You are tasked with drafting a new communication in the style of '{style}' "
            f"with a tone '{respformat}' and in the format of '{comformat}'. "
            f"Here's what you need to say: '{what_to_respond}'."
        )

    api_key_path = "openai_api_key.txt"
    try:
        with open(api_key_path, "r") as file:
            openai.api_key = file.read().strip()
        if not openai.api_key:  # File is empty
            raise ValueError("API key file is empty.")
    except FileNotFoundError:
        response_output_text.delete("1.0", tk.END)
        response_output_text.insert(
            tk.END,
            "To use this tool, you'll need your own OpenAI API key saved as a plain text file "
            "named openai_api_key.txt in the same directory. The file should contain only the API key—"
            "no quotes or assignments (\"\" or =), just the key itself."
        )
        return
    except ValueError:
        response_output_text.delete("1.0", tk.END)
        response_output_text.insert(
            tk.END,
            "Your openai_api_key.txt file is empty. Please add your OpenAI API key to the file."
        )
        return

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            top_p=1
        )
        result = response.choices[0].message.content
        response_output_text.delete("1.0", tk.END)
        response_output_text.insert(tk.END, result)
    except Exception as e:
        response_output_text.delete("1.0", tk.END)
        response_output_text.insert(tk.END, f"Error: {str(e)}")

def clear_fields():
    original_message_input.delete("1.0", tk.END)  # Clear original message
    response_input.delete("1.0", tk.END)  # Clear response input
    response_output_text.delete("1.0", tk.END)  # Clear ChatGPT output

def copy_to_clipboard():
    # Get the content from the response_output_text widget
    text = response_output_text.get("1.0", tk.END).strip()
    # Copy the content to the clipboard
    app.clipboard_clear()
    app.clipboard_append(text)
    app.update()  # Ensure the clipboard content is updated

# Function to allow tab between fields
def bind_tab_key(widget):
    widget.bind("<Tab>", focus_next_widget)

# Function to focus on the next widget
def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"  # Prevent default Tab behavior in Text widget

# Set up the main application window
app = tk.Tk()
app.title("Quick Response Assistant")

# Handle missing AT.png using try-except
try:
    icon = tk.PhotoImage(file="AT.png")
    app.iconphoto(False, icon)
except tk.TclError:
    pass  # If the file is not found, just continue without an icon

# Get screen width and height
screen_width    = app.winfo_screenwidth()
screen_height   = app.winfo_screenheight()

# Get default app size
window_width    = var.app_width  # Example: 450
window_height   = int(round(screen_height * 0.98, 0))

x_offset        = 25
y_offset        = 0
app.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")
app.geometry(f"{window_width}x{window_height}")
app.minsize(450, 900)   # Set minimum size (width x height)


# Dropdown for Styles
respformat_var = tk.StringVar(value="Replicate Sender")
# Style options sorted alphabetically for easier selection
respformat_options = [
    "Action-Oriented", 
    "Business", 
    "Friendly", 
    "Legal", 
    "Persuasive", 
    "Professional", 
    "Technical",
    "Replicate Sender"
]
# Mapping of user-selected styles to AI-friendly descriptions
respformat_mapping = {
    "Professional": "Maintain a formal, concise and respectful tone with clear language suitable for business or managerial communication.",
    "Friendly": "Use a warm and approachable tone, with relaxed language to create rapport.",
    "Diplomatic": "Provide a tactful and neutral response, avoiding direct confrontation while addressing sensitive topics.",
    "Persuasive": "Craft the response to convince the reader, using logical arguments and motivational language.",
    "Action-Oriented": "Direct and focused on motivating immediate action or next steps.",
    "Legal": "Maintain a highly formal, precise tone with legal terminology and references to policies or regulations.",
    "Business": "Balanced professional tone, focused on clear communication of business objectives and outcomes.",
    "Technical": "Use precise, subject-specific language, focusing on accuracy and clarity for technical or specialized topics.",
    "Replicate Sender": "Replicate the style and tone of the received message."
}
respformat_label = tk.Label(app, text="Response Tone:")
respformat_dropdown = ttk.Combobox(app, textvariable=respformat_var, values=respformat_options)


# Dropdown for Styles (Communication Style)
style_var = tk.StringVar(value="Replicate Sender")
# Communication style options
style_options = [
    "Concise", 
    "Conversational", 
    "Informative",
    "Diplomatic", 
    "Engaging", 
    "Managerial", 
    "Strategic",
    "Replicate Sender"
]
# Mapping of user-selected communication style to AI-friendly descriptions
style_mapping = {
    "Concise": "Keep the message short and to the point, focusing on essential information.",
    "Conversational": "Maintain a natural tone, mimicking the flow of informal conversation.",
    "Informative": "Provide detailed and factual information, aiming to educate or inform the reader.",
    "Diplomatic": "Handle the communication tactfully, maintaining neutrality and avoiding direct confrontation.",
    "Engaging": "Use a lively and interactive tone to capture and maintain the reader's interest.",
    "Managerial": "Present information clearly and confidently, suitable for decision-making or leadership contexts.",
    "Strategic": "Use a high-level, long-term perspective focusing on goals, planning, and outcomes.",
    "Replicate Sender": "Replicate the style and tone of the received message."
}
style_label     = tk.Label(app, text="Communication Style:")
style_dropdown  = ttk.Combobox(app, textvariable=style_var, values=style_options)




# Dropdown for Communication format
comformat_var   = tk.StringVar(value="Email")
comformat_options = [
    "Email",
    "Text or Messages",
    "Social Media Posts"
    ]
comformat_label     = tk.Label(app, text="Communication Format:")
comformat_dropdown  = ttk.Combobox(app, textvariable=comformat_var, values=comformat_options)





# Textbox for Original Received Message
original_message_label = tk.Label(app, text="Original Received Message:")
### Frame for original message input with scrollbar
original_message_frame = tk.Frame(app)
original_message_input = tk.Text(original_message_frame, wrap=tk.WORD, height=10, width=50)
original_message_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
original_message_scrollbar = tk.Scrollbar(original_message_frame, orient=tk.VERTICAL, command=original_message_input.yview)
original_message_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
original_message_input.config(yscrollcommand=original_message_scrollbar.set)


# Bind Tab to move focus to next widget
bind_tab_key(original_message_input)

# Textbox for What to Respond
response_label = tk.Label(app, text="What to Respond:")
response_input = tk.Text(app, wrap=tk.WORD, height=10, width=50)  # Set height and width

### Frame for response input with scrollbar
response_frame = tk.Frame(app)
response_input = tk.Text(response_frame, wrap=tk.WORD, height=10, width=50)
response_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
response_scrollbar = tk.Scrollbar(response_frame, orient=tk.VERTICAL, command=response_input.yview)
response_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
response_input.config(yscrollcommand=response_scrollbar.set)


# Bind Tab to move focus to next widget
bind_tab_key(response_input)

# Clear button
clear_button = tk.Button(app, text="Clear Fields", command=clear_fields)


# Submit button
submit_button = tk.Button(app, text="Generate Response", command=generate_response)


# Textbox for displaying OpenAI response
response_output_text = tk.Text(app, wrap=tk.WORD, height=10, width=50)  # Set height and width

### Frame for response output with scrollbar
response_output_frame = tk.Frame(app)

response_output_text = tk.Text(response_output_frame, wrap=tk.WORD, height=10, width=50)
response_output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
response_output_scrollbar = tk.Scrollbar(response_output_frame, orient=tk.VERTICAL, command=response_output_text.yview)
response_output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
response_output_text.config(yscrollcommand=response_output_scrollbar.set)


# Add text label at the bottom left
version_label_left = tk.Label(app, text="arash@ahura-tech.com  :)", font=("Arial", 8))


# Copy to Clipboard button
copy_button = tk.Button(app, text="Copy", command=copy_to_clipboard)

# Add version label at the bottom right
version_label_right = tk.Label(app, text=f"{var.codeVer}", font=("Arial", 8))



# ********* Grid Areas *************
# Configure grid rows and columns to be resizable
app.grid_rowconfigure(0, weight=0)  # Fixed row for dropdowns
app.grid_rowconfigure(1, weight=0)  # Fixed row for dropdowns
app.grid_rowconfigure(2, weight=0)  # Fixed row for labels
app.grid_rowconfigure(3, weight=0)  # Resizable row for text windows
app.grid_rowconfigure(4, weight=1)  # Fixed row for labels
app.grid_rowconfigure(5, weight=0)  # Resizable row for text windows
app.grid_rowconfigure(6, weight=1)  # Fixed row for buttons
app.grid_rowconfigure(7, weight=0)  # Space between buttons and output
app.grid_rowconfigure(8, weight=3)  # Resizable row for output text
app.grid_rowconfigure(9, weight=0)  # Fixed row for version info
app.grid_columnconfigure(0, weight=0)  # Left column does not expand
app.grid_columnconfigure(1, weight=1)  # Middle column expands to fit button
app.grid_columnconfigure(2, weight=1)  # Right column does not expand

buttonWidth = 20
clear_button.config(width=buttonWidth)  # Adjust width as needed
copy_button.config(width=buttonWidth)  # Adjust width as needed
submit_button.config(width=buttonWidth)  # Adjust width as needed



comformat_label.grid(row=0, column=0, padx=10, pady=2, sticky='w')  # Align left
comformat_dropdown.grid(row=0, column=1, columnspan=2, padx=10, pady=2, sticky='ew')
style_label.grid(row=1, column=0, padx=10, pady=2, sticky='w')  # Align left
style_dropdown.grid(row=1, column=1, columnspan=2, padx=10, pady=2, sticky='ew')
respformat_label.grid(row=2, column=0, padx=10, pady=2, sticky='w')  # Align left
respformat_dropdown.grid(row=2, column=1, columnspan=2, padx=10, pady=2, sticky='ew')


original_message_label.grid(row=3, column=0, padx=10, pady=2, sticky='w')  # Align left
original_message_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=2, sticky='nsew')

response_label.grid(row=5, column=0, padx=10, pady=2, sticky='w')  # Align left
response_frame.grid(row=6, column=0, columnspan=3, padx=10, pady=2, sticky='nsew')


clear_button.grid(row=7, column=0, padx=10, pady=5, sticky="ew")  # Align left
copy_button.grid(row=7, column=1, padx=10, pady=5, sticky='ew')  # Center in the middle column
submit_button.grid(row=7, column=2, padx=10, pady=5, sticky="ew")  # Align right

response_output_frame.grid(row=8, column=0, columnspan=3, padx=10, pady=2, sticky='nsew')


version_label_left.grid(row=9, column=0, padx=5, pady=1, sticky='w')  # Align left
version_label_right.grid(row=9, column=2, padx=5, pady=1, sticky='e')  # Align right



    

# Bind Tab to move focus to next widget
bind_tab_key(response_output_text)

# Run the application
app.mainloop()


