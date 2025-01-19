from langchain_core.messages import SystemMessage, RemoveMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph import START, StateGraph, END

from prompts.chatbot_prompts import LAST_CONVERSATIONS_MSG, INITIAL_MSG_FIRST_STATE_TRUE
from services.memory import MemoryService


class ChatbotService:
    """
    A class that represents a chatbot service. This class handle the chatbot state and interaction workflows.
    This class incorporates an LLM to process and summarize the conversation.
    """

    class State(MessagesState):
        """
        Represents the state of the chatbot during a conversation.
        summary (str): A summary of the conversation.
        is_first_state (bool): A flag indicating if this is the initial state of the conversation.
        """
        summary: str
        is_first_state: bool

    def __init__(self):
        """
        Initialize the LLM
        """
        self.llm = ChatOpenAI()

    def build_graph(self):
        """
        Builds a state graph that defines the chatbot's workflow.
        :return: A compiled graph of states and transitions for managing the chatbot's behavior.
        """
        builder = StateGraph(ChatbotService.State)

        builder.add_node("chatbot", self._call_model)
        builder.add_node(self._summarize)

        builder.add_edge(START, "chatbot")
        builder.add_conditional_edges("chatbot", self._select_summarize)
        builder.add_edge("_summarize", END)
        react_graph = builder.compile(checkpointer=MemoryService().memory)

        return react_graph

    def _call_model(self, state: State):
        """
        Invokes the language model to process the current conversation state.
        :param state: the current conversation state.
        :return: Updated state containing whether it's the first state and the new messages from the model.
        """

        is_first_state = state.get("is_first_state", True)
        if is_first_state:
            initial_message = SystemMessage(content=INITIAL_MSG_FIRST_STATE_TRUE)

            state["messages"] = [initial_message] + state["messages"]
            state["is_first_state"] = False

        summary = state.get("summary", "")

        if summary:
            system_message = f'Summary of the conversation earlier: {summary}'
            messages = [SystemMessage(content=system_message)] + state["messages"]
        else:
            messages = state["messages"]

        response = self.llm.invoke(messages)

        return {"is_first_state": True, "messages": response}

    def _summarize(self, state: State):
        """
        Summarizes the current conversation and removes old messages.
        :param state: the current conversation state.
        :return: Updated state containing the summary and cleaned-up messages.
        """
        summary = state.get("summary", "")
        if summary:
            summary_message = LAST_CONVERSATIONS_MSG.format(summary=summary)
        else:
            summary_message = ("Please summarize the conversation above. Take account all the information. "
                               "Don´t act like an assistant, just summarize")

        messages = state["messages"] + [SystemMessage(content=summary_message)]
        response = self.llm.invoke(messages)
        delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]

        return {"summary": response.content, "messages": delete_messages}

    @staticmethod
    def _select_summarize(state: State):
        """
        Determines whether to transition to the summarization state based on the number of messages.

        :param state: the current conversation state.
        :return: The name of the next state ("_summarize" or END).
        """
        messages = state["messages"]
        if len(messages) > 4:
            return "_summarize"

        return END
