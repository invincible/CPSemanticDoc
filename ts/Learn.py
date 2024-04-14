import pickle
import re

import nltk
from nltk import word_tokenize, SnowballStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier


class LearnerTFIdfPlusSGD:
    def __init__(self):
        self.sgd = None
        self.tfids_vectorizer = None

    def save_models(self):
        pickle.dump(self.tfids_vectorizer, open("./models/tfids_vectorizer.pickle", "wb"))
        pickle.dump(self.sgd, open("./models/sgd-tfidf.pickle", "wb"))

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

    def __prepare_texts(self, texts, text_vectorizer):
        preparing_text = []

        for text in texts:
            text_result = self.__clear_text(text)
            text_result = self.__tokenize_text(text_result)
            text_result = self.__remove_stop_words(text_result)
            text_result = self.__stemmer_text(text_result)
            text_result = " ".join(text_result)
            preparing_text.append(text_result)

        text_vector = text_vectorizer.fit_transform(preparing_text).toarray()
        return text_vector

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

    def learn_models(self, texts, labels):
        nltk.download('punkt')
        nltk.download('stopwords')

        self.tfids_vectorizer = TfidfVectorizer()
        x = self.__prepare_texts(texts, self.tfids_vectorizer)

        self.sgd = SGDClassifier(loss="hinge")
        self.sgd.fit(x, labels)
