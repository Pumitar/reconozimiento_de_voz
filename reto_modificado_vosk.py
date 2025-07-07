import pyttsx3
import vosk
import sounddevice as sd
import queue
import json
import random

# Inicializa el modelo solo una vez
modelo = vosk.Model("modelos/modelo-es")  # Cambia la ruta si está en otro lado
samplerate = 16000  # Frecuencia estándar

# Cola de audio
audio_q = queue.Queue()

def callback(indata, frames, time, status):
    audio_q.put(bytes(indata))

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
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("Por favor, hable (Vosk)...")
        rec = vosk.KaldiRecognizer(modelo, samplerate)

        texto_detectado = ""
        segundos_maximos = 4
        bloques = int(samplerate / 8000 * segundos_maximos)  # bloques de 0.5s

        for _ in range(bloques):
            data = audio_q.get()
            if rec.AcceptWaveform(data):
                resultado = json.loads(rec.Result())
                texto_detectado = resultado.get("text", "")
                break

        if texto_detectado:
            print("Usted dijo:", texto_detectado)
            return texto_detectado
        else:
            print("No se entendió lo que dijo.")
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



# Hablar primero
frase_inicial = "Hola, soy Sabina, tu asistente virtual"
hablar(frase_inicial)

frase_secundaria = "Quieres que te cuente Cuento o un chiste?"
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


