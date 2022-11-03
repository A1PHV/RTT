import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

#nltk.download('punkt')
#nltk.download('stopwords')

class Text_Handler:
    def __init__(self, t):
        self.text = t

    tokenization = []

    def tokenize(self):
        st = nltk.sent_tokenize(self.text)
        for i in st:
            wt = word_tokenize(i)
            self.tokenization.append(wt)
        russian_stopwords = stopwords.words("russian")
        self.tokenization = [word for word in self.tokenization if word not in russian_stopwords]

    def write(self):
        for i in self.tokenization:
            print(i)

vertext = input()
T = Text_Handler(vertext)
T.tokenize()
T.write()