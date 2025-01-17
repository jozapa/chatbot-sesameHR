from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from services.chatbot import ChatbotService
from services.memory import MemoryService


class UserInput(BaseModel):
    user: str


class AssistantResponse(BaseModel):
    assistant: str


class Assistant:
    def __init__(self):
        chatbot_service = ChatbotService()
        self.react_graph = chatbot_service.build_graph()
        self.memory_service_config = MemoryService().config

    def generate_response(self, user_message: str) -> str:
        input_message = HumanMessage(content=user_message)
        response_metadata = self.react_graph.invoke({"messages": [input_message]}, self.memory_service_config)
        return response_metadata['messages'][-1].content


load_dotenv()
assistant = Assistant()
app = FastAPI()


def get_assistant() -> Assistant:
    return assistant


@app.post("/chat", response_model=AssistantResponse)
async def generate_response_endpoint(user_request: UserInput):
    assistant_message = assistant.generate_response(user_request.user)
    return AssistantResponse(assistant=assistant_message)


# Endpoint GET /health
@app.get("/health")
async def health():
    return {"health": "healthy"}
