import speech_recognition as sr
import pyttsx3
import webbrowser as sub
import datetime
import random

from information import information
from machines import machines
from diet import diet


class assistant:

    """
    Clase que representa a Alexa, un asistente virtual en Python.

    Attributes:
        name (str): El nombre del asistente.
        listener (Recognizer): El reconocedor de voz.
        engine (pyttsx3.Engine): El motor de texto a voz.
        voice (pyttsx3.Voice): La voz utilizada por el motor de texto a voz.
        conversation (list): Almacena la conversación actual.
    """

    def __init__(self):
        self.name = "alexa"
        self.listener = sr.Recognizer()

        self.engine = pyttsx3.init()
        self.voice = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voice[0].id)
        self.engine.setProperty('rate', 150)
        self.is_listening = True
        self.talk(f'¿Gym de la UPC?')
        

    """
    Convierte un texto en voz y lo reproduce.
    Args:
        text (str): El texto a convertir y reproducir.
    """
    def talk(self, text): 
        self.engine.say(text)
        self.engine.runAndWait()

    """
    Escucha el audio del micrófono y reconoce el texto.
    Returns:
        str: El texto reconocido.
    """

    def listen(self):
        rec = ""
        try:
            with sr.Microphone() as source:
                self.listener.adjust_for_ambient_noise(source, duration=4)
                self.talk("Escuchando...")
                print("Escuchando...")
                voice = self.listener.listen(source) 
                rec = self.listener.recognize_google(voice, language="es-ES")
                print("Texto reconocido:", rec)
                rec = rec.lower()
                
                if self.name in rec:
                    # talk(rec) 
                    rec = rec.replace(self.name, '')
                    print(rec)

        except sr.UnknownValueError:
            self.talk("Vuelve a intentarlo")
        except sr.RequestError as e:
            print(f"Error en la solicitud a la API de Google: {e}")
        except Exception as e:
            print(f"Error inesperado al escuchar: {e}")

        return rec

    """
    Ejecuta las acciones basadas en el texto reconocido por el asistente.
    """
    def run(self):
        while self.is_listening:
            rec = self.listen()
            actions = {
                'terminar asistente': self.terminate_assistant,
                'finalizar': self.terminate_assistant,
                'detener': self.terminate_assistant,
                'registrarse': self.open_website,
                'registrar': self.open_website,
                'inscribirse': self.open_website,
                'inscribir': self.open_website,
                'hora': self.get_current_time,
                'gracias': self.respond_to_thanks,
                'información': self.set_Intro,
                'secciones': self.set_Secciones,
                'máquina': self.set_Machies,
                'mancuernas': self.set_Machies,
                'dieta': self.alimentos,
                'peso': self.alimentos,
                'comidas':self.alimentos
            }

            for keyword, action in actions.items():
                if keyword in rec:
                    action(rec)
                    break

    

    def open_website(self, rec):
        self.talk(f'Pasos para inscripcion del gimnasio.' )
        self.talk(f'1. Debe registrarse con el correo intitucional.')
        self.talk(f'2. Selecionar el día y horario que mas le convenga.')
        self.talk(f'3. Debes llenar el formulario cinco veces, uno por cada día de la semana de lunes a viernes.')

        sub.open('https://form.jotform.com/232703905549056')
        self.talk(f'Abriendo pagina de inscripcion' )

    def get_current_time(self, rec):
        hora = datetime.datetime.now().strftime('%I:%M %p')
        self.talk("Son las " + hora)


    def respond_to_thanks(self, rec):
        self.talk("Con mucho gusto")

    def set_Intro(self, rec):
        if 'introducción' in rec or 'información' in rec:
            intro_info = information.get('introducción', {'texto': 'La introducción no está disponible.',})
            self.talk(intro_info['texto'])

    def set_Secciones(self, rec):
        if 'secciones' in rec:
            secciones_text = information.get('secciones', 'La información de secciones no está disponible.')
            self.talk(secciones_text['texto'])

    def set_Machies(self, rec):
        machine_keywords = {
            'extensión': 'MÁQUINA EXTENSIÓN Y CURL DE PIERNAS',
            'cabina doble': 'MAQUINA CABINA DOBLE FUNCION PARA GIMNASIO',
            'polea alta y baja': 'MAQUINA POLEA ALTA Y BAJA',
            'prensa de piernas inclinada':'MAQUINA PIERNAS EN PRENSA EN VERTICAL INCLINADA',
            'prensa de piernas': 'MAQUINA PRENSA DE PIERNAS',
            'pecho plano': 'MAQUINA PECHO PLANO PARA DISCO OLIMPICO',
            'remo': 'MAQUINA SOPORTE BARRA REMO',
            'banco abdominal':'MAQUINA BANCO ABDOMINAL AÉREO Y FONDOS',
            'smith':'MAQUINA SMITH',
            'dorsalera':'MÁQUINA DORSALERA O DE JALÓN A PECHO',
            'jalón a pecho':'MÁQUINA DORSALERA O DE JALÓN A PECHO',
            'pantorrillas':'MAQUINA PARA PANTORRILLAS',
            'multifunción':'MÁQUINAS MULTIFUNCIÓN',
            'banco olímpico':'MÁQUINA DE BANCO OLÍMPICO',
            'banco':'MÁQUINA DE BANCO OLÍMPICO',
            'mancuernas':'MANCUERNAS',
            'pesas':'MANCUERNAS',
            'elíptica':'MAQUINA ELÍPTICA',
            'stepper':'MAQUINA STEPPER',
            'escaladora':'MAQUINA STEPPER',
            'bicicleta':'MAQUINA BICICLETA ESTÁTICA',
            'bicicleta estática':'MAQUINA BICICLETA ESTÁTICA',
            'cinta de correr':'MAQUINA CINTA DE CORRER',
            'caminadora':'MAQUINA CINTA DE CORRER'

        }

        if 'cuántas máquinas' in rec or 'número' in rec:
            self.talk(f"Hay {len(machines)} máquinas en total.")

        # Cuando pregunta qué máquinas hay
        elif 'qué máquinas' in rec or 'nombres' in rec:
            machine_names = list(machines.keys())
            self.talk(f"Las máquinas disponibles son: {', '.join(machine_names)}")

        # Cuando se menciona una máquina específica
        else:         
            for keyword, machine_name in machine_keywords.items():
                if keyword in rec:
                    machine_info = machines.get(machine_name, 'La información de esta máquina no está disponible.')
                    # img=machine_info['imagen']
                    self.talk(machine_name)
                    self.talk(machine_info['texto'])
                    
                    self.talk("Mostrando imagen de la máquina.")
                    # img = machine_info['imagen']
                    url = machine_info['url']
                    sub.open(url)
                    # return img
                    
                    break
            else:
                self.talk("No se encontró información para esa máquina.")
                self.talk("o no pronuncio bien la máquina.")

    def alimentos(self, rec):

        if 'insuficiente' in rec:
            diet_insuficiente = diet["insuficiente"]["dietInsuficiente"]

            def generar_dieta_aleatoria():
                # return random.sample(diet_insuficiente, k=random.randint(5, 10))
                return random.sample(diet_insuficiente, k=3)

            # Generar una dieta aleatoria
            dieta_generada = generar_dieta_aleatoria()

            # Mostrar la dieta generada
            self.talk("Aquí tienes una dieta para personas con peso insuficiente:")
            for alimento in dieta_generada:
                self.talk(alimento)
        
        if 'saludable' in rec:
            diet_saludable = diet["saludable"]["dietSaludable"]

            def generar_dieta_aleatoria():
                return random.sample(diet_saludable, k=4)

            # Generar una dieta aleatoria
            dieta_generada = generar_dieta_aleatoria()

            # Mostrar la dieta generada
            self.talk("Aquí tienes una dieta para personas con peso saludable:")
            for alimento in dieta_generada:
                self.talk(alimento)

        if 'sobrepeso' in rec or 'obeso' in rec:
            diet_sobrepeso = diet["sobrepeso"]["dietSobrepeso"]

            def generar_dieta_aleatoria():
                return random.sample(diet_sobrepeso, k=1)  # Ajusta el número de alimentos según sea necesario

            # Generar una dieta aleatoria
            dieta_generada = generar_dieta_aleatoria()

            # Mostrar la dieta generada
            self.talk("Aquí tienes una dieta para personas con sobrepeso u obesidad:")
            for alimento in dieta_generada:
                self.talk(alimento)
        

        else: 
            self.talk("Que dieta quieres saber")
            self.talk("peso insuficiente")
            self.talk("peso saludable ")
            self.talk("sobrepeso")
            self.talk("obeso")


    def terminate_assistant(self, rec):
        self.talk("Terminando asistente")
        self.is_listening = False  # Establece la bandera en False para salir del bucle de escucha
        return
    
class Imagenes:
    def __init__(self):
        self.img = "MF2.png"

    def send_image(self, new_image):
        self.img = new_image
        return self.img

    def get_current_image(self):
        return self.img

    def run(self, new_image="MF2.png"):
        return self.send_image(new_image)

class ICM:
    @staticmethod
    def Calcular(altura, peso):
        # Realizar los cálculos del IMC aquí
        imc = peso / (altura ** 2)
        assistant = assistant()
        if imc < 18.5:
            assistant.talk("Peso insuficiente (IMC inferior a 18.5)")
            assistant.talk("Objetivo: Ganar masa muscular y fortalecer el cuerpo.")
            assistant.talk("Recomendación de máquinas y ejercicios:")
            assistant.talk("Máquina Extensión y Curl de Piernas: Trabajar cuádriceps y femorales. Máquina Pecho Plano para Disco Olímpico: Fortalecer el pecho. Mancuernas: Ejercicios variados para el cuerpo completo. Máquina Polea Alta y Baja: Ejercicios para brazos y espalda.")

        elif imc >= 18.5 and imc <= 24.9:
            assistant.talk("Peso saludable (IMC entre 18.5 y 24.9)")
            assistant.talk("Objetivo: Mantener la forma física y la salud en general.")
            assistant.talk("Recomendación de máquinas y ejercicios:")
            assistant.talk("Máquina Cabina Doble Función para Gimnasio: Fortalecer el tren superior (pecho y hombros). Máquina Smith: Ejercicios compuestos para grupos musculares grandes. Máquina de Banco Olímpico: Ejercicios de press de banca para el torso.")
            
        elif imc >= 25 and imc <= 29.9:
            assistant.talk("Sobrepeso (IMC entre 25 y 29.9)")
            assistant.talk("Objetivo: Quemar grasa, tonificar y fortalecer el cuerpo.")
            assistant.talk("Recomendación de máquinas y ejercicios:")
            assistant.talk("Máquina Press de Piernas: Trabajar cuádriceps, glúteos e isquiotibiales. Máquina de Polea Alta y Baja: Ejercicios para brazos y espalda. Máquina Bicicleta Estática: Ejercicio cardiovascular de baja intensidad.")

        else:
            assistant.talk("Obeso (IMC 30 o más)")
            assistant.talk("Objetivo: Reducir grasa corporal, mejorar la salud cardiovascular y fortalecer el cuerpo.")
            assistant.talk("Recomendación de máquinas y ejercicios:")
            assistant.talk("Máquina Prensa de Piernas: Trabajar piernas de manera integrada. Máquina de Cinta de Correr: Ejercicio cardiovascular para quemar calorías. Máquina Elíptica: Entrenamiento cardiovascular de bajo impacto.")


        return imc
