
import yfinance as yf
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
import subprocess

# Download S&P 500 stock list
sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
tickers = sorted(sp500['Symbol'].tolist())  # Sorted for better UX

# Define UI Colors
PRIMARY_COLOR = "gold"
SECONDARY_COLOR = "black"
TEXT_COLOR = "white"

# Define Fonts
FONT_FAMILY = "Helvetica"

# Function to fetch and display stock data
def search_stock():
    selected_stock = stock_entry.get().upper()
    from_date = pd.to_datetime(from_date_entry.get()).strftime('%Y-%m-%d')
    to_date = pd.to_datetime(to_date_entry.get()).strftime('%Y-%m-%d')

    if selected_stock not in tickers:
        result_label.config(text="Error: Please select a valid stock!", fg="red")
        return

    try:
        # Fetch stock data
        stock_data = yf.download(selected_stock, start=from_date, end=to_date)

        if stock_data.empty:
            result_label.config(text="No data found for the selected range.", fg="red")
            return

        # Reset index and format Date
        stock_data.reset_index(inplace=True)
        stock_data['Date'] = stock_data['Date'].dt.strftime('%Y-%m-%d')

        # Select only relevant columns
        stock_data = stock_data[['Date', 'Open', 'Close', 'High', 'Low', 'Volume']]

        # Clear previous data in the Treeview
        for row in stock_table.get_children():
            stock_table.delete(row)

        # Insert new data into the table
        for _, row in stock_data.iterrows():
            stock_table.insert("", "end", values=tuple(row))

        # Update result label
        result_label.config(text=f"Showing data for {selected_stock}", fg="green")

    except Exception as e:
        result_label.config(text=f"Error fetching data: {e}", fg="red")

# Function to filter stock suggestions
def update_suggestions(event):
    typed_text = stock_entry.get().upper()
    filtered_tickers = [t for t in tickers if t.startswith(typed_text)]
    stock_listbox.delete(0, tk.END)
    for item in filtered_tickers:
        stock_listbox.insert(tk.END, item)

# Function to select stock from the listbox
def select_stock(event):
    selected = stock_listbox.get(tk.ACTIVE)
    stock_entry.delete(0, tk.END)
    stock_entry.insert(0, selected)
    stock_listbox.pack_forget()

# Function to display selected menu option
def display_option(option):
    for widget in content.winfo_children():
        widget.destroy()

    frame = tk.Frame(content, bg=SECONDARY_COLOR, relief="raised", bd=2)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(frame, text=option, font=(FONT_FAMILY, 24, 'italic'), bg=SECONDARY_COLOR, fg=PRIMARY_COLOR).pack(pady=10)


    
    if option == "Stocks Data":
        tk.Label(frame, text="Enter Stock Symbol:", font=(FONT_FAMILY, 12), bg=SECONDARY_COLOR, fg=PRIMARY_COLOR).pack(pady=5)

        global stock_entry, stock_listbox
        stock_entry = tk.Entry(frame, font=(FONT_FAMILY, 12), width=30)
        stock_entry.pack(pady=5)
        stock_entry.bind("<KeyRelease>", update_suggestions)

        stock_listbox = tk.Listbox(frame, font=(FONT_FAMILY, 12), width=30, height=5)
        stock_listbox.pack(pady=5)
        stock_listbox.bind("<ButtonRelease-1>", select_stock)

        # Date pickers
        tk.Label(frame, text="From:", font=(FONT_FAMILY, 12), bg=SECONDARY_COLOR, fg=PRIMARY_COLOR).pack(pady=5)
        global from_date_entry
        from_date_entry = DateEntry(frame, font=(FONT_FAMILY, 12), width=12, background=PRIMARY_COLOR, foreground='black', borderwidth=2)
        from_date_entry.pack(pady=5)

        tk.Label(frame, text="To:", font=(FONT_FAMILY, 12), bg=SECONDARY_COLOR, fg=PRIMARY_COLOR).pack(pady=5)
        global to_date_entry
        to_date_entry = DateEntry(frame, font=(FONT_FAMILY, 12), width=12, background=PRIMARY_COLOR, foreground='black', borderwidth=2)
        to_date_entry.pack(pady=5)

        global result_label
        result_label = tk.Label(frame, text="", font=(FONT_FAMILY, 12), bg=SECONDARY_COLOR, fg=PRIMARY_COLOR)
        result_label.pack(pady=5)

        tk.Button(frame, text="Search", font=(FONT_FAMILY, 12), bg=PRIMARY_COLOR, fg='black', bd=2, padx=10, pady=5, relief="flat", command=search_stock).pack(pady=10)

        # Table to display stock data
        global stock_table
        columns = ("Date", "Open", "Close", "High", "Low", "Volume")
        stock_table = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            stock_table.heading(col, text=col)
            stock_table.column(col, width=120, anchor="center")

        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(frame, orient="vertical", command=stock_table.yview)
        tree_scroll_x = ttk.Scrollbar(frame, orient="horizontal", command=stock_table.xview)
        stock_table.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x.pack(side="bottom", fill="x")
        stock_table.pack(fill="both", expand=True, padx=20, pady=10)


    if option == "Visuals":
        subprocess.Popen(['python', 'visual.py'])  # Open the visual.py script
        root.quit()  # Close the login window after successful login
        root.destroy()

    if option == "Forecast":
        subprocess.Popen(['python', 'forecast.py'])  # Open the forecast.py script
        root.quit()  # Close the login window after successful login
        root.destroy()

    if option == "Market Cap & Yearly Sector Growth":
        subprocess.Popen(['python', 'marketcap.py'])  # Open the Marketcap.py script
        root.quit()  # Close the login window after successful login
        root.destroy()
        
    if option == "Logout":
        subprocess.Popen(['python', 'LoginPage.py'])  # Open the LoginPage.py script
        root.quit()  # Close the login window after successful login
        root.destroy()

    if option == "Buy/Sell":
        subprocess.Popen(['python', 'BuySell.py'])  # Open the BuySell.py script
        root.quit()  # Close the login window after successful login
        root.destroy()


# Create main window
root = tk.Tk()
root.title("Stock Market Dashboard")
root.geometry("1200x700")
root.iconbitmap(r'C:\Users\user\OneDrive\Desktop\Stock Market Prediction Model\Icons\business.ico')
root.state('zoomed')

# Sidebar frame
sidebar = tk.Frame(root, bg=SECONDARY_COLOR, width=250, relief="raised", bd=3)
sidebar.pack(side="left", fill="y")

# Sidebar header
header = tk.Label(sidebar, text="Stock Dashboard", font=(FONT_FAMILY, 24, 'bold', 'italic'), bg=SECONDARY_COLOR, fg=PRIMARY_COLOR, pady=20)
header.pack(fill="x")

# Main content frame
content = tk.Frame(root, bg=PRIMARY_COLOR)
content.pack(side="right", fill="both", expand=True)

# Sidebar buttons
buttons = [
    ("Stocks Data", PRIMARY_COLOR),
    ("Market Cap & Yearly Sector Growth", PRIMARY_COLOR),
    ("Visuals", PRIMARY_COLOR),
    ("Forecast", PRIMARY_COLOR),
    ("Buy/Sell", PRIMARY_COLOR),
    ("Logout", PRIMARY_COLOR)
]

for text, color in buttons:
    btn = tk.Button(sidebar, text=text, command=lambda t=text: display_option(t), bg=color, fg='black', font=(FONT_FAMILY, 14, 'bold', 'italic'), relief="flat", bd=2, padx=10, pady=10, borderwidth=2)
    btn.pack(fill="x", pady=15, padx=20)

# Initial message
display_option("Stocks Data")

# Run the application
root.mainloop()


