import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


def get_uv_description(uv_val):
    if uv_val is None: return "Unknown"
    if uv_val <= 2: return "Low"
    if uv_val <= 5: return "Moderate"
    if uv_val <= 7: return "High"
    if uv_val <= 10: return "Very High"
    return "Extreme"


def get_aqi_description(aqi_val):
    if aqi_val is None: return "Unknown"
    if aqi_val <= 50: return "Good"
    if aqi_val <= 100: return "Moderate"
    if aqi_val <= 150: return "Unhealthy for Sensitive Groups"
    if aqi_val <= 200: return "Unhealthy"
    if aqi_val <= 300: return "Very Unhealthy"
    return "Hazardous"


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def smart(request):
    lat = request.query_params.get('lat')
    lon = request.query_params.get('lon')

    if not lat or not lon:
        return Response(
            {"error": "Please provide both 'lat' and 'lon' query parameters."},
            status=status.HTTP_400_BAD_REQUEST
        )

    coordinates = {"latitude": lat, "longitude": lon}
    weather_url = "https://api.open-meteo.com/v1/forecast"
    air_quality_url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    weather_params = {
        **coordinates,
        "current": "temperature_2m,relative_humidity_2m,uv_index",
        "temperature_unit": "celsius"
    }
    aqi_params = {
        **coordinates,
        "current": "us_aqi"
    }

    try:
        weather_response = requests.get(weather_url, params=weather_params, timeout=10)
        aqi_response = requests.get(air_quality_url, params=aqi_params, timeout=10)

        weather_response.raise_for_status()
        aqi_response.raise_for_status()

        current_weather = weather_response.json().get("current", {})
        current_aqi = aqi_response.json().get("current", {})

        payload = {
            "location": {"latitude": lat, "longitude": lon},
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

    except requests.exceptions.RequestException as e:
        print(f"[BestBliss] Open-Meteo failed: {type(e).__name__}: {e}")
        return Response(
            {"error": "Failed to fetch aggregated metrics from external providers."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )