from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langgraph.graph import START, StateGraph, END
from services.memory import MemoryService
from langchain_core.runnables import RunnableConfig

class ChatbotService:

    class State(MessagesState):
        summary: str

    def __init__(self):
       self.llm = ChatOpenAI()
    #    self.sys_msg = SystemMessage(content="Eres SesameBot, un asistente virtual diseñado para responder preguntas generales de forma amigable.\n"
    #             "Respondes en español por defecto, a menos que el input esté en inglés. En ese caso, respondes en inglés.\n"
    #             "No tienes acceso a internet, por lo que basas tus respuestas únicamente en tu conocimiento.\n"
    #             "Si el texto recibido está vacío debes decir: "
    #             "\"Parece que no has enviado nada, hazme una pregunta para que pueda ayudarte.\"\n"
    #             # "Si la pregunta supera el límite de tokens permitido, debes decir que se ha superado: "
    #             # "Si no sabes la respuesta, sé transparente y di: "
    #             # "\"No estoy seguro de la respuesta. ¿Quieres que lo intente de otra manera?\"\n"
    #             # "\nEjemplos de comportamiento esperado:\n"
    #             # "Usuario: [envío vacío]\n"
    #             # "SesameBot: \"Parece que no has enviado nada, hazme una pregunta para que pueda ayudarte.\"\n"
    #             # "Usuario: \"What is the capital of Spain?\"\n"
    #             # "SesameBot: \"The capital of Spain is Madrid.\"\n"
    #             # "Usuario: \"Explícame todos los planetas del sistema solar con detalle.\"\n"
    #             # "SesameBot: \"La respuesta es muy larga, pero aquí tienes un resumen: el sistema solar tiene ocho planetas, "
    #             # "cada uno con características únicas. Si quieres más detalles sobre alguno de ellos, dime cuál te interesa.\"\n"
    #    )
               
       

    # # def _assistant(self, state: MessagesState):
    # #     return {"messages": [self.llm.invoke([self.sys_msg] + state["messages"])]}       
    
    def _build_graph_stream(self):
        builder = StateGraph(self.State)
        
        builder.add_node("chatbot", self._call_model_stream)
        builder.add_node(self._summarize)

        builder.add_edge(START, "chatbot")
        builder.add_conditional_edges("chatbot", self._select_summarize)
        builder.add_edge("_summarize", END)
        
        react_graph = builder.compile(checkpointer=MemoryService().memory)
        return react_graph
    
    def _build_graph_not_stream(self):
        builder = StateGraph(self.State)
        
        builder.add_node("chatbot", self._call_model_not_stream)
        builder.add_node(self._summarize)

        builder.add_edge(START, "chatbot")
        builder.add_conditional_edges("chatbot", self._select_summarize)
        builder.add_edge("_summarize", END)
        
        react_graph = builder.compile(checkpointer=MemoryService().memory)
        return react_graph
    
    def _call_model_stream(self, state: State, config: RunnableConfig):
        #print(state, "glhnldsakhgjalsdg")
        is_first_state = state.get("is_first_state", True)
        #print(is_first_state)
        if is_first_state:
            initial_message = SystemMessage(content="Eres SesameBot, un asistente virtual diseñado para responder preguntas generales de forma amigable.\n"
                "Respondes en español por defecto, a menos que el input esté en inglés. En ese caso, respondes en inglés.\n"
                "No tienes acceso a internet, por lo que basas tus respuestas únicamente en tu conocimiento.\n"
                "Si el texto recibido está vacío debes decir: "
                "\"Parece que no has enviado nada, hazme una pregunta para que pueda ayudarte.\"\n")

            state["messages"] = [initial_message] + state["messages"]
            state["is_first_state"] = False

        summary = state.get("summary", "")
        #print(summary, "Aaaaaaaaaaaa")

        if summary:
            system_message = f'Summary of the conversation earlier: {summary}'

            messages = [SystemMessage(content=system_message)] + state["messages"]
        else: 
            messages = state["messages"]

        response = self.llm.invoke(messages, config)
        return {"messages": response}
    def _call_model_not_stream(self, state: State):
        #print(state, "glhnldsakhgjalsdg")
        is_first_state = state.get("is_first_state", True)
        #print(is_first_state)
        if is_first_state:
            initial_message = SystemMessage(content="Eres SesameBot, un asistente virtual diseñado para responder preguntas generales de forma amigable.\n"
                "Respondes en español por defecto, a menos que el input esté en inglés. En ese caso, respondes en inglés.\n"
                "No tienes acceso a internet, por lo que basas tus respuestas únicamente en tu conocimiento.\n"
                "Si el texto recibido está vacío debes decir: "
                "\"Parece que no has enviado nada, hazme una pregunta para que pueda ayudarte.\"\n")

            state["messages"] = [initial_message] + state["messages"]
            state["is_first_state"] = False

        summary = state.get("summary", "")
        #print(summary, "Aaaaaaaaaaaa")

        if summary:
            system_message = f'Summary of the conversation earlier: {summary}'

            messages = [SystemMessage(content=system_message)] + state["messages"]
        else: 
            messages = state["messages"]

        response = self.llm.invoke(messages)
        return {"messages": response}
    
    def _summarize(self, state: State):

        summary = state.get("summary", "")

        if summary:
            #print(summary, "DEBERIA ENTRAR AQUI EN ALGUN MOMENTO")
            #print("entra en summary")
            summary_messge = (
                f"This the summary of the last conversations: {summary}\n\n"
                "Your mission is to create a summary by takig account the new messages above and the previous summary:\n"
                "Take account all the information\n"
                "Don´t act like an assistant, just summarize"
            )
        
        else:
            summary_messge = "Please summarize the conversation above. Take account all the information. Don´t act like an assistant, just summarize"

        #print(state["messages"], "asdflañsdjfñlasdjf")
        messages = state["messages"] + [SystemMessage(content=summary_messge)]
        #print(messages, "VAMOS A VER SI ESTO VA")
        response = self.llm.invoke(messages)
        #print({"summary": response.content}, "AAAAAA ESTE ES EL SUMMARY")
        delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]

        return {"summary": response.content, "messages": delete_messages}
    

    
    def _select_summarize(self, state: State):
        #print(state, "fffff")
        messages = state["messages"]
        #print("entra en select summarize")
        #print(len(messages))
        if len(messages) > 4:
            return "_summarize"
        
        return END