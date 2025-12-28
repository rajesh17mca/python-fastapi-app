import requests
from fastapi import Request

def search_city_by_name(place: str, request: Request):
    url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={place}&count=1&language=en&format=json"
    )
    request.app.logger.info("Making call to geocoding API", extra={"url": url})

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if "results" in data and data["results"]:
            result = data["results"][0]
            return {"name": result["name"], "country": result["country"], "lat": result["latitude"], "lon": result["longitude"]}

        request.app.logger.error( "Fetching failed",extra={
            "error_code": response.status_code,
            "error_details": response.text},
        )
        return {"error_code": response.status_code, "error_details": response.text}

    except Exception as e:
        request.app.logger.error("Exception occurred during making call", extra={"error": str(e)})
        return {"error": f"An unexpected error occurred: {e}"}
