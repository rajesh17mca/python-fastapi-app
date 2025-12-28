import requests
from fastapi import Request

def fetch_weather(city: str, request: Request):
    api_key = request.app.state.config.WEATHER_API_KEY
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    request.app.logger.info("Making a call to weather API")

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {"condition": data["current"]["condition"]["text"], "weather": data["current"]["temp_c"], "wind": data["current"]["wind_kph"]}
        else:
            request.app.logger.error(
                "Fetching failed",
                extra={"error_code": response.status_code, "error_details": response.text})
            return {"error_code": response.status_code,"error_details": response.text}

    except Exception as e:
        request.app.logger.error("Exception occurred during making call",extra={"error": str(e)},)
        return {"error": f"An unexpected error occurred: {e}"}
