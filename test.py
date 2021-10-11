from googletrans import Translator

def test():
    translator = Translator()
    # translate raw tweet
    language = 'pt'
    text = 'jovempannews estamos idosos proibidos de sair de casa para nosso bem aíinventaram a vacina de gripe bem na semana mais perigosa do coronavirusqual a intenção de vocês'
    try:
        temp = translator.detect('이 문장은 한글로 쓰여졌습니다.')
        print("---------------------------------------------")
        print(temp)
        print("---------------------------------------------")
        temp = translator.translate(text, src='pt', dest='en')
        en_text = temp.text
        print(f"source {temp.src} destination {temp.dest}")
        print(en_text)
    except ValueError:
        print(f"invalid language: {language}")

if __name__ == "__main__":
    test()