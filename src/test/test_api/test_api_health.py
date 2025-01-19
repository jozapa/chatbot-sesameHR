import requests

# Base url of the local server
LOCAL_URL = "http://localhost:8000"

# Endpoints for chat ad health checks
CHAT_ENDPOINT = f"{LOCAL_URL}/chat"
HEALTH_ENDPOINT = f"{LOCAL_URL}/health"


def test_get_health():
    """
    Tests the /health GET endpoint.

    Sends a GET request to the /health endpoint and verifies that the response
    contains the expected JSON object {"health": "healthy"}.
    """
    response = requests.get(HEALTH_ENDPOINT)
    response.raise_for_status()
    assert response.json() == {"health": "healthy"}


def test_wrong_post_health():
    """
    Tests the behavior of the /health endpoint with an incorrect HTTP method.

    Sends a POST request to the /health endpoint and verifies that the server
    returns a 405 Method Not Allowed status code and the correct error message.
    """
    response = requests.post(HEALTH_ENDPOINT)
    assert response.status_code == 405
    assert response.json() == {"detail": "Method Not Allowed"}
