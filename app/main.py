from services.chatbot import ChatbotService
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()



def main():
    # Crear una instancia del servicio del chatbot
    chatbot_service = ChatbotService()

    # Construir el grafo de conversación
    react_graph = chatbot_service._build_graph()


    print("SesameBot: ¡Hola! Soy SesameBot, tu asistente virtual. Hazme una pregunta para empezar. 😊")

    while True:
        # Leer la entrada del usuario
        user_input = input("Tú: ")
        messages = [HumanMessage(content=user_input)]
        messages = react_graph.invoke({"messages":messages})
        print(messages)


if __name__ == "__main__":
    main()










# from IPython.display import Image, display


# graph = ChatbotService()._build_graph()

# png_data = graph.get_graph(xray=True).draw_mermaid_png()
# with open("output.png", "wb") as f:
#     f.write(png_data)

# # Opcional: Mostrar la imagen guardada
# display(Image("output.png"))