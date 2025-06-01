
import yfinance as yf
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import requests  
from bs4 import BeautifulSoup
import subprocess  # Import subprocess module

# Function to scrape S&P 500 tickers from Wikipedia
def scrape_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "wikitable"})
    tickers = []
    for row in table.findAll("tr")[1:]:  # Skip the header row
        ticker = row.findAll("td")[0].text.strip()
        tickers.append(ticker)
    return tickers

# Predefined date options
DATE_OPTIONS = [30, 60, 90, 180, 365]  # Date options in days

# Function to fetch and plot stock data
def fetch_data():
    ticker = ticker_combobox.get().strip()
    days = int(date_combobox.get())
    if not ticker:
        return
    
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period=f"{days}d")
        info = stock.info

        market_cap = info.get("marketCap", "N/A")
        sector = info.get("sector", "N/A")
        industry = info.get("industry", "N/A")
        current_price = history['Close'][-1]
        profit_loss = ((current_price - history['Close'][0]) / history['Close'][0]) * 100

        ax0.clear()
        ax1.clear()
        ax2.clear()

        ax0.set_title(
            f'Stock: {ticker}\nSector: {sector} \nIndustry: {industry}\nMarket Cap: ${market_cap / 1e9:.2f} Billion',
            fontsize=14, color='gold', pad=20
        )
        ax0.set_facecolor('black')
        ax0.axis('off')

        ax1.set_title(f'Profit/Loss ({days} Days): {profit_loss:.2f}%', fontsize=14, color='gold')
        ax1.plot(history['Close'], color='gold', linewidth=2)
        ax1.fill_between(history.index, history['Close'], color='gold', alpha=0.3)
        ax1.set_facecolor('black')
        ax1.tick_params(axis='x', colors='gold')
        ax1.tick_params(axis='y', colors='gold')
        
        ax2.set_title('Daily Returns Histogram', fontsize=14, color='gold')
        daily_returns = history['Close'].pct_change().dropna()
        ax2.hist(daily_returns, bins=30, color='gold', edgecolor='black')
        ax2.set_facecolor('black')
        ax2.tick_params(axis='x', colors='gold')
        ax2.tick_params(axis='y', colors='gold')

        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        canvas.draw()
    except Exception as e:
        ax0.clear()
        ax0.set_title(f"Error: {str(e)}", fontsize=16, color='red', pad=20)
        ax0.set_facecolor('black')
        ax0.axis('off')
        canvas.draw()

# Function to clear the plot
def clear_data():
    ax0.clear()
    ax1.clear()
    ax2.clear()
    ax0.set_facecolor('black')
    ax1.set_facecolor('black')
    ax2.set_facecolor('black')
    ax0.axis('off')
    canvas.draw()

# Function to go back to MainDashBoard.py
def go_back():
    subprocess.Popen(['python', 'MainDashBoard.py'])
    root.quit()
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("MarketCap & Yearly Sector")
root.state("zoomed")
root.iconbitmap(r'C:\Users\user\OneDrive\Desktop\Stock Market Prediction Model\Icons\financial-profit.ico')
root.configure(bg='black')

control_frame = tk.Frame(root, bg='black')
control_frame.pack(pady=10)

sp500_tickers = scrape_sp500_tickers()

ticker_label = tk.Label(control_frame, text="Select Stock:", bg='black', fg='gold', font=('Arial', 14))
ticker_label.grid(row=0, column=0, padx=5)
ticker_combobox = ttk.Combobox(control_frame, values=sp500_tickers, width=20, font=('Arial', 14))
ticker_combobox.grid(row=0, column=1, padx=5)
ticker_combobox.current(0)

date_label = tk.Label(control_frame, text="Select Period (Days):", bg='black', fg='gold', font=('Arial', 14))
date_label.grid(row=0, column=2, padx=5)
date_combobox = ttk.Combobox(control_frame, values=DATE_OPTIONS, width=10, font=('Arial', 14))
date_combobox.grid(row=0, column=3, padx=5)
date_combobox.current(0)

fetch_button = tk.Button(control_frame, text="Fetch Data", command=fetch_data, bg='gold', fg='black', font=('Arial', 14))
fetch_button.grid(row=0, column=4, padx=5)

clear_button = tk.Button(control_frame, text="Clear Data", command=clear_data, bg='gold', fg='black', font=('Arial', 14))
clear_button.grid(row=0, column=5, padx=5)

# Back Button
goback_button = tk.Button(control_frame, text="Back", command=go_back, bg='red', fg='white', font=('Arial', 14))
goback_button.grid(row=0, column=6, padx=5)

fig = plt.figure(figsize=(10, 8), facecolor='black')
gs = fig.add_gridspec(3, 1, height_ratios=[1, 2, 2])
ax0 = fig.add_subplot(gs[0])
ax1 = fig.add_subplot(gs[1])
ax2 = fig.add_subplot(gs[2])
ax0.axis('off')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root.mainloop()



