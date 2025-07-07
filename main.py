import pyttsx3

#Iniciar el motor
engine = pyttsx3.init()

#configuracián de parámetros
engine.setProperty("rate",150)
engine.setProperty("volume",0.9)

#Seleccion de voz
voices = engine.getProperty("voices")
#for i, voz in enumerate(voices):
    #print(f"{voz.name}")
    
engine.setProperty("voice", voices[0].id)

text = "Hola, espero que estes muy bien. Soy tu asistente Sabina"

#vocalizar texto 
engine.say(text)

#ejecutar
engine.runAndWait()
