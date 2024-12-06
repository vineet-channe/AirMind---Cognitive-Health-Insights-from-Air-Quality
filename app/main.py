import streamlit as st
import numpy as np
from keras import models
from api_utils import get_air_quality_data
from sklearn.preprocessing import StandardScaler

# Load pre-trained model


# Load model
model = models.load_model("/Users/vineetchanne/Desktop/CV PROJECTS/airquality/model/cognitive_health_model_1.h5")



# Streamlit UI
st.title("Cognitive Health Assessment Based on Air Quality")
st.sidebar.header("Real-Time Input Parameters")

# Inputs
lat = st.sidebar.number_input("Enter Latitude", value=37.7749)  # Example: San Francisco
lon = st.sidebar.number_input("Enter Longitude", value=-122.4194)

# Fetch Air Quality Data
if st.sidebar.button("Fetch Air Quality Data"):
    try:
        air_quality_data = get_air_quality_data(lat, lon)
        if air_quality_data:
            air_quality_data["temperature"] = 25  # Default placeholder temperature
            st.session_state.air_quality_data = air_quality_data
            st.success("Air Quality Data Fetched Successfully!")
            st.write("Air Quality Data:", air_quality_data)
        else:
            st.error("No valid air quality data returned. Please try again.")
    except Exception as e:
        st.error(f"Error fetching air quality data: {e}")

# Predict Cognitive Health Impact
if st.sidebar.button("Predict Cognitive Health Impact"):
    if 'air_quality_data' not in st.session_state:
        st.error("Air Quality Data is not available. Please fetch data first!")
    else:
        try:
            air_quality_data = st.session_state.air_quality_data
            # Prepare data for prediction
            input_features = np.array([[
                air_quality_data["pm2_5"],
                air_quality_data["pm10"],
                air_quality_data["co"],
                air_quality_data["no2"],
                air_quality_data["so2"],
                air_quality_data["o3"],
                air_quality_data["temperature"]
            ]])

            # Scale features
            scaler = StandardScaler()
            input_features_scaled = scaler.fit_transform(input_features)

            # Predict using the model
            prediction = model.predict(input_features_scaled)
            st.write(f"Predicted Cognitive Health Impact Score: {prediction[0][0]:.2f}")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
