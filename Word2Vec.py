from gensim.models import Word2Vec
from Tokenizer import Tokenizer

tokenization = []

class Neuro:
    def __init__(self, t):
        self.text = t

    def prepare_text(self):
        Tokenization = Tokenizer(self.text)
        self.tokenization = Tokenization.tokenization()

    def ML(self):
        self.prepare_text()
        w2v_model = Word2Vec(min_count=10, window=2, negative=10, alpha=0.03, min_alpha=0.0007, sample=6e-5, sg=1)
        w2v_model.train(tokenization, total_examples=w2v_model.corpus_count, epochs=30, report_delay=1)
        w2v_model.init_sims(replace=True)

