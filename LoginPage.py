from tkinter import *
from tkinter import messagebox
import subprocess

# Define constants for colors, fonts, and sizes
BACKGROUND_COLOR = "#121212"  # Black background for the window
TEXT_COLOR = "#FFD700"  # Golden text color
BUTTON_COLOR = "#FFD700"  # Button color
BUTTON_TEXT_COLOR = "#121212"  # Text color for the button
FONT_FAMILY = "Helvetica"  # Font family for text
TITLE_FONT_SIZE = 55
LABEL_FONT_SIZE = 18
ENTRY_FONT_SIZE = 16
BUTTON_FONT_SIZE = 12
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 0

# Create the main window
window = Tk(screenName='Login Page')  # Set the size of the window
window.state('zoomed')  # Make the window full-screen
window.title('Login Page')  # Set the title of the window
window.iconbitmap(r'C:\Users\user\OneDrive\Desktop\Stock Market Prediction Model\Icons\login.ico')  # Set the icon of the window
window.configure(bg=BACKGROUND_COLOR)  # Set the background color of the window
frame = Frame(bg=BACKGROUND_COLOR)  # Create a frame to hold the widgets

# Backend function to check login credentials
def login():
    # Hardcoded credentials
    username = 'smp'
    password = 'smp'
    
    # Check if username or password fields are empty
    if username_entry.get() == "" or password_entry.get() == "":
        messagebox.showerror(title='Error', message='Username or password cannot be empty')  # Show error if fields are empty
        return

    # Check if entered credentials match the hardcoded ones
    if username_entry.get() == username and password_entry.get() == password:
       messagebox.showinfo(title='Login success', message='Logged in successfully')  # Show success message
       run_main_dashboard()  # Call the function to run the main dashboard after successful login
    else:
        messagebox.showerror(title='Error', message='Incorrect username or password')  # Show error if credentials are wrong

# Function to open the main dashboard and close the login window
def run_main_dashboard():
    subprocess.Popen(['python', 'MainDashboard.py'])  # Open the MainDashboard.py script
    window.quit()  # Close the login window after successful login
    window.destroy()  # Ensure window is fully destroyed

# Create the widgets for the login page
login_label = Label(frame, text='Welcome to Secure Access Portal', bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, TITLE_FONT_SIZE, 'bold italic'))
username_label = Label(frame, text='UserName', bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, LABEL_FONT_SIZE, 'bold italic'))
password_label = Label(frame, text='PassWord', bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, LABEL_FONT_SIZE, 'bold italic'))
username_entry = Entry(frame, font=(FONT_FAMILY, ENTRY_FONT_SIZE, 'italic'), borderwidth=5)  # Entry widget for username
password_entry = Entry(frame, show='*', font=(FONT_FAMILY, ENTRY_FONT_SIZE, 'italic'), borderwidth=5)  # Entry widget for password (show '*' for password)

# Load images for the buttons and labels
button_photo = PhotoImage(file=r'C:\Users\user\OneDrive\Desktop\Stock Market Prediction Model\Images\arrow.png')  # Load image for the login button
login_button = Button(frame, text="Login >", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=(FONT_FAMILY, BUTTON_FONT_SIZE, 'bold italic'), command=login, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, image=button_photo, borderwidth=10, highlightbackground=BUTTON_COLOR, highlightthickness=3)  # Create the login button
user_photo = PhotoImage(file=r'C:\Users\user\OneDrive\Desktop\Stock Market Prediction Model\Images\001-profile-removebg-preview.png')  # Load user icon image
pass_photo = PhotoImage(file=r'C:\Users\user\OneDrive\Desktop\Stock Market Prediction Model\Images\001-padlock-removebg-preview.png')  # Load padlock icon image
userlabel_photo = Label(frame, image=user_photo, width=40, height=40, bg=BACKGROUND_COLOR)  # Label for the user icon
passlabel_photo = Label(frame, image=pass_photo, width=40, height=40, bg=BACKGROUND_COLOR)  # Label for the padlock icon

# Place widgets inside the frame using grid layout
login_label.grid(row=0, column=0, columnspan=3, sticky="news", pady=40)  # Title label at the top
userlabel_photo.grid(row=1, column=0)  # Place user icon
username_label.grid(row=1, column=1, pady=20)  # Username label
username_entry.grid(row=1, column=2)  # Username entry field
passlabel_photo.grid(row=2, column=0)  # Place padlock icon
password_label.grid(row=2, column=1, pady=20)  # Password label
password_entry.grid(row=2, column=2)  # Password entry field
login_button.grid(row=3, column=0, columnspan=3, pady=30)  # Login button at the bottom

# Pack the frame to display it on the window
frame.pack()

# Run the application (start the Tkinter event loop)
window.mainloop()




