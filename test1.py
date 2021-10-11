from googletrans import Translator

# Check that googletrans is working (it doesn't always)
translator = Translator()
results =translator.translate('हॅलो वर्ल्ड')
print(results.text)