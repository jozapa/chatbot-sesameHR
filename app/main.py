from services.chatbot import ChatbotService
from langchain_core.messages import HumanMessage
from services.memory import MemoryService
from dotenv import load_dotenv
load_dotenv()

from IPython.display import Image, display

def main():
    # Crear una instancia del servicio del chatbot
    chatbot_service = ChatbotService()
    


    # Construir el grafo de conversación
    react_graph = chatbot_service._build_graph()

    png_data = react_graph.get_graph(xray=True).draw_mermaid_png()
    with open("output.png", "wb") as f:
        f.write(png_data)


    print("SesameBot: ¡Hola! Soy SesameBot, tu asistente virtual. Hazme una pregunta para empezar. 😊")

    while True:
        # Leer la entrada del usuario
        user_input = input("Tú: ")
        input_message = HumanMessage(content=user_input)
        response = react_graph.invoke({"messages":[input_message]}, MemoryService().config)
        print(response['messages'][-1].content)


if __name__ == "__main__":
    main()










# 


# graph = ChatbotService()._build_graph()



# # Opcional: Mostrar la imagen guardada
# display(Image("output.png"))