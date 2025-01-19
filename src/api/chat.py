from services.chatbot import ChatbotService
from services.memory import MemoryService
from langchain_core.messages import HumanMessage


class Assistant:
    """
    Represents an AI assistant that generates responses to users using a chatbot with memory
    configuration.
    """

    def __init__(self):
        """
        Initialize the Assistant class. Involves building the react graph and memory service config.
        """
        chatbot_service = ChatbotService()
        self.react_graph = chatbot_service.build_graph()
        self.memory_service_config = MemoryService().config

    def generate_response(self, user_message: str) -> str:
        """
        Generate the response for a given response.

        The method takes a user message as an input, invokes the react graph with the configured memory
        and returns the AI response.

        :param user_message: the input message from the user
        :return: the AI response from the assistant
        """
        input_message = HumanMessage(content=user_message)
        response_metadata = self.react_graph.invoke({"messages": [input_message]}, self.memory_service_config)
        return response_metadata['messages'][-1].content
