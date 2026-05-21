import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def smart(request):
    # 1. Capture incoming client coordinate pairs
    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')

    if not lat or not lon:
        return Response(
            {"error": "Please provide both 'lat' and 'lon' query parameters."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Base query configuration pairs
    coordinates = {"latitude": lat, "longitude": lon}

    # 2. Setup endpoints targets
    weather_url = "https://api.open-meteo.com/v1/forecast"
    air_quality_url = "https://api.open-meteo.com/v1/air-quality"

    # Define variables we want from standard weather endpoint
    weather_params = {
        **coordinates,
        "current": "temperature_2m,relative_humidity_2m,uv_index",
        "temperature_unit": "celsius"
    }

    # Define variables we want from air quality endpoint (US AQI standard)
    aqi_params = {
        **coordinates,
        "current": "us_aqi"
    }

    try:
        # 3. Fire requests to both Open-Meteo systems
        weather_response = requests.get(weather_url, params=weather_params, timeout=5)
        aqi_response = requests.get(air_quality_url, params=aqi_params, timeout=5)
        
        # Throw error structural issues immediately if endpoints fail
        weather_response.raise_for_status()
        aqi_response.raise_for_status()

        # Parse payloads
        weather_data = weather_response.json()
        aqi_data = aqi_response.json()

        # 4. Extract target indices from current dictionary payloads
        current_weather = weather_data.get("current", {})
        current_aqi = aqi_data.get("current", {})

        # 5. Build clean dictionary unified data scheme
        payload = {
            "location": {
                "latitude": lat,
                "longitude": lon
            },
            "metrics": {
                "temperature": {
                    "value": current_weather.get("temperature_2m"),
                    "unit": "°C"
                },
                "humidity": {
                    "value": current_weather.get("relative_humidity_2m"),
                    "unit": "%"
                },
                "uv_index": {
                    "value": current_weather.get("uv_index"),
                    "classification": get_uv_description(current_weather.get("uv_index", 0))
                },
                "air_quality": {
                    "value": current_aqi.get("us_aqi"),
                    "classification": get_aqi_description(current_aqi.get("us_aqi", 0)),
                    "unit": "US AQI"
                }
            }
        }

        return Response(payload, status=status.HTTP_200_OK)

    except requests.exceptions.RequestException:
        return Response(
            {"error": "Failed to fetch aggregated metrics from external providers."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )


def get_uv_description(uv_val):
    """Helper categorization block mapping standard UV Index tiers"""
    if uv_val is None: return "Unknown"
    if uv_val <= 2: return "Low"
    if uv_val <= 5: return "Moderate"
    if uv_val <= 7: return "High"
    if uv_val <= 10: return "Very High"
    return "Extreme"


def get_aqi_description(aqi_val):
    """Helper classification block mapping standard EPA US AQI index boundaries"""
    if aqi_val is None: return "Unknown"
    if aqi_val <= 50: return "Good"
    if aqi_val <= 100: return "Moderate"
    if aqi_val <= 150: return "Unhealthy for Sensitive Groups"
    if aqi_val <= 200: return "Unhealthy"
    if aqi_val <= 300: return "Very Unhealthy"
    return "Hazardous"