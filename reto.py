import  pyttsx3
import random

def hablar(texto):
    motor = pyttsx3.init()
    motor.say(texto)
    motor.runAndWait()
    motor.stop()

# Hablar primero
frase_inicial = "Hola, soy Sabina, tu asistente virtual"
frase_secundaria = "Quieres que te cuente un chiste?"
hablar(frase_inicial)
hablar(frase_secundaria)


chistes_buenos = ["¿Por qué el asistente virtual rompió con su GPS?, ¡Porque siempre lo estaba llevando por mal camino!", "¿Por qué el robot fue a terapia?, ¡Porque tenía muchos circuitos cerrados.!"]
chistes_malos = ["¿Qué hace un robot en la playa?, ¡Nada, porque se oxida!", "¿Qué hace un asistente virtual cuando se enamora?, Empieza a procesar emociones."]

pregunta = input("Quieres que te cuente un chiste? :")
#opciones
if pregunta == "si":
    respuesta = "bien, te contare un chiste bueno."
    chiste = "Aqui va...." + random.choice(chistes_buenos)
    
elif pregunta == "no":
    respuesta = "oh.., igual te lo contare"
    chiste = "Aqui va...." + random.choice(chistes_malos)

else:
    respuesta = "no entendi tu respuesta"
  
hablar(respuesta)
hablar(chiste)
    