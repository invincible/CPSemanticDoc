import pickle
import re
from nltk import word_tokenize, SnowballStemmer
from nltk.corpus import stopwords



class BertPlusSGD:
    def __init__(self):
        self.sgd = None
        self.bert = None

    def load_models(self):
        self.bert = pickle.load(open("./models/bert_vectorizer.pickle", "rb"))
        self.sgd = pickle.load(open("./models/sgd-bert.pickle", "rb"))

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

    def __prepare_text(self, text, text_vectorizer):
        text_result = self.__clear_text(text)
        text_result = self.__tokenize_text(text_result)
        text_result = self.__remove_stop_words(text_result)
        text_result = self.__stemmer_text(text_result)
        text_result = " ".join(text_result)

        text_vector = text_vectorizer.transform([text_result]).toarray()
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

    def predict_for_text(self, text):
        preparing_text = self.__prepare_text(text, self.bert)
        return self.sgd.predict(preparing_text)[0]
