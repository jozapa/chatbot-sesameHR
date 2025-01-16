from services.chatbot import ChatbotService
from langchain_core.messages import HumanMessage
from services.memory import MemoryService
from dotenv import load_dotenv
load_dotenv()
import asyncio

from IPython.display import Image, display

async def main_stream():
    # Crear una instancia del servicio del chatbot
    chatbot_service = ChatbotService()
    


    # Construir el grafo de conversación
    react_graph = chatbot_service._build_graph_stream()

    # png_data = react_graph.get_graph(xray=True).draw_mermaid_png()
    # with open("output.png", "wb") as f:
    #     f.write(png_data)


    print("SesameBot: ¡Hola! Soy SesameBot, tu asistente virtual. Hazme una pregunta para empezar. 😊")

    while True:
        # Leer la entrada del usuario
        user_input = input("Tú: ")
        input_message = HumanMessage(content=user_input)
        #response = react_graph.astream_events({"messages":[input_message]}, MemoryService().config, version="v2")
        async for event in react_graph.astream_events(
            {"messages": [input_message]}, 
            MemoryService().config, 
            version="v2"):
            if event["event"] == "on_chat_model_stream" and event['metadata'].get('langgraph_node','') == "chatbot":
                print(event["data"])
            #print(f"Node: {event['metadata'].get('langgraph_node','')}. Type: {event['event']}. Name: {event['name']}")
        #print(response['messages'][-1].content)
                
def main_not_stream():
    # Crear una instancia del servicio del chatbot
    chatbot_service = ChatbotService()
    


    # Construir el grafo de conversación
    react_graph = chatbot_service._build_graph_not_stream()

    # png_data = react_graph.get_graph(xray=True).draw_mermaid_png()
    # with open("output.png", "wb") as f:
    #     f.write(png_data)


    # print("SesameBot: ¡Hola! Soy SesameBot, tu asistente virtual. Hazme una pregunta para empezar. 😊")

    while True:
        # Leer la entrada del usuario
        user_input = input("Tú: ")
        input_message = HumanMessage(content=user_input)
        response = react_graph.invoke({"messages":[input_message]}, MemoryService().config)
        print(response['messages'][-1].content)


if __name__ == "__main__":
    streaming = False
    if streaming:
        asyncio.run(main_stream())
    else:
        main_not_stream()










# 


# graph = ChatbotService()._build_graph()



# # Opcional: Mostrar la imagen guardada
# display(Image("output.png"))