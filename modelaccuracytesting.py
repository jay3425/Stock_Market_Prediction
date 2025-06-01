import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC, SVR
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
from math import sqrt

# Load data
data = pd.read_csv(r"C:\Users\user\OneDrive\Desktop\Stock Market Prediction Model\stocks\A.csv")
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

data['Open-Close'] = data['Open'] - data['Close']
data['High-Low'] = data['High'] - data['Low']
data = data.dropna()

# Feature selection
x = data[['Open-Close', 'High-Low']]

# Classification target variable
y_class = np.where(data['Close'].shift(-1) > data['Close'], 1, -1)

# Regression target variable
y_reg = data['Close']

# Train-test split
x_train, x_test, y_train_class, y_test_class = train_test_split(x, y_class, test_size=0.25, random_state=44)
x_train, x_test, y_train_reg, y_test_reg = train_test_split(x, y_reg, test_size=0.25, random_state=44)

# Classification Models
classification_models = {
    'SVM': SVC(kernel='linear'),
    'Logistic Regression': LogisticRegression(),
    'Random Forest': RandomForestClassifier(n_estimators=100),
    'KNN': KNeighborsClassifier(n_neighbors=5),
    'Gradient Boosting': GradientBoostingClassifier()
}

classification_results = {}
for name, model in classification_models.items():
    model.fit(x_train, y_train_class)
    accuracy = accuracy_score(y_test_class, model.predict(x_test))
    classification_results[name] = accuracy

# Regression Models
regression_models = {
    'SVR': SVR(kernel='linear', C=1),
    'Linear Regression': LinearRegression(),
    'Random Forest Regressor': RandomForestRegressor(n_estimators=100),
    'KNN Regressor': KNeighborsRegressor(n_neighbors=5),
    'Gradient Boosting Regressor': GradientBoostingRegressor()
}

regression_results = {}
for name, model in regression_models.items():
    model.fit(x_train, y_train_reg)
    predictions = model.predict(x_test)
    rms = sqrt(mean_squared_error(y_test_reg, predictions))
    regression_results[name] = rms

# Print results
print("Classification Model Accuracies:")
for model, accuracy in classification_results.items():
    print(f"{model}: {accuracy:.2f}")

print("\nRegression Model RMSE:")
for model, rms in regression_results.items():
    print(f"{model}: {rms:.2f}")





import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC, SVR
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, mean_squared_error
from math import sqrt

# Load data
data = pd.read_csv(r"C:\Users\user\OneDrive\Desktop\Stock Market Prediction Model\stocks\A.csv")
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

data['Open-Close'] = data['Open'] - data['Close']
data['High-Low'] = data['High'] - data['Low']
data = data.dropna()

# Feature selection
x = data[['Open-Close', 'High-Low']]

# Classification target variable
y_class = np.where(data['Close'].shift(-1) > data['Close'], 1, -1)

# Regression target variable
y_reg = data['Close']

# Normalize data for LSTM
scaler = MinMaxScaler()
x_scaled = scaler.fit_transform(x)
y_scaled = scaler.fit_transform(y_reg.values.reshape(-1, 1))

# Prepare LSTM data
def create_sequences(x, y, time_steps=10):
    x_seq, y_seq = [], []
    for i in range(len(x) - time_steps):
        x_seq.append(x[i:i+time_steps])
        y_seq.append(y[i+time_steps])
    return np.array(x_seq), np.array(y_seq)

TIME_STEPS = 10
x_lstm, y_lstm = create_sequences(x_scaled, y_scaled, TIME_STEPS)

# Train-test split
x_train, x_test, y_train_class, y_test_class = train_test_split(x, y_class, test_size=0.25, random_state=44)
x_train, x_test, y_train_reg, y_test_reg = train_test_split(x, y_reg, test_size=0.25, random_state=44)

# Split LSTM data
split = int(0.75 * len(x_lstm))
x_train_lstm, x_test_lstm = x_lstm[:split], x_lstm[split:]
y_train_lstm, y_test_lstm = y_lstm[:split], y_lstm[split:]

# Classification Models
classification_models = {
    'SVM': SVC(kernel='linear'),
    'Logistic Regression': LogisticRegression(),
    'Random Forest': RandomForestClassifier(n_estimators=100),
    'KNN': KNeighborsClassifier(n_neighbors=5),
    'Gradient Boosting': GradientBoostingClassifier()
}

classification_results = {}
for name, model in classification_models.items():
    model.fit(x_train, y_train_class)
    accuracy = accuracy_score(y_test_class, model.predict(x_test))
    classification_results[name] = accuracy

# Regression Models
regression_models = {
    'SVR': SVR(kernel='linear', C=1),
    'Linear Regression': LinearRegression(),
    'Random Forest Regressor': RandomForestRegressor(n_estimators=100),
    'KNN Regressor': KNeighborsRegressor(n_neighbors=5),
    'Gradient Boosting Regressor': GradientBoostingRegressor()
}

regression_results = {}
for name, model in regression_models.items():
    model.fit(x_train, y_train_reg)
    predictions = model.predict(x_test)
    rms = sqrt(mean_squared_error(y_test_reg, predictions))
    regression_results[name] = rms

# LSTM Model for Regression
model_lstm = Sequential([
    LSTM(50, return_sequences=True, input_shape=(TIME_STEPS, x_lstm.shape[2])),
    Dropout(0.2),
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(1)
])

model_lstm.compile(optimizer='adam', loss='mean_squared_error')
model_lstm.fit(x_train_lstm, y_train_lstm, epochs=50, batch_size=16, validation_data=(x_test_lstm, y_test_lstm))

lstm_predictions = model_lstm.predict(x_test_lstm)
lstm_rmse = sqrt(mean_squared_error(y_test_lstm, lstm_predictions))
regression_results['LSTM'] = lstm_rmse

# Print results
print("Classification Model Accuracies:")
for model, accuracy in classification_results.items():
    print(f"{model}: {accuracy:.2f}")

print("\nRegression Model RMSE:")
for model, rms in regression_results.items():
    print(f"{model}: {rms:.2f}")