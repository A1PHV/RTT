from gensim.models import Word2Vec
#import nltk
import re
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
import pandas as pd

patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
stopwords_ru = stopwords.words("russian")
morph = MorphAnalyzer()

#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('omw-1.4')

class Neuro:
    def __init__(self):
        self.data = []
        #self.msg_terror = pd.read_csv("terrormsg.csv", header=None)
        self.words = pd.read_csv("terrormsg.csv", header=None)
        self.msg_terror = pd.read_csv("extract_flibusta_dialogues.1.txt", delimiter="\t", header=None)
        self.msg_terror.append(self.words)
        self.msg_terror = self.msg_terror.dropna().drop_duplicates().values.tolist()
        self.w2v_model = Word2Vec(min_count=5, window=2, negative=5, alpha=0.03, min_alpha=0.0007, sample=6e-5, sg=1)

    def lemmatize(self, doc):
        doc = re.sub(patterns, ' ', doc)
        tokens = []
        for token in doc.split():
            if token and token not in stopwords_ru:
                token = token.strip()
                token = morph.normal_forms(token)[0]
                tokens.append(token)
        if len(tokens) > 0:
            return tokens
        return "пусто"

    def ML(self):
        for i in self.msg_terror:
            if i != '#VALUE!':
                self.data.append(self.lemmatize(str(i)))
        self.w2v_model.build_vocab(self.data)
        self.w2v_model.train(self.data, total_examples=self.w2v_model.corpus_count, epochs=30, report_delay=1)
        self.w2v_model.init_sims(replace=True)
        print("Обучение завершено")

    def ret_similarity(self, word):
        return self.w2v_model.wv.most_similar(positive=word)

