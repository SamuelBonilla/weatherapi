import requests

from src.api import app

url = "http://0.0.0.0:8000"

def test_validate_format():
    response = requests.get(f"{url}/weather?city=Bogota&country=co")
    validate_format = {
            "location_name": str,
            "temperature": str,
            "wind": str,
            "cloudiness": str,
            "pressure": str,
            "humidity": str,
            "sunrise": str,
            "sunset": str,
            "geo_coordinates": list,
            "requested_time": str,
            "forecast": dict
    }
    assert list(sorted(response.json().keys())) == list(sorted(validate_format.keys()))


def test_validate_200():
    response = requests.get(f"{url}/weather?city=Bogota&country=co")
    assert response.status_code == 200


def test_invalid_city():
    response = requests.get(f"{url}/weather?city=Bogsssa&country=co")
    assert response.json() == { "cod": "404", "message": "city not found" }


def test_invalid_country_param():
    response = requests.get(f"{url}/weather?city=Bogota")
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "query",
                    "country"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
