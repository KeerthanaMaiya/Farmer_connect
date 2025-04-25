from googletrans import Translator

translator = Translator()

from_lang = 'en'
to_lang = 'kn'

get_sentence = input("Enter")

text_to_translate = translator.translate(get_sentence,src= from_lang,dest= to_lang)
text = text_to_translate.text
print(text)

