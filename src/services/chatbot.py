from langchain_core.messages import SystemMessage, RemoveMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph import START, StateGraph, END

from const.prompts import LAST_CONVERSATIONS_MSG, INITIAL_MSG_FIRST_STATE_TRUE
from services.memory import MemoryService


class ChatbotService:
    # TODO: Docstrings

    class State(MessagesState):
        # TODO: Docstrings
        summary: str
        is_first_state: bool

    def __init__(self):
        # TODO: Docstrings
        self.llm = ChatOpenAI()

    def build_graph(self):
        # TODO: Docstrings
        builder = StateGraph(ChatbotService.State)

        builder.add_node("chatbot", self._call_model_stream)
        builder.add_node(self._summarize)

        builder.add_edge(START, "chatbot")
        builder.add_conditional_edges("chatbot", self._select_summarize)
        builder.add_edge("_summarize", END)
        react_graph = builder.compile(checkpointer=MemoryService().memory)

        return react_graph

    def _call_model_stream(self, state: State, config: RunnableConfig):
        # TODO: Docstrings
        is_first_state = state.get("is_first_state", True)
        if is_first_state:
            initial_message = SystemMessage(content=INITIAL_MSG_FIRST_STATE_TRUE)

            state["messages"] = [initial_message] + state["messages"]
            state["is_first_state"] = False

        messages = state["messages"]
        response = self.llm.invoke(messages, config)

        return {"messages": response}

    def _call_model_not_stream(self, state: State):
        # TODO: Docstrings
        is_first_state = state.get("is_first_state", True)
        if is_first_state:
            initial_message = SystemMessage(content=INITIAL_MSG_FIRST_STATE_TRUE)

            state["messages"] = [initial_message] + state["messages"]
            state["is_first_state"] = False

        messages = state["messages"]
        response = self.llm.invoke(messages)

        return {"messages": response}

    def _summarize(self, state: State):
        # TODO: Docstrings
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
        # TODO: Docstrings
        messages = state["messages"]
        if len(messages) > 4:
            return "_summarize"

        return END
