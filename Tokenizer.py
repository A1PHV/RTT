import nltk
import re
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer

patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
stopwords_ru = stopwords.words("russian")
morph = MorphAnalyzer()

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

class Tokenizer:
    def __init__(self, t):
        self.text = t

    tokenization = []

    def tokenize(self, doc):
        doc = re.sub(patterns, ' ', doc)
        tokens = []
        for token in doc.split():
            if token and token not in stopwords_ru:
                token = token.strip()
                token = morph.normal_forms(token)[0]

                tokens.append(token)
        if len(tokens) > 2:
            return tokens
        return None

    def tokenization(self):
        self.tokenization = self.tokenize(self.text)
        return self.tokenization
        #for i in self.tokenization:
        #    print(i)




