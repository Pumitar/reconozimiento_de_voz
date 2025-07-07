import pyttsx3
import random, requests
import speech_recognition as sr

chistes = [{"pregunta": "¿Por qué el asistente virtual rompió con su GPS?", "respuesta": "¡Porque siempre lo estaba llevando por mal camino!"}, {
    "pregunta": "¿Por qué el robot fue a terapia?", "respuesta": "¡Porque tenía muchos circuitos cerrados.!"}, {"pregunta": "¿Qué hace un robot en la playa?", "respuesta": "¡Nada, porque se oxida!"}, {
    "pregunta": "¿Qué hace un asistente virtual cuando se enamora?", "respuesta": "¡Empieza a procesar emociones.!"}]

cuentos = [{ "titulo": "El robot soñador", "texto": "Había una vez un robot que soñaba con ser humano. Pasaba sus días observando a las personas y aprendiendo de ellas. Un día, decidió que quería sentir emociones. Así que se programó para reír, llorar y amar. Aunque nunca llegó a ser humano, su corazón de metal latía con fuerza por todo lo que había aprendido."},{
    "titulo": "El asistente virtual y el misterio del café", "texto": "Un asistente virtual llamado Sabina se dio cuenta de que cada mañana, su dueño dejaba una taza de café a medio beber. Intrigada, decidió investigar. Después de varios días de observación, descubrió que su dueño solo tomaba café cuando estaba pensando en algo importante. Desde entonces, Sabina siempre preparaba una taza de café caliente para ayudar a su dueño a concentrarse."},{
    "titulo": "El cuento del robot y la luna", "texto": "Un robot llamado Luna soñaba con visitar la luna. Un día, decidió construir un cohete con piezas de repuesto. Después de mucho esfuerzo, logró despegar y llegó a la luna. Allí, descubrió un paisaje lleno de estrellas y silencio. Aunque no podía tocar la luna, su corazón robótico se llenó de felicidad al cumplir su sueño."}]


def get_clima(city: str) -> str:
    base_url = f"https://wttr.in/{city}?format=%C+%t"# Iniciar el bot
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        return "No se pudo obtener el clima. Asegúrate de que la ciudad sea válida."

def iniciar_reconocimiento():
    mic = sr.Microphone(device_index=2)
    recog = sr.Recognizer()
    return mic, recog
    
def hablar(texto):
    motor = pyttsx3.init()
    motor.say(texto)
    motor.runAndWait()
    motor.stop()

def escuchar(mic=None, recog=None):
    
    if recog is None:
        mic, recog = iniciar_reconocimiento()
        
    with mic as audio_file:
        print("Por favor, hable")
        recog.adjust_for_ambient_noise(audio_file, duration=0.5)

        try:
            audio = recog.listen(audio_file, phrase_time_limit=2)
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
    if "clima" in texto:
        return "clima"
    elif "cuento" in texto:
        return "cuento"
    elif "chiste" in texto:
        return "chiste"
    elif "nada" in texto:
        return "nada"
    else:
        return "respuesta no válida"

def get_asistente(rsp):
    chiste = {}
    cuento = {}
    
    if rsp == "clima":
        respuesta = "ok, dime la ciudad de la que quieres saber el clima"
        city = escuchar(mic, recog)
        clima_info = get_clima(city)
        clima_city = "El clima en"+city+ "es:" +clima_info+ "."
        
    elif rsp == "cuento":
        respuesta = "bien, te contare un cuento. Aqui va...."
        cuento = random.choice(cuentos)
    
    elif rsp == "chiste":
        respuesta = "oks, te lo contare. Aqui va...."
        chiste = random.choice(chistes)
        
    elif rsp == "nada":
        respuesta = "ok, igual te contare algo. Aqui va!"
        random.randint(1, 2)
        if random.randint(1,2) == 1:
            chiste = random.choice(chistes)
        elif random.randint(1,2) == 2:
            cuento = random.choice(cuentos)

    else:
        respuesta = "no entendi tu respuesta"
        
    return respuesta, chiste, cuento


mic, recog = iniciar_reconocimiento()

# Hablar primero
frase_inicial = "Hola, soy Sabina, tu asistente virtual"
hablar(frase_inicial)

frase_secundaria = "Que quieres que te diga?.. Puedo decirte el clima, un chiste, un cuento, o simplemente nada."
hablar(frase_secundaria)

#reconocimiento
rsp = escuchar(mic, recog)
rsp = interpretar_respuesta(rsp)

# opciones
respuesta, chiste, cuento = get_asistente(rsp)




hablar(respuesta)
# hablar(cuento)

if chiste:
    chiste_pregunta = chiste.get("pregunta")
    chiste_respuesta = chiste.get("respuesta")
    hablar(chiste_pregunta)
    hablar(chiste_respuesta)
elif cuento:
    cuento_titulo = cuento.get("titulo")
    cuento_texto = cuento.get("texto")
    hablar(cuento_titulo)
    hablar(cuento_texto)
