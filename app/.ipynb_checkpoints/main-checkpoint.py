import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

# Load the trained model and scaler
model = load_model('model/cognitive_health_model.h5')
scaler = StandardScaler()

# Streamlit interface
st.title("Real-Time Cognitive Health Prediction Based on Air Quality")

# Input sliders for air quality data
pm2_5 = st.slider("PM2.5 (µg/m³)", 0, 200, 50)
pm10 = st.slider("PM10 (µg/m³)", 0, 150, 50)
co = st.slider("CO (ppm)", 0.0, 10.0, 1.0)
no2 = st.slider("NO2 (ppb)", 0, 100, 30)
so2 = st.slider("SO2 (ppb)", 0, 50, 10)
o3 = st.slider("O3 (ppb)", 0, 150, 40)
temperature = st.slider("Temperature (°C)", 10, 35, 25)
humidity = st.slider("Humidity (%)", 30, 90, 60)

# Prepare the input data
input_data = np.array([[pm2_5, pm10, co, no2, so2, o3, temperature, humidity]])

# Scale the input data
input_data_scaled = scaler.fit_transform(input_data)

# Make prediction
prediction = model.predict(input_data_scaled)
st.write(f"Predicted Cognitive Health Score: {prediction[0][0]:.2f}")

# Provide feedback based on the predicted score
if prediction[0][0] > 70:
    st.warning("This indicates potentially poor cognitive health. Consider taking preventive measures.")
else:
    st.success("This indicates healthy cognitive health.")
