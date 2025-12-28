import requests
from fastapi import Request

def get_exchange_rate(base_currency: str, target_currency: str, request: Request):
    api_key = request.app.state.config.CURRENCY_EXCHANGE_API_KEY
    url = (
        f"https://v6.exchangerate-api.com/v6/"
        f"{api_key}/pair/{base_currency}/{target_currency}"
    )

    request.app.logger.info("Making call to exchangerate API")
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if response.status_code == 200:
            return {"base_currency": base_currency, "target_currency": target_currency, "exchange_rate": data.get("conversion_rate")}

        request.app.logger.error(
            "Fetching failed",
            extra={"error_code": response.status_code,"error_details": response.text})
        return {"error_code": response.status_code, "error_details": data.get("error-type", "Unknown error")}

    except Exception as e:
        request.app.logger.error("Exception occurred during making call", extra={"error": str(e)},)
        return {"error": f"An unexpected error occurred: {e}"}

