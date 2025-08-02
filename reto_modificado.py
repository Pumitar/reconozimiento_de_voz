"""
Módulo de asistente virtual que cuenta chistes.

Este módulo implementa un asistente virtual simple que puede contar chistes
buenos o malos según la preferencia del usuario, utilizando reconocimiento
de voz para la interacción.
"""

import pyttsx3
import speech_recognition as sr
import random


# Lista de chistes organizados
chistes_buenos = [
    {
        "pregunta": "¿Por qué el asistente virtual rompió con su GPS?",
        "respuesta": "¡Porque siempre lo estaba llevando por mal camino!"
    },
    {
        "pregunta": "¿Por qué el robot fue a terapia?",
        "respuesta": "¡Porque tenía muchos circuitos cerrados.!"
    }
]


chistes_malos = [
    {
        "pregunta": "¿Qué hace un robot en la playa?",
        "respuesta": "¡Nada, porque se oxida!"
    },
    {
        "pregunta": "¿Qué hace un asistente virtual cuando se enamora?",
        "respuesta": "¡Empieza a procesar emociones.!"
    }
]


def hablar(texto):
    """
    Convierte texto a voz y lo reproduce.

    Args:
        texto (str): El texto que se desea convertir a voz.
    """
    motor = pyttsx3.init()
    motor.say(texto)
    motor.runAndWait()
    motor.stop()


def escuchar():
    """
    Captura audio del micrófono y lo convierte a texto.

    Returns:
        str: El texto reconocido del audio, o cadena vacía si hay error.
    """
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
    """
    Interpreta la respuesta del usuario para determinar si es afirmativa o negativa.

    Args:
        texto (str): El texto a interpretar.

    Returns:
        str: 'si' para respuesta afirmativa, 'no' para negativa,
             'respuesta no válida' para otros casos.
    """
    texto = texto.lower()
    if (any(palabra in texto for palabra in ["afirmativo", "sí", "si"]) or
            texto in ["sí", "si"]):
        return "si"
    elif "negativo" in texto or texto == "no" or "no" in texto:
        return "no"
    return "respuesta no válida"


def get_chiste(rsp):
    """
    Selecciona un chiste aleatorio basado en la respuesta del usuario.

    Args:
        rsp (str): La respuesta interpretada del usuario ('si', 'no' u otro).

    Returns:
        tuple: (respuesta, chiste)
            - respuesta (str): El mensaje de introducción al chiste
            - chiste (dict): Diccionario con la pregunta y respuesta del chiste
    """
    chiste = {}
    if rsp == "si":
        respuesta = "bien, te contare un chiste bueno. Aqui va..."
        chiste = random.choice(chistes_buenos)
    elif rsp == "no":
        respuesta = "oh... igual te lo contare. Aqui va..."
        chiste = random.choice(chistes_malos)
    else:
        respuesta = "no entendi tu respuesta"
    return respuesta, chiste


def main():
    """
    Función principal que ejecuta el asistente virtual.
    
    Lista los dispositivos de audio disponibles y ejecuta el flujo principal
    del programa: saluda, pregunta si quiere un chiste, escucha la respuesta
    y cuenta el chiste correspondiente.
    """
    # Mostrar dispositivos de audio disponibles
    for i, mic in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{i}: {mic}")

    # Hablar primero
    frase_inicial = "Hola, soy Sabina, tu asistente virtual"
    hablar(frase_inicial)

    frase_secundaria = "¿Quieres que te cuente un chiste?"
    hablar(frase_secundaria)

    # Reconocimiento
    rsp = escuchar()
    rsp = interpretar_respuesta(rsp)

    # Obtener y contar el chiste
    respuesta, chiste = get_chiste(rsp)
    if chiste:  # Verificar que el chiste existe
        hablar(respuesta)
        chiste_pregunta = chiste.get("pregunta")
        chiste_respuesta = chiste.get("respuesta")
        if chiste_pregunta:
            hablar(chiste_pregunta)
        if chiste_respuesta:
            hablar(chiste_respuesta)
    else:
        hablar("Lo siento, hubo un error al contar el chiste")


if __name__ == "__main__":
    main()
