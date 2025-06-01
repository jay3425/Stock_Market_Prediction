import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import subprocess

# Download S&P 500 stock list
sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
tickers = sorted(sp500['Symbol'].tolist())  # Sorted for better UX

# Define UI Colors
PRIMARY_COLOR = "gold"
SECONDARY_COLOR = "black"
TEXT_COLOR = "gold"
FONT_FAMILY = "Helvetica"

# Create Tkinter window
root = tk.Tk()
root.state("zoomed")  # Maximized window
root.title("Stock Visuals")
root.iconbitmap(r'C:\Users\user\OneDrive\Desktop\Stock Market Prediction Model\Icons\eye_4106804.ico')
root.configure(bg=SECONDARY_COLOR)  # Background color

# Title Label
label = tk.Label(root, text="Stock Visuals", font=(FONT_FAMILY, 40, "bold"), fg=TEXT_COLOR, bg=SECONDARY_COLOR)
label.pack(pady=20)

# Search bar for selecting stocks
selected_stock = tk.StringVar()
search_frame = tk.Frame(root, bg=SECONDARY_COLOR)
search_frame.pack(pady=10, anchor="center")

stock_label = tk.Label(search_frame, text="Select Stock", font=(FONT_FAMILY, 14, "bold"), fg=TEXT_COLOR, bg=SECONDARY_COLOR)
stock_label.pack()

# Styled Entry Box with Padding
search_entry = ttk.Entry(search_frame, textvariable=selected_stock, font=(FONT_FAMILY, 12), width=25)
search_entry.pack(pady=5, ipady=5)  # ipady for better height

# Styled Suggestion Listbox (Dropdown Effect)
suggestion_listbox = tk.Listbox(search_frame, width=25, height=4, font=(FONT_FAMILY, 12),
                                bg=SECONDARY_COLOR, fg=TEXT_COLOR, highlightbackground=PRIMARY_COLOR,
                                selectbackground=PRIMARY_COLOR, selectforeground="black",
                                relief="flat", borderwidth=2)
suggestion_listbox.pack()
suggestion_listbox.configure(exportselection=False)
suggestion_listbox.pack_forget()  # Initially hidden

def update_suggestions(event):
    query = search_entry.get().upper()
    suggestion_listbox.delete(0, tk.END)
    matches = [t for t in tickers if query in t]

    if matches:
        for match in matches[:5]:  # Limit suggestions to 5
            suggestion_listbox.insert(tk.END, match)
        suggestion_listbox.pack()
    else:
        suggestion_listbox.pack_forget()  # Hide when no match

def select_stock(event):
    selected_stock.set(suggestion_listbox.get(tk.ACTIVE))
    suggestion_listbox.pack_forget()  # Hide after selection

search_entry.bind("<KeyRelease>", update_suggestions)
suggestion_listbox.bind("<ButtonRelease-1>", select_stock)

# Dropdown for selecting price type
price_options = ["Open", "High", "Low", "Close"]
selected_price = tk.StringVar()
price_dropdown = ttk.Combobox(root, textvariable=selected_price, values=price_options, state="readonly", width=20, font=(FONT_FAMILY, 12))
price_dropdown.pack(pady=10)
price_dropdown.set("Select price type")

# Date Picker Frame
frame = tk.Frame(root, bg=SECONDARY_COLOR)
frame.pack(pady=10)

date_label = tk.Label(frame, text="From - To:", font=(FONT_FAMILY, 16, "bold"), fg=TEXT_COLOR, bg=SECONDARY_COLOR)
date_label.grid(row=0, column=0, padx=10, pady=5)

# Date Pickers
from_date = DateEntry(frame, width=12, background=PRIMARY_COLOR, foreground="black", borderwidth=2, font=(FONT_FAMILY, 12))
from_date.grid(row=0, column=1, padx=5)

to_date = DateEntry(frame, width=12, background=PRIMARY_COLOR, foreground="black", borderwidth=2, font=(FONT_FAMILY, 12))
to_date.grid(row=0, column=2, padx=5)

# Canvas for Matplotlib Graph
graph_frame = tk.Frame(root, bg=SECONDARY_COLOR)
graph_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Function to fetch and plot stock data
def show_selection():
    stock = selected_stock.get()
    price_type = selected_price.get()
    start = from_date.get_date()
    end = to_date.get_date()
    
    if not stock or stock not in tickers:
        result_label.config(text="⚠️ Please select a valid stock!", fg="red")
        return

    if not price_type or price_type == "Select price type":
        result_label.config(text="⚠️ Please select a price type!", fg="red")
        return

    try:
        data = yf.download(stock, start=start, end=end)
        
        if data.empty:
            result_label.config(text="⚠️ No data available for the selected date range!", fg="red")
            return

        for widget in graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor(SECONDARY_COLOR)
        ax.set_facecolor(SECONDARY_COLOR)
        ax.plot(data.index, data[price_type], label=f"{price_type} Price", color="#00FF00")
        ax.set_xlabel("Date", fontsize=12, fontname=FONT_FAMILY, color=TEXT_COLOR)
        ax.set_ylabel(f"{price_type} Price (USD)", fontsize=12, fontname=FONT_FAMILY, color=TEXT_COLOR)
        ax.set_title(f"{stock} Stock {price_type} Price", fontsize=14, fontweight="bold", fontname=FONT_FAMILY, color=TEXT_COLOR)
        ax.tick_params(axis='x', colors=TEXT_COLOR)
        ax.tick_params(axis='y', colors=TEXT_COLOR)
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d, %Y"))
        fig.autofmt_xdate(rotation=45)
        ax.grid(True, color=TEXT_COLOR, linestyle='--', linewidth=0.5)
        ax.legend(facecolor=SECONDARY_COLOR, edgecolor=PRIMARY_COLOR, labelcolor=TEXT_COLOR)

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        result_label.config(text=f"Showing {stock} {price_type} prices from {start} to {end}", fg="green")
    except Exception as e:
        result_label.config(text=f"⚠️ Error: {e}", fg="red")

# Buttons Frame
button_frame = tk.Frame(root, bg=SECONDARY_COLOR)
button_frame.pack(pady=10)

# Show Button
show_button = tk.Button(button_frame, text="Show", font=(FONT_FAMILY, 14, "bold"), fg=SECONDARY_COLOR, bg=PRIMARY_COLOR, command=show_selection)
show_button.grid(row=0, column=0, padx=10)

# Back Button
def go_back():
    root.destroy()
    subprocess.Popen(["python", "MainDashBoard.py"])  # Open MainDashBoard.py

back_button = tk.Button(button_frame, text="Back", font=(FONT_FAMILY, 14, "bold"), fg=SECONDARY_COLOR, bg='red', command=go_back)
back_button.grid(row=0, column=1, padx=10)

# Result Label
result_label = tk.Label(root, text="", font=(FONT_FAMILY, 14), fg=TEXT_COLOR, bg=SECONDARY_COLOR)
result_label.pack(pady=10)

root.mainloop()

