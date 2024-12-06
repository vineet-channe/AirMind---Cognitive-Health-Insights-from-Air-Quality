import streamlit as st
import numpy as np
from keras import models
from api_utils import get_air_quality_data
from sklearn.preprocessing import StandardScaler
import joblib

# Load pre-trained model
model = joblib.load('/Users/vineetchanne/Desktop/CV PROJECTS/airquality/model/nn_model.pkl')

# Custom styles for background with spinning Earth GIF
st.markdown("""
    <style>
        .stApp {
            background: url('https://media.giphy.com/media/l1KVcrdl7rJpFnY2s/giphy.gif') no-repeat center center fixed; 
            background-size: cover;
            background-position: center;
            background-attachement: fixed
        }
        .stTitle {
            color: white;
            font-weight: 700;
            text-align: center;
            font-size: 3rem;
            text-transform: uppercase;
            margin-top: 2rem;
        }
        .stHeader {
            color: #ecf0f1;
            text-align: center;
            margin-top: 1rem;
        }
        .stText {
            font-size: 16px;
            color: #ecf0f1;
            text-align: center;
        }
        .stButton button {
            background-color: #2980b9;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            padding: 12px 24px;
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #3498db;
            transform: scale(1.05);
        }
        .stAlert {
            padding: 20px;
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 0.1);
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
        }
        .stAlertSuccess {
            background-color: rgba(46, 204, 113, 0.1);
        }
        .stAlertError {
            background-color: rgba(231, 76, 60, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Main Title
st.title("🌍 Cognitive Health Assessment Based on Air Quality 🧠")

# Additional text
st.markdown("""
### Cognitive Health and Air Quality

Cognitive health is essential for maintaining mental clarity, focus, and overall brain function. Air quality plays a crucial role in cognitive health. Exposure to high levels of air pollutants, such as **PM2.5**, **PM10**, **CO**, **NO₂**, **SO₂**, and **O₃**, has been linked to cognitive decline and mental health issues. This app allows you to assess the cognitive health impact based on real-time air quality data for any given location.

As part of a healthy environment, good air quality is vital for maintaining the brain's functionality. Poor air quality has been shown to adversely affect cognitive abilities and increase risks for mental health issues, particularly in areas with high levels of air pollution. 
""")

# Streamlit UI for Input
st.sidebar.header("Real-Time Input Parameters 🌱")

lat = st.sidebar.number_input("📍 Enter Latitude", value=37.7749, help="Provide latitude of your location.")
lon = st.sidebar.number_input("📍 Enter Longitude", value=-122.4194, help="Provide longitude of your location.")

# Remove the first button, just keep the second one
fetch_button = st.sidebar.button("🔄 Fetch Air Quality Data")
predict_button = st.sidebar.button("📊 Predict Cognitive Health Impact")

# Create an empty placeholder to hold dynamic content that will change after button presses
placeholder = st.empty()

# Fetch Air Quality Data
if fetch_button:
    with st.spinner('Fetching data...'):
        try:
            air_quality_data = get_air_quality_data(lat, lon)
            if air_quality_data:
                air_quality_data["temperature"] = 25  # Default placeholder temperature
                st.session_state.air_quality_data = air_quality_data
                st.success("✅ Air Quality Data Fetched Successfully!", icon="✅")
                st.write("🌿 Air Quality Data:", air_quality_data)

                # Move everything down by clearing and re-rendering the content
                placeholder.empty()
                st.write("🌍 **Air Quality Data** successfully fetched!")
            else:
                st.error("❌ No valid air quality data returned. Please try again.")
        except Exception as e:
            st.error(f"❌ Error fetching air quality data: {e}")

# Predict Cognitive Health Impact
if predict_button:
    if 'air_quality_data' not in st.session_state:
        st.error("❌ Air Quality Data is not available. Please fetch data first!")
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

            # Ensure prediction is accessed correctly
            predicted_value = prediction[0][0] if prediction.ndim > 1 else prediction[0]  # Access the first (and only) element in the array

            st.success(f"📈 Predicted Cognitive Health Impact Score: {predicted_value:.2f}")

            # Display result with some creative flair
            if predicted_value > 0.7:
                st.markdown(
                    "<div class='stAlert stAlertError'><h3 style='color:red;'>❗ High Impact on Cognitive Health</h3></div>",
                    unsafe_allow_html=True)
            elif predicted_value > 0.3:
                st.markdown(
                    "<div class='stAlert'><h3 style='color:orange;'>⚠ Moderate Impact on Cognitive Health</h3></div>",
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    "<div class='stAlert stAlertSuccess'><h3 style='color:green;'>✅ Low Impact on Cognitive Health</h3></div>",
                    unsafe_allow_html=True)

            # Move everything down by clearing and re-rendering the content
            placeholder.empty()
            st.write("🌍 **Cognitive Health Impact** predicted successfully!")
        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
