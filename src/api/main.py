from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from api.chat import Assistant

# Load the OpenAI api key
load_dotenv()

# Initialize the assistant.
assistant = Assistant()

# Initialize the FastAPI app.
app = FastAPI()


class UserInput(BaseModel):
    """
    Represents the structure of a user message sent to the chat API
    """
    user: str


class AssistantResponse(BaseModel):
    """
    Represents the structure of the assistant´s response send back to the client (user)
    """
    assistant: str


def get_assistant() -> Assistant:
    """
    Retrieves the initialized assistant instance.
    :return: the global Assistant instance
    """
    return assistant


@app.post("/chat", response_model=AssistantResponse)
async def generate_response_endpoint(user_request: UserInput):
    """
    Handles the /chat POST endpoint to process user input and generate a response.

    The endpoint takes a UserInput object as input message, processes it through the assistant
    and returns the generated response.

    :param user_request: the user request message wrapped in the UserInput.
    :return: The assistant response wrapped in the AssistantResponse.
    """
    assistant_message = assistant.generate_response(user_request.user)
    return AssistantResponse(assistant=assistant_message)


@app.get("/health")
async def health():
    """
    Handles the /health GET endpoint to check the application's health status.

    This endpoint is used to verify that the service is running.

    :return: the health status of the application.
    """
    return {"health": "healthy"}
