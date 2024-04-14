import pickle
import re

import nltk
from nltk import word_tokenize, SnowballStemmer
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from sklearn.linear_model import SGDClassifier
import numpy as np


class LearnerWord2VecPlusSGD:
    def __init__(self):
        self.sgd = None
        self.word2vec = None

    def save_models(self):
        self.word2vec.save("./models/word2vec.wv")
        pickle.dump(self.sgd, open("./models/sgd-w2v.pickle", "wb"))

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

    def __prepare_texts(self, texts):
        preparing_text = []

        for text in texts:
            text_result = self.__clear_text(text)
            text_result = self.__tokenize_text(text_result)
            text_result = self.__remove_stop_words(text_result)
            text_result = self.__stemmer_text(text_result)
            preparing_text.append(text_result)

        return preparing_text

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

    def learn_models(self, texts, vector_size, labels):
        nltk.download('punkt')
        nltk.download('stopwords')

        self.word2vec = Word2Vec(
            min_count=1,
            window=10,
            vector_size=vector_size,
            negative=10,
            alpha=0.03,
            min_alpha=0.0007,
            sample=6e-5,
            sg=1)

        texts_clear = self.__prepare_texts(texts)
        self.word2vec.build_vocab(texts_clear)
        self.word2vec.train(texts_clear, epochs=20, total_examples=len(texts_clear))

        texts_vectors = []
        for text in texts_clear:
            texts_vectors.append(self.__get_sum_vector_for_text(text, vector_size)[0])

        self.sgd = SGDClassifier(loss="hinge")
        self.sgd.fit(texts_vectors, labels)
