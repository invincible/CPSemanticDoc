import pickle
import re

from gensim.models import Word2Vec
from nltk import word_tokenize, SnowballStemmer
from nltk.corpus import stopwords
import numpy as np


class Word2VecPlusSGD:
    def __init__(self):
        self.sgd = None
        self.word2vec = None

    def load_models(self):
        self.word2vec = Word2Vec.load("./models/word2vec.wv")
        self.sgd = pickle.load(open("./models/sgd-w2v.pickle", "rb"))

    def __tokenize_text(self, text):
        return word_tokenize(text, language="russian")

    def __remove_stop_words(self, text):
        stopwords_list = set(stopwords.words("russian"))
        result = []
        for t in text:
            if t not in stopwords_list:
                result.append(t)
        return result

    def __stemmer_text(self, text_tokens):
        text_result = []

        snowball_stemmer = SnowballStemmer('russian')
        for t in text_tokens:
            text_result.append(snowball_stemmer.stem(t))
        return text_result

    def __prepare_text(self, text):
        text_result = self.__clear_text(text)
        text_result = self.__tokenize_text(text_result)
        text_result = self.__remove_stop_words(text_result)
        text_result = self.__stemmer_text(text_result)

        return text_result

    def __clear_text(self, text):
        document = re.sub(r'\W', ' ', text)
        document = re.sub(r'\s+[а-яА-я]\s+', ' ', document)
        document = re.sub(r'\^[а-яА-я]\s+', ' ', document)
        document = re.sub(r'[0-9]+', 'digit', document)
        document = re.sub(r'http\S+', ' ', document)
        document = re.sub(r'\s+', ' ', document, flags=re.I)
        document = re.sub(r'^b\s+', '', document)
        document = document.lower()

        return document

    def __get_sum_vector_for_text(self, tokens, vector_size):
        text_vector = np.zeros((1, vector_size))
        for token in tokens:
            if self.word2vec.wv.has_index_for(token):
                text_vector += self.word2vec.wv.get_vector(token)
        return text_vector

    def predict_for_text(self, text, vector_size):
        preparing_text = [self.__prepare_text(text)]
        text_vector = []
        for text in preparing_text:
            text_vector.append(self.__get_sum_vector_for_text(text, vector_size)[0])

        return self.sgd.predict(text_vector)[0]
