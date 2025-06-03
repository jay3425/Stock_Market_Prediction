![](https://github.com/jay3425/Stock_Market_Prediction/blob/my-new-branch/Screenshot%20(452).png)
# 📈 Stock Market Prediction Dashboard

An interactive, AI-powered stock prediction and visualization dashboard built with Python and Tkinter. This system offers a suite of tools for stock analysis, including price forecasting, buy/sell signals, market cap trends, model accuracy testing, and secure login authentication.

---

## 🚀 Features

### 🔐 Login System
- Secure access via a Tkinter-based login portal with hardcoded credentials (for demonstration).
- User-friendly interface with custom icons and visual branding.

### 📊 Main Dashboard
- Central hub to navigate between features: data analysis, forecasting, buy/sell, market cap, and visuals.
- Fully GUI-based with real-time stock ticker filtering and responsive design.

### 📈 Stock Prediction
- Machine Learning-based **Buy/Sell recommendations** using SVM.
- **Price Forecasting** using Linear Regression for the next day’s closing price.
- Accuracy and confidence metrics displayed in real-time.

### 📉 Forecasting Tool
- Visualize growth trends over custom date ranges.
- See actual and predicted percentage growth over the next 30 days using linear regression.
- Dual-chart interface for price and volume analysis.

### 📊 Market Cap & Sector Analysis
- Real-time data scraping from Wikipedia for S&P 500 stocks.
- Market cap display, sector/industry breakdown, and return visualization.
- Profit/loss tracking over multiple durations (30–365 days).
- Daily returns histogram and historical trend plots.

### 📡 Model Accuracy Testing
- Compare classification models (SVM, Random Forest, KNN, etc.).
- Evaluate regression models (Linear Regression, SVR, LSTM).
- Visual output of model accuracy and RMSE scores.
- Deep learning integration via LSTM for time-series prediction.

### 📉 Visual Explorer
- Select and visualize stock prices (Open, High, Low, Close) over any time range.
- Enhanced interactivity with dropdown menus and styled date pickers.

---

## 🧠 Technologies Used

- **Python** (Tkinter, Scikit-learn, TensorFlow, Pandas, NumPy)
- **yFinance** – For real-time stock data
- **Matplotlib** – For plotting and visualization
- **BeautifulSoup** – For web scraping S&P 500 tickers
- **tkcalendar** – Date selection interface

---

## 📂 File Structure

```plaintext
├── LoginPage.py              # Login interface
├── MainDashboard.py          # Central navigation panel
├── BuySell.py                # Buy/Sell prediction tool
├── forecast.py               # Growth forecasting module
├── marketcap.py              # Market cap & sector analytics
├── modelaccuracytesting.py   # ML model benchmarking
├── visual.py                 # Visual stock explorer
├── symbols_valid_meta.csv    # Optional ticker metadata (CSV)
└── README.md                 # Project documentation
````

---

## 💡 How to Run

1. **Install Dependencies**:

   ```bash
   pip install yfinance scikit-learn matplotlib pandas numpy tkcalendar beautifulsoup4 tensorflow
   ```

2. **Run the App**:
   Start from the login interface:

   ```bash
   python LoginPage.py
   ```

3. **Login Credentials** (demo):

   * **Username**: `smp`
   * **Password**: `smp`

---

## 📸 Screenshots

> Include here:

* Login page
![](https://github.com/jay3425/Stock_Market_Prediction/blob/my-new-branch/Screenshot%20(452).png)
* Dashboard layout
![](https://github.com/jay3425/Stock_Market_Prediction/blob/my-new-branch/Screenshot%20(455).png)
* Prediction output
![](https://github.com/jay3425/Stock_Market_Prediction/blob/my-new-branch/Screenshot%20(456).png)
* Forecasting graphs
![](https://github.com/jay3425/Stock_Market_Prediction/blob/my-new-branch/Screenshot%20(457).png)
* Market Cap/Yearly Sector growth
* ![](https://github.com/jay3425/Stock_Market_Prediction/blob/my-new-branch/Screenshot%20(458).png)

---

## 👨‍💻 Author

**Jay dengle** – *Aspiring Data Analyst / ML Engineer*
📧 [jaydengle2005@gmail.com](mailto:jaydengle2005@gmail.com)
🌐 [LinkedIn](https://www.linkedin.com/in/jay-anil-dengle-049952337/) | [GitHub](https://github.com/jay3425)

---

## 📃 License

This project is for educational and demonstration purposes. Feel free to fork, modify, and build upon it.

---


