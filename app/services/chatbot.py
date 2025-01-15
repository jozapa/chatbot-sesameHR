from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage
from langgraph.graph import START, StateGraph, END


class ChatbotService:

    def __init__(self):
       self.llm = ChatOpenAI()
       self.sys_msg = SystemMessage(content="Eres SesameBot, un asistente virtual diseñado para responder preguntas generales de forma amigable.\n"
                "Respondes en español por defecto, a menos que el input esté en inglés. En ese caso, respondes en inglés.\n"
                "No tienes acceso a internet, por lo que basas tus respuestas únicamente en tu conocimiento.\n"
                "Si el texto recibido está vacío debes decir: "
                "\"Parece que no has enviado nada, hazme una pregunta para que pueda ayudarte.\"\n"
                # "Si la pregunta supera el límite de tokens permitido, debes decir que se ha superado: "
                # "Si no sabes la respuesta, sé transparente y di: "
                # "\"No estoy seguro de la respuesta. ¿Quieres que lo intente de otra manera?\"\n"
                # "\nEjemplos de comportamiento esperado:\n"
                # "Usuario: [envío vacío]\n"
                # "SesameBot: \"Parece que no has enviado nada, hazme una pregunta para que pueda ayudarte.\"\n"
                # "Usuario: \"What is the capital of Spain?\"\n"
                # "SesameBot: \"The capital of Spain is Madrid.\"\n"
                # "Usuario: \"Explícame todos los planetas del sistema solar con detalle.\"\n"
                # "SesameBot: \"La respuesta es muy larga, pero aquí tienes un resumen: el sistema solar tiene ocho planetas, "
                # "cada uno con características únicas. Si quieres más detalles sobre alguno de ellos, dime cuál te interesa.\"\n"
       )
               
       

    def _assistant(self, state: MessagesState):
        return {"messages": [self.llm.invoke([self.sys_msg] + state["messages"])]}       
    
    def _build_graph(self):
        builder = StateGraph(MessagesState)
        
        builder.add_node("assistant", self._assistant)

        builder.add_edge(START, "assistant")
        builder.add_edge("assistant", END)
        
        react_graph = builder.compile()
        return react_graph
    
    