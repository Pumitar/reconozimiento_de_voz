import pyttsx3
import speech_recognition as sr
import random

chistes_buenos = [{"pregunta": "¿Por qué el asistente virtual rompió con su GPS?", "respuesta": "¡Porque siempre lo estaba llevando por mal camino!"}, {
    "pregunta": "¿Por qué el robot fue a terapia?", "respuesta": "¡Porque tenía muchos circuitos cerrados.!"}]
chistes_malos = [{"pregunta": "¿Qué hace un robot en la playa?", "respuesta": "¡Nada, porque se oxida!"}, {
    "pregunta": "¿Qué hace un asistente virtual cuando se enamora?", "respuesta": "¡Empieza a procesar emociones.!"}]

def hablar(texto):
    motor = pyttsx3.init()
    motor.say(texto)
    motor.runAndWait()
    motor.stop()


def escuchar():
    mic = sr.Microphone(device_index=2)
    recog = sr.Recognizer()

    with mic as audio_file:
        print("Por favor, hable")
        recog.adjust_for_ambient_noise(audio_file, duration=2)

        try:
            audio = recog.listen(audio_file, phrase_time_limit=4)
            text = recog.recognize_google(audio, language="es-ES")
            print("Usted dijo:", text)
            return text
        
        except sr.UnknownValueError:
            print("No se entendió lo que dijo.")
            return ""
        
        except sr.RequestError as e:
            print("Error al conectar con el servicio:", e)
            return ""

def interpretar_respuesta(texto):
    texto = texto.lower()
    if "afirmativo" in texto or texto in ["sí", "si"] or "sí" in texto or "si" in texto:
        return "si"
    elif "negativo" in texto or texto == "no" or "no" in texto:
        return "no"
    else:
        return "respuesta no válida"

def get_chiste(rsp):
    chiste = {}
    if rsp == "si":
        respuesta = "bien, te contare un chiste bueno. Aqui va...."
        chiste = random.choice(chistes_buenos)

    elif rsp == "no":
        respuesta = "oh.., igual te lo contare. Aqui va...."
        chiste = random.choice(chistes_malos)

    else:
        respuesta = "no entendi tu respuesta"
        
    return respuesta, chiste


for i, mic in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{i}: {mic}")



# Hablar primero
frase_inicial = "Hola, soy Sabina, tu asistente virtual"
hablar(frase_inicial)

frase_secundaria = "Quieres que te cuente un chiste?"
hablar(frase_secundaria)

#reconocimiento
rsp = escuchar()
rsp = interpretar_respuesta(rsp)

# opciones
respuesta, chiste = get_chiste(rsp)
chiste_pregunta = chiste.get("pregunta")
chiste_respuesta = chiste.get("respuesta")

hablar(respuesta)
hablar(chiste_pregunta)
hablar(chiste_respuesta)


