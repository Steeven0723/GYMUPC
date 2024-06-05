from assistant import assistant

"""
Función principal que crea una instancia de AlexaAssistant y maneja la interacción con el usuario.
"""
def main():
    Assistant = assistant()
    Assistant.talk("¿en qué puedo ayudarte?")
    #assistant.talk("Soy Alexa, tu asistente virtual que desarrollas en Python.")

    Assistant.run()
        

if __name__ == "__main__":
    main()
    