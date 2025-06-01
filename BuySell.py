# import pandas as pd
# import numpy as np
# import tkinter as tk
# from tkinter import ttk, StringVar, Listbox, Scrollbar
# import yfinance as yf
# from sklearn.model_selection import train_test_split
# from sklearn.svm import SVC
# from sklearn.linear_model import LinearRegression
# import subprocess

# # Load S&P 500 tickers
# sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
# tickers = sorted(sp500['Symbol'].tolist())

# # Colors & Fonts
# BG_COLOR = "#121212"  # Dark Mode Background
# TEXT_COLOR = "gold"
# BUTTON_BG = "#FFD700"
# FONT_STYLE = ("Times New Roman", 20, "italic", "bold")

# # UI Functions
# def update_suggestions(event):
#     typed_text = stock_entry.get().upper()
#     filtered_tickers = [t for t in tickers if t.startswith(typed_text)]
#     stock_listbox.delete(0, tk.END)
#     for item in filtered_tickers:
#         stock_listbox.insert(tk.END, item)

# def select_suggestion(event):
#     stock_var.set(stock_listbox.get(stock_listbox.curselection()))
#     stock_listbox.delete(0, tk.END)

# def predict_stock(selected_stock):
#     stock_data = yf.download(selected_stock, period='1y')
#     if stock_data.empty:
#         result_label.config(text="No data found for prediction.", fg="red")
#         return

#     # Feature Engineering
#     stock_data['Open-Close'] = stock_data['Open'] - stock_data['Close']
#     stock_data['High-Low'] = stock_data['High'] - stock_data['Low']
#     stock_data = stock_data.dropna()
#     x = stock_data[['Open-Close', 'High-Low']]
#     y = np.where(stock_data['Close'].shift(-1) > stock_data['Close'], 1, -1)

#     # SVM Model
#     x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=44)
#     model = SVC(kernel='linear')
#     model.fit(x_train, y_train)
#     prediction = model.predict([x.iloc[-1].values])[0]
    
#     # Linear Regression Model for Tomorrow's Price Prediction
#     stock_data['Target'] = stock_data['Close'].shift(-1)
#     stock_data = stock_data.dropna()
#     X_lr = stock_data[['Open', 'High', 'Low', 'Close', 'Volume']]
#     y_lr = stock_data['Target']
#     X_train_lr, X_test_lr, y_train_lr, y_test_lr = train_test_split(X_lr, y_lr, test_size=0.25, random_state=44)
#     lr_model = LinearRegression()
#     lr_model.fit(X_train_lr, y_train_lr)
#     tomorrow_price = lr_model.predict([X_lr.iloc[-1].values])[0]
    
#     # Get Stock Info
#     stock_info = yf.Ticker(selected_stock).info
#     stock_name = stock_info.get('longName', 'N/A')
#     sector = stock_info.get('sector', 'N/A')
#     market_cap = stock_info.get('marketCap', 'N/A')
    
#     # Display Result
#     prediction_text = "BUY" if prediction == 1 else "SELL"
#     result_label.config(text=f"Stock: {stock_name}\nSector: {sector}\nMarket Cap: {market_cap}\nPrediction: {prediction_text}\nPredicted Closing Price Tomorrow: ${tomorrow_price:.2f}",
#                         fg="green" if prediction == 1 else "red")

# def show_prediction():
#     selected_stock = stock_entry.get().upper()
#     if selected_stock not in tickers:
#         result_label.config(text="Error: Please select a valid stock!", fg="red")
#         return
#     predict_stock(selected_stock)

# def go_back():
#     subprocess.Popen(['python', 'MainDashBoard.py'])  
#     root.quit()  
#     root.destroy()

# # GUI Setup
# root = tk.Tk()
# root.title("Stock Prediction")
# root.state('zoomed')
# root.configure(bg=BG_COLOR)

# # Main Frame
# frame = tk.Frame(root, bg=BG_COLOR)
# frame.pack(pady=30)

# # Title
# tk.Label(frame, text="Stock Prediction System", font=("Times New Roman", 50, "italic", "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=10)

# # Stock Selection
# stock_var = StringVar()
# stock_entry = tk.Entry(frame, textvariable=stock_var, font=("Times New Roman", 20), width=40)
# stock_entry.pack(pady=5)
# stock_entry.bind("<KeyRelease>", update_suggestions)

# # Listbox with Scrollbar
# listbox_frame = tk.Frame(frame)
# listbox_frame.pack(pady=5)

# stock_listbox = Listbox(listbox_frame, height=5, width=46, font=("Times New Roman", 15))
# stock_listbox.pack(side=tk.LEFT)

# scrollbar = Scrollbar(listbox_frame, command=stock_listbox.yview)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# stock_listbox.config(yscrollcommand=scrollbar.set)

# stock_listbox.bind("<ButtonRelease-1>", select_suggestion)

# # Buttons
# button_frame = tk.Frame(frame, bg=BG_COLOR)
# button_frame.pack(pady=20)

# show_button = tk.Button(button_frame, text="Show Prediction", width=15, command=show_prediction, bg=BUTTON_BG, font=FONT_STYLE, activebackground="gold")
# show_button.grid(row=0, column=0, padx=10)

# back_button = tk.Button(button_frame, text="Back", width=15, command=go_back, bg="red", font=FONT_STYLE, activebackground="darkred")
# back_button.grid(row=0, column=1, padx=10)

# # Result Label
# result_label = tk.Label(frame, text="", font=("Times New Roman", 20, "italic", "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
# result_label.pack(pady=10)

# # Run
# root.mainloop()






# with the prediction confidence
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, StringVar, Listbox, Scrollbar
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
import subprocess

# Load S&P 500 tickers
sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
tickers = sorted(sp500['Symbol'].tolist())

# Colors & Fonts
BG_COLOR = "#121212"  # Dark Mode Background
TEXT_COLOR = "gold"
BUTTON_BG = "#FFD700"
FONT_STYLE = ("Times New Roman", 20, "italic", "bold")

# UI Functions
def update_suggestions(event):
    typed_text = stock_entry.get().upper()
    filtered_tickers = [t for t in tickers if t.startswith(typed_text)]
    stock_listbox.delete(0, tk.END)
    for item in filtered_tickers:
        stock_listbox.insert(tk.END, item)

def select_suggestion(event):
    stock_var.set(stock_listbox.get(stock_listbox.curselection()))
    stock_listbox.delete(0, tk.END)

def predict_stock(selected_stock):
    stock_data = yf.download(selected_stock, period='1y')
    if stock_data.empty:
        result_label.config(text="No data found for prediction.", fg="red")
        return

    # Feature Engineering
    stock_data['Open-Close'] = stock_data['Open'] - stock_data['Close']
    stock_data['High-Low'] = stock_data['High'] - stock_data['Low']
    stock_data = stock_data.dropna()
    x = stock_data[['Open-Close', 'High-Low']]
    y = np.where(stock_data['Close'].shift(-1) > stock_data['Close'], 1, -1)

    # SVM Model
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=44)
    model = SVC(kernel='linear', probability=True)  # Enable probability estimates
    model.fit(x_train, y_train)
    prediction = model.predict([x.iloc[-1].values])[0]
    confidence = model.predict_proba([x.iloc[-1].values])[0].max() * 100  # Get probability of the predicted class

    # Linear Regression Model for Tomorrow's Price Prediction
    stock_data['Target'] = stock_data['Close'].shift(-1)
    stock_data = stock_data.dropna()
    X_lr = stock_data[['Open', 'High', 'Low', 'Close', 'Volume']]
    y_lr = stock_data['Target']
    X_train_lr, X_test_lr, y_train_lr, y_test_lr = train_test_split(X_lr, y_lr, test_size=0.25, random_state=44)
    lr_model = LinearRegression()
    lr_model.fit(X_train_lr, y_train_lr)
    tomorrow_price = lr_model.predict([X_lr.iloc[-1].values])[0]

    # Calculate R² score
    r2_score = lr_model.score(X_test_lr, y_test_lr) * 100  # Convert to percentage

    # Get Stock Info
    stock_info = yf.Ticker(selected_stock).info
    stock_name = stock_info.get('longName', 'N/A')
    sector = stock_info.get('sector', 'N/A')
    market_cap = stock_info.get('marketCap', 'N/A')

    # Display Result
    prediction_text = "BUY" if prediction == 1 else "SELL"
    result_label.config(text=f"Stock: {stock_name}\n"
                             f"Sector: {sector}\n"
                             f"Market Cap: {market_cap}\n"
                             f"Prediction: {prediction_text}\n"
                             f"Prediction Confidence: {confidence:.2f}%\n"
                             f"Predicted Closing Price Tomorrow: ${tomorrow_price:.2f}\n"
                             f"Regression Model Accuracy (R² Score): {r2_score:.2f}%",
                        fg="green" if prediction == 1 else "red")

def show_prediction():
    selected_stock = stock_entry.get().upper()
    if selected_stock not in tickers:
        result_label.config(text="Error: Please select a valid stock!", fg="red")
        return
    predict_stock(selected_stock)

def go_back():
    subprocess.Popen(['python', 'MainDashBoard.py'])  
    root.quit()  
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Stock Prediction")
root.state('zoomed')
root.iconbitmap(r'C:\Users\user\OneDrive\Desktop\Stock Market Prediction Model\Icons\buy-sell_18167640.ico')  # Update with your icon path
root.configure(bg=BG_COLOR)

# Main Frame
frame = tk.Frame(root, bg=BG_COLOR)
frame.pack(pady=30)

# Title
tk.Label(frame, text="Stock Prediction System", font=("Times New Roman", 50, "italic", "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=10)

# Stock Selection
stock_var = StringVar()
stock_entry = tk.Entry(frame, textvariable=stock_var, font=("Times New Roman", 20), width=40)
stock_entry.pack(pady=5)
stock_entry.bind("<KeyRelease>", update_suggestions)

# Listbox with Scrollbar
listbox_frame = tk.Frame(frame)
listbox_frame.pack(pady=5)

stock_listbox = Listbox(listbox_frame, height=5, width=46, font=("Times New Roman", 15))
stock_listbox.pack(side=tk.LEFT)

scrollbar = Scrollbar(listbox_frame, command=stock_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
stock_listbox.config(yscrollcommand=scrollbar.set)

stock_listbox.bind("<ButtonRelease-1>", select_suggestion)

# Buttons
button_frame = tk.Frame(frame, bg=BG_COLOR)
button_frame.pack(pady=20)

show_button = tk.Button(button_frame, text="Show Prediction", width=15, command=show_prediction, bg=BUTTON_BG, font=FONT_STYLE, activebackground="gold")
show_button.grid(row=0, column=0, padx=10)

back_button = tk.Button(button_frame, text="Back", width=15, command=go_back, bg="red", font=FONT_STYLE, activebackground="darkred")
back_button.grid(row=0, column=1, padx=10)

# Result Label
result_label = tk.Label(frame, text="", font=("Times New Roman", 20, "italic", "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
result_label.pack(pady=10)

# Run
root.mainloop()






