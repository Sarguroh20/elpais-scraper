from googletrans import Translator

translator = Translator()

def translate_title(title):
    try:
        return translator.translate(title, src="es", dest="en").text
    except:
        return "N/A"