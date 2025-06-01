
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import numpy as np
import subprocess

# Download S&P 500 stock list
sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
tickers = sorted(sp500['Symbol'].tolist())  # Sorted for better UX

# Function to fetch stock data and plot
def fetch_stock_data():
    stock_ticker = dropdown.get().strip().upper()  # Get the selected ticker from the dropdown
    if not stock_ticker:
        messagebox.showerror("Error", "Please select a stock ticker!")
        return

    try:
        # Get the selected date range
        date_range = date_range_var.get()
        end_date = datetime.now()
        start_date = end_date - timedelta(days=date_range)

        # Fetch stock data
        stock = yf.Ticker(stock_ticker)
        stock_history = stock.history(start=start_date, end=end_date)

        if stock_history.empty:
            messagebox.showerror("Error", "Invalid stock ticker or no data available!")
            return

        # Clear previous plot and table
        for widget in graph_frame.winfo_children():
            widget.destroy()
        for widget in table_frame.winfo_children():
            widget.destroy()

        # Calculate percentage growth
        initial_price = stock_history['Close'].iloc[0]
        current_price = stock_history['Close'].iloc[-1]
        growth_percentage = ((current_price - initial_price) / initial_price) * 100

        # Predict potential growth (simple linear regression for demonstration)
        x = np.arange(len(stock_history))
        y = stock_history['Close'].values
        coefficients = np.polyfit(x, y, 1)
        potential_growth = coefficients[0] * 30  # Predict growth over the next 30 days

        # Display growth percentage and potential growth
        growth_label.config(text=f"Actual Growth: {growth_percentage:.2f}%", fg='#00FF00' if growth_percentage >= 0 else '#FF6347')
        potential_growth_label.config(text=f"Potential Growth (Next 30 Days): {potential_growth:.2f}%", fg='#00FF00' if potential_growth >= 0 else '#FF6347')

        # Plot 1: Stock Price Trend
        fig1, ax1 = plt.subplots(figsize=(8, 4), facecolor='#1E1E1E')
        stock_history['Close'].plot(ax=ax1, title=f"{stock_ticker} Stock Price", color='#FFD700')
        ax1.set_facecolor('#2E2E2E')
        ax1.grid(True, linestyle='--', alpha=0.7, color='#555555')
        ax1.set_xlabel("Date", color='#FFD700')
        ax1.set_ylabel("Price (USD)", color='#FFD700')
        ax1.tick_params(axis='x', colors='#FFD700')
        ax1.tick_params(axis='y', colors='#FFD700')
        ax1.title.set_color('#FFD700')

        # Plot 2: Volume vs. Price
        fig2, ax2 = plt.subplots(figsize=(8, 4), facecolor='#1E1E1E')
        ax2.bar(stock_history.index, stock_history['Volume'], color='#FFD700', alpha=0.6, label='Volume')
        ax2.set_ylabel("Volume", color='#FFD700')
        ax2.tick_params(axis='y', labelcolor='#FFD700')

        ax2_secondary = ax2.twinx()
        ax2_secondary.plot(stock_history.index, stock_history['Close'], color='#00FF00', label='Price')
        ax2_secondary.set_ylabel("Price (USD)", color='#00FF00')
        ax2_secondary.tick_params(axis='y', labelcolor='#00FF00')

        ax2.set_title(f"{stock_ticker} Volume vs. Price", color='#FFD700')
        ax2.set_facecolor('#2E2E2E')
        ax2.grid(True, linestyle='--', alpha=0.7, color='#555555')
        ax2.set_xlabel("Date", color='#FFD700')
        ax2.tick_params(axis='x', colors='#FFD700')
        ax2.legend(loc='upper left', facecolor='#1E1E1E', edgecolor='#FFD700', labelcolor='#FFD700')
        ax2_secondary.legend(loc='upper right', facecolor='#1E1E1E', edgecolor='#00FF00', labelcolor='#00FF00')

        # Embed plots in Tkinter window
        canvas1 = FigureCanvasTkAgg(fig1, master=graph_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=BOTH, expand=True)

        canvas2 = FigureCanvasTkAgg(fig2, master=graph_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=BOTH, expand=True)

        # Display key metrics in a table
        table_data = stock_history[['Open', 'High', 'Low', 'Close', 'Volume']].tail(10)  # Last 10 days data
        table = ttk.Treeview(table_frame, columns=("Date", "Open", "High", "Low", "Close", "Volume"), show="headings")
        table.heading("Date", text="Date")
        table.heading("Open", text="Open")
        table.heading("High", text="High")
        table.heading("Low", text="Low")
        table.heading("Close", text="Close")
        table.heading("Volume", text="Volume")

        for index, row in table_data.iterrows():
            table.insert("", "end", values=(index.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'], row['Volume']))

        table.pack(fill=BOTH, expand=True)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to clear input and results
def clear_input():
    dropdown.set('')  # Clear the dropdown selection
    for widget in graph_frame.winfo_children():
        widget.destroy()
    for widget in table_frame.winfo_children():
        widget.destroy()
    growth_label.config(text="Actual Growth: N/A", fg='#FFD700')
    potential_growth_label.config(text="Potential Growth (Next 30 Days): N/A", fg='#FFD700')

def go_back():
    root.destroy()
    subprocess.Popen(["python", "MainDashBoard.py"])

# Create the main window
root = Tk()
root.title("Stock Forecasting")
root.state("zoomed") # Adjusted height
root.iconbitmap(r'C:\Users\user\OneDrive\Desktop\Stock Market Prediction Model\Icons\predictive-analysis.ico')
root.configure(bg='#1E1E1E')

# Header
header = Label(root, text="Stock Forecasting Tool", font=("Arial", 24, "bold"), bg='#1E1E1E', fg='#FFD700')
header.pack(pady=10)

# Input frame
input_frame = Frame(root, bg='#1E1E1E')
input_frame.pack(pady=10)

# Label and Dropdown for stock ticker
label = Label(input_frame, text="Select Stock:", font=("Arial", 14), bg='#1E1E1E', fg='#FFD700')
label.grid(row=0, column=0, padx=5)

dropdown = ttk.Combobox(input_frame, font=("Arial", 14), width=20)
dropdown['values'] = tickers  # Set initial values as the full S&P 500 list
dropdown.grid(row=0, column=1, padx=5)

# Date range selection
date_range_var = IntVar(value=365)  # Default: 1 year
date_range_menu = ttk.Combobox(input_frame, font=("Arial", 14), width=15, textvariable=date_range_var)
date_range_menu['values'] = [30, 90, 180, 365]  # 1 month, 3 months, 6 months, 1 year
date_range_menu.grid(row=0, column=2, padx=5)

# Fetch button
fetch_button = Button(input_frame, text="Fetch Data", font=("Arial", 14), bg='#4CAF50', fg='white', command=fetch_stock_data)
fetch_button.grid(row=0, column=3, padx=10)

# Clear button
clear_button = Button(input_frame, text="Clear", font=("Arial", 14), bg='#f44336', fg='white', command=clear_input)
clear_button.grid(row=0, column=4, padx=10)

# Back button
back_button = Button(input_frame, text="Back", font=("Arial", 14), bg='#f44336', fg='white', command=go_back)
back_button.grid(row=0, column=5, padx=10)

# Growth percentage label
growth_label = Label(root, text="Actual Growth: N/A", font=("Arial", 16), bg='#1E1E1E', fg='#FFD700')
growth_label.pack(pady=10)

# Potential growth label
potential_growth_label = Label(root, text="Potential Growth (Next 30 Days): N/A", font=("Arial", 16), bg='#1E1E1E', fg='#FFD700')
potential_growth_label.pack(pady=10)

# Graph frame
graph_frame = Frame(root, bg='#1E1E1E')
graph_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Table frame
table_frame = Frame(root, bg='#1E1E1E')
table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Run the application
root.mainloop()




