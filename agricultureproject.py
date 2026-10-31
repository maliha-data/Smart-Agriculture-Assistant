
import streamlit as st
import pandas as pd
import requests
import json

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Smart Agriculture Assistant",
    page_icon="🌾",
    layout="wide"
)

# -----------------------------
# Custom CSS Styling
# -----------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #e8f5e9,
        #f1f8e9,
        #e3f2fd
    );
}

/* General text */
p, label, span {
    color: #263238;
}

/* Main title */
.main-title {
    font-size: 45px;
    font-weight: bold;
    text-align: center;
    color: #166534;
    margin-bottom: 5px;
}

/* Subtitle */
.sub-title {
    text-align: center;
    padding: 22px;
    border-radius: 18px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.10);
    color: #263238;
}

/* Dashboard heading */
.dashboard-title {
    color: #166534;
    font-size: 30px;
    font-weight: 800;
    margin-top: 20px;
}

/* Cards */
.card {
    background-color: white;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.10);
    margin-bottom: 20px;
}

.card h3 {
    color: #2e7d32;
}

/* Weather box */
.weather-box {
    background: linear-gradient(
        135deg,
        #43a047,
        #66bb6a
    );
    color: white;
    padding: 25px;
    border-radius: 20px;
    text-align: center;
}

.weather-box h1,
.weather-box h2,
.weather-box p {
    color: white !important;
}

/* Tip box */
.tip-box {
    background-color: #fff8e1;
    padding: 20px;
    border-radius: 15px;
    border-left: 6px solid #ffb300;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #E8F5E9;
}

/* Input */
.stTextInput input {
    background-color: white !important;
    color: #263238 !important;
    border: 2px solid #66BB6A !important;
    border-radius: 10px;
}

/* Select box */
.stSelectbox div[data-baseweb="select"] {
    background-color: white;
    color: #263238;
}

/* Metrics */
[data-testid="stMetricValue"] {
    color: #166534;
}

[data-testid="stMetricLabel"] {
    color: #2E7D32;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Main Title
# -----------------------------

st.markdown(
    '<div class="main-title">🌾 Smart Agriculture Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Smart Weather Monitoring and Agriculture Recommendations</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("🌱 Agriculture Settings")

city = st.sidebar.text_input(
    "Enter Your City",
    placeholder="e.g. Karachi"
)

crop = st.sidebar.selectbox(
    "Select Your Crop",
    ["Wheat", "Rice", "Maize", "Cotton", "Sugarcane"]
)


# -----------------------------
# Crop Information
# -----------------------------

crop_data = {
    "Wheat": {
        "temperature": "15-25°C",
        "water": "Moderate",
        "soil": "Loamy soil",
        "tip": "Avoid excessive watering and monitor soil moisture."
    },

    "Rice": {
        "temperature": "20-35°C",
        "water": "High",
        "soil": "Clayey soil",
        "tip": "Maintain suitable soil moisture for healthy growth."
    },

    "Maize": {
        "temperature": "18-27°C",
        "water": "Moderate",
        "soil": "Well-drained soil",
        "tip": "Provide sufficient water during important growth stages."
    },

    "Cotton": {
        "temperature": "21-30°C",
        "water": "Moderate",
        "soil": "Black soil",
        "tip": "Monitor pests and avoid waterlogging."
    },

    "Sugarcane": {
        "temperature": "20-35°C",
        "water": "High",
        "soil": "Fertile loamy soil",
        "tip": "Maintain regular irrigation and monitor crop growth."
    }
}


# -----------------------------
# Crop Information Display
# -----------------------------

st.header("🌿 Selected Crop Information")

crop_info = crop_data[crop]

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div class="card">
        <h3>🌡️ Suitable Temperature</h3>
        <h2>{crop_info["temperature"]}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="card">
        <h3>💧 Water Requirement</h3>
        <h2>{crop_info["water"]}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    f"""
    <div class="tip-box">
    <h3>🌱 Soil Type</h3>
    <p>{crop_info["soil"]}</p>
    <h3>💡 Farming Tip</h3>
    <p>{crop_info["tip"]}</p>
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Weather API Integration
# -----------------------------

if city:

    try:

        # Step 1: Get City Coordinates

        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )

        geo_response.raise_for_status()

        geo_data = geo_response.json()

        # Display Geocoding API Response
        print("\n========== GEOCODING API DATA ==========")
        print(json.dumps(geo_data, indent=4))

        if "results" not in geo_data or not geo_data["results"]:

            st.error("❌ City not found. Please try another city.")

        else:

            Latitude = geo_data["results"][0]["latitude"]
            Longitude = geo_data["results"][0]["longitude"]

            country = geo_data["results"][0].get(
                "country",
                "Unknown"
            )

            # Step 2: Get Weather Data

            weather_url = "https://api.open-meteo.com/v1/forecast"

            weather_params = {
                "latitude": Latitude,
                "longitude": Longitude,
                "current": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "wind_speed_10m",
                    "precipitation"
                ],
                "daily": [
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_probability_max"
                ],
                "timezone": "auto",
                "forecast_days": 3
            }

            weather_response = requests.get(
                weather_url,
                params=weather_params,
                timeout=10
            )

            weather_response.raise_for_status()

            weather_data = weather_response.json()

            # API DATA IN TERMINAL
            print("\n========== WEATHER API DATA ==========")
            print(json.dumps(weather_data, indent=4))

            # API DATA IN STREAMLIT BROWSER
            st.subheader("🔍 Weather API Response")
            st.json(weather_data)

            # Step 3: Extract Weather Information

            current = weather_data["current"]
            daily = weather_data["daily"]

            temperature = current["temperature_2m"]
            humidity = current["relative_humidity_2m"]
            wind_speed = current["wind_speed_10m"]
            precipitation = current["precipitation"]

            rain_probability = daily[
                "precipitation_probability_max"
            ][0]

            # Step 4: Weather Dashboard

            st.markdown(
                f"""
                <div class="dashboard-title">
                📍 Agriculture Dashboard - {city}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="weather-box">
                <h2>🌤️ Current Weather</h2>
                <h1>{temperature}°C</h1>
                <p>📍 {city}, {country}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Step 5: Weather Metrics

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "💧 Humidity",
                    f"{humidity}%"
                )

            with col2:
                st.metric(
                    "💨 Wind Speed",
                    f"{wind_speed} km/h"
                )

            with col3:
                st.metric(
                    "🌧️ Precipitation",
                    f"{precipitation} mm"
                )

            with col4:
                st.metric(
                    "🌡️ Temperature",
                    f"{temperature}°C"
                )

            # Step 6: Farming Recommendations

            st.header("🌱 Farming Recommendations")

            if rain_probability >= 70:

                irrigation_advice = (
                    "💧 High chance of rain. "
                    "Consider reducing irrigation."
                )

            elif rain_probability >= 40:

                irrigation_advice = (
                    "💧 Moderate chance of rain. "
                    "Monitor weather and adjust irrigation accordingly."
                )

            else:

                irrigation_advice = (
                    "💧 Low chance of rain. "
                    "Ensure proper irrigation and avoid overwatering."
                )

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    f"""
                    <div class="card">
                    <h3>💡 Irrigation Advice</h3>
                    <p>{irrigation_advice}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:

                st.markdown(
                    f"""
                    <div class="card">
                    <h3>🌧️ Rain Probability</h3>
                    <h2>{rain_probability}%</h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Step 7: Three-Day Forecast

            st.header("📅 3-Day Weather Forecast")

            forecast_df = pd.DataFrame({
                "Date": daily["time"],
                "Maximum Temperature (°C)": daily["temperature_2m_max"],
                "Minimum Temperature (°C)": daily["temperature_2m_min"],
                "Rain Probability (%)": daily["precipitation_probability_max"]
            })

            st.dataframe(
                forecast_df,
                use_container_width=True
            )

    except requests.exceptions.RequestException as e:

        st.error(f"❌ API Connection Error: {e}")

    except (KeyError, IndexError, TypeError, ValueError) as e:

        st.error(f"❌ Weather data processing error: {e}")

    except Exception as e:

        st.error(f"❌ Something went wrong: {e}")

else:

    st.info("👈 Please enter a city name in the sidebar to view weather information.")


# -----------------------------
# Footer
# -----------------------------

st.markdown("---")

st.markdown(
    "<center>🌾 Smart Agriculture Assistant | Powered by Open-Meteo API</center>",
    unsafe_allow_html=True
)