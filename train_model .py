# =====================================================
# Import Libraries
# =====================================================

import pandas as pd
import numpy as np
import joblib

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, LSTM, Dense, Dropout

# =====================================================
# Load Dataset
# =====================================================

data = pd.read_excel("climate_dataset_1500_rows.xlsx")

print("Dataset Loaded Successfully")


# =====================================================
# Risk Label Creation
# =====================================================

def risk_level(row):

    if row['Temperature'] > 40 or row['Rainfall'] > 120:
        return 3
    elif row['Temperature'] > 35:
        return 2
    elif row['Humidity'] > 80:
        return 1
    else:
        return 0


data['Risk'] = data.apply(risk_level, axis=1)


# =====================================================
# Feature Selection
# =====================================================

features = data[['Temperature','Rainfall','Humidity','Wind Speed']]


# =====================================================
# Normalization
# =====================================================

scaler = MinMaxScaler()

scaled_data = scaler.fit_transform(features)

joblib.dump(scaler,"scaler.pkl")


# =====================================================
# Time Series Creation
# =====================================================

X=[]
y=[]

time_step=5

for i in range(len(scaled_data)-time_step):

    X.append(scaled_data[i:i+time_step])
    y.append(data['Risk'].iloc[i+time_step])

X=np.array(X)
y=np.array(y)


# =====================================================
# Train Test Split
# =====================================================

X_train,X_test,y_train,y_test=train_test_split(
    X,y,test_size=0.2,random_state=42
)


# =====================================================
# CNN + LSTM Model
# =====================================================

model=Sequential()

model.add(
Conv1D(
64,
2,
activation='relu',
input_shape=(X_train.shape[1],X_train.shape[2])
)
)

model.add(LSTM(50))

model.add(Dropout(0.2))

model.add(Dense(4,activation='softmax'))

model.compile(
optimizer='adam',
loss='sparse_categorical_crossentropy',
metrics=['accuracy']
)

model.summary()


# =====================================================
# Train Model
# =====================================================

model.fit(
X_train,
y_train,
epochs=20,
batch_size=32,
validation_data=(X_test,y_test)
)


# =====================================================
# Save Model
# =====================================================

model.save("climate_model.h5")

print("Model Saved Successfully")