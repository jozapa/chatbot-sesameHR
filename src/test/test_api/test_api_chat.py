import requests

#Base url of the local server
LOCAL_URL = "http://localhost:8000"

#Endpoints for chat ad health checks
CHAT_ENDPOINT = f"{LOCAL_URL}/chat"
HEALTH_ENDPOINT = f"{LOCAL_URL}/health"


def test_hello_assistant():
    """
    Tests the assistant's ability to respond to a simple greeting.

    Sends a POST request to the /chat endpoint with the user's message "Hola"
    and checks if the response contains the "assistant" key and a valid reply
    that includes the word "hola".
    """
    response = requests.post(CHAT_ENDPOINT, json={"user": "Hola"})
    response.raise_for_status()
    response_json = response.json()
    assert "assistant" in response_json
    assert "hola" in response_json["assistant"].lower()

def test_identity_chatbot():
    response = requests.post(CHAT_ENDPOINT, json={"user": "Hola, quien eres?"})
    response_json = response.json()
    assert "sesame" in response_json["assistant"].lower()


def test_check_memory():
    """
    Tests the assistant's memory capabilities.

    Sends a sequence of messages to the /chat endpoint:
    1. Introduces the user as "Josep".
    2. Asks the assistant to recall the user's name.
    Verifies that the assistant correctly remembers and responds with "Josep"
    """
    response = requests.post(CHAT_ENDPOINT, json={"user": "Hola, me llamo Josep"})
    response.raise_for_status()
    response = requests.post(CHAT_ENDPOINT, json={"user": "Cómo me llamo?"})
    response_json = response.json()
    assert "assistant" in response_json
    assert "Jose" in response_json["assistant"]

def test_addition():
    """
    Tests the assistant's ability to perform basic arithmetic.

    Sends a POST request to the /chat endpoint with the user's query
    "Cuánto es dos más dos" and verifies if the assistant's response contains
    the correct result ("4" or "cuatro").
    """
    response = requests.post(CHAT_ENDPOINT, json={"user": "Cuánto es dos más dos"})
    response.raise_for_status()
    response_json = response.json()
    assert "assistant" in response_json
    assert "4" in response_json["assistant"] or "cuatro" in response_json["assistant"].lower()

def test_check_memory_summary():
    response = requests.post(CHAT_ENDPOINT, json={"user": "Hola, me llamo Josep"})
    response.raise_for_status()
    response = requests.post(CHAT_ENDPOINT, json={"user": "Mi abuela se llama Tomasa"})
    response.raise_for_status()
    response = requests.post(CHAT_ENDPOINT, json={"user": "Mi tía se llama pepa"})
    response.raise_for_status()
    response = requests.post(CHAT_ENDPOINT, json={"user": "Hola, como me llamo? Como se llama mi abuela"
                                                          "Y como se llama mi tía?"})
    response_json = response.json()
    assert "assistant" in response_json
    assert "pepa" and "Jose" and "Tomasa" in response_json["assistant"].lower()



def test_empty_message():
    """
    Tests the assistant's response to an empty user message.

    Sends a POST request to the /chat endpoint with an empty message and
    verifies that the response contains the "assistant" key.
    """
    response = requests.post(CHAT_ENDPOINT, json={"user": ""})
    response.raise_for_status()
    assert "assistant" in response.json()

def test_wrong_format():
    """
    Tests the behavior of the /chat endpoint when an incorrect input format is used.

    Sends a POST request to the /chat endpoint with a JSON object that doesn't
    contain the "user" key and checks if the server returns a 422 Unprocessable
    Entity status code.
    """
    response = requests.post(CHAT_ENDPOINT, json={"assistant": "Hola que tal"})
    assert response.status_code == 422

def test_empty_json():
    """
    Tests the /chat endpoint with an empty JSON object.

    Sends a POST request to the /chat endpoint with an empty JSON body and verifies
    that the server returns a 422 Unprocessable Entity status code.
    """
    response = requests.post(CHAT_ENDPOINT, json={})
    assert response.status_code == 422


