# -*- coding: utf-8 -*-
"""train_model

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ibaqbcoqkp7-XX7vG35GeGYW1H3Vhcvz
"""

import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from datetime import datetime, timedelta

# Fetch historical data for EUR/USD from Yahoo Finance API
data = yf.download('EURUSD=X', start='2010-01-01', end=datetime.now())

# Resample the data to weekly frequency and calculate OHLC (Open, High, Low, Close) prices
weekly_data = data.resample('W').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'})

# Drop rows with missing values
weekly_data.dropna(inplace=True)

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(weekly_data)

# Convert scaled data back to DataFrame
scaled_df = pd.DataFrame(scaled_data, columns=weekly_data.columns, index=weekly_data.index)

# Split the data into features (X) and target variable (y)
X = scaled_df[['Open', 'High', 'Low']]
y = scaled_df['Close']

# Build the model
model = Sequential([
    Dense(64, activation='relu', input_shape=(X.shape[1],)),
    Dense(64, activation='relu'),
    Dense(1)
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X, y, epochs=100, batch_size=32, verbose=0)

# Save the trained model
model.save('exchange_rate_prediction_model.h5')