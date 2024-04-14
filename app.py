from io import BytesIO

import PyPDF2 as PyPDF2
from fastapi import FastAPI, UploadFile
from typing import Annotated
from fastapi import Form
from pydantic import BaseModel

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from bs.Test import BertPlusSGD
from ts.Test import TFIdfPlusSGD
from ws.Test import Word2VecPlusSGD

Base = declarative_base()
class document_types(Base):
    __tablename__ = "document_types"
    id = Column(Integer, primary_key=True, index=True, name="id")
    type = Column(String, name="type")

    def __init__(self, name):
        self.type = name

class documents(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True, name="id")
    text = Column(String, name="text")
    type_id = Column(Integer, ForeignKey('document_types.id'), name="type_id")

    def __init__(self, text, type_id):
        self.text = text
        self.type_id = type_id

class predictions(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True, name="id")
    prediction = Column(String, name="prediction")
    document_id = Column(Integer, ForeignKey('documents.id'), name="document_id")

    def __init__(self, prediction, document_id):
        self.prediction = prediction
        self.document_id = document_id

class reaction(Base):
    __tablename__ = "reaction"
    id = Column(Integer, primary_key=True, index=True, name="id")
    reaction_type = Column(String, name="reaction_type")
    predictions_id = Column(Integer, ForeignKey('predictions.id'), name="predictions_id")

    def __init__(self, reaction_type, predictions_id):
        self.reaction_type = reaction_type
        self.predictions_id = predictions_id


engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/test")
session = Session(bind=engine)

Base.metadata.create_all(bind=engine)

#добавить классы которые есть в тестовом датасете и загрузить документы из тестового датасета

created_doc_type1 = document_types("доверенность")
created_doc_type2 = document_types("акт")
created_doc_type3 = document_types("счет")
created_doc_type4 = document_types("приказ")
created_doc_type5 = document_types("заявление")
created_doc_type6 = document_types("устав")
created_doc_type7 = document_types("решение")
created_doc_type8 = document_types("приложение")
created_doc_type9 = document_types("договор")
created_doc_type10 = document_types("соглашение")
created_doc_type11 = document_types("договор оферты")
session.add_all([created_doc_type1, created_doc_type2, created_doc_type3, created_doc_type4,
                created_doc_type5, created_doc_type6, created_doc_type7, created_doc_type8,
                created_doc_type9, created_doc_type10, created_doc_type11])
session.commit()


tfidf = TFIdfPlusSGD()
tfidf.load_models()
w2v = Word2VecPlusSGD()
w2v.load_models()
bert = BertPlusSGD()
bert.load_models()


app = FastAPI()

@app.get("/app/types")
async def get_types():
    return session.query(document_types).all()


class doc_type(BaseModel):
    name: str
@app.post("/app/types")
async def create_doc_type(new_doc_type: doc_type):
    created_doc_type = document_types(new_doc_type.name)
    session.add(created_doc_type)
    session.commit()
    return session.query(document_types).all()



class doc_from_text(BaseModel):
    type_id: int
    text: str
@app.post("/app/text")
async def create_doc_from_txt(doc: doc_from_text):
    created_doc = documents(doc.text, doc.type_id)
    session.add(created_doc)
    session.commit()
    session.refresh(created_doc)
    return created_doc


import docx
def extract_text_from_file(file: UploadFile):
    if ".pdf" in file.filename:
        read_pdf = PyPDF2.PdfReader(file.file)
        number_of_pages = len(read_pdf.pages)
        text = ""
        for i in range(number_of_pages):
            page = read_pdf.pages[0]
            text += page.extract_text()
        return text
    elif ".doc" in file.filename or ".docx" in file.filename:
        data = file.file.readlines()
        bytes_str = b''.join(data)
        doc = docx.Document(BytesIO(bytes_str))
        text = ""
        for parag in doc.paragraphs:
            text += parag.text
        return text
    elif ".rtf" in file.filename:
        #  проблемы с колировкой
        file_content_read = file.file.readlines()
        text = b''.join(file_content_read)
        from rtf_converter import rtf_to_txt
        plain_text = rtf_to_txt(text.decode('cp1251'))
        return plain_text
    elif ".txt" in file.filename:
        lines = file.file.readlines()
        text = ""
        for i in lines:
            text += i.decode('utf8')
        return text
    elif ".html" in file.filename:
        lines = file.file.readlines()
        text = ""
        for i in lines:
            text += i.decode('utf8')
        return text


@app.post("/app/file")
async def create_doc_txt(type_id: Annotated[int, Form()], file: Annotated[UploadFile, Form()]):
    text = extract_text_from_file(file)
    created_doc = documents(text, type_id)
    session.add(created_doc)
    session.commit()
    session.refresh(created_doc)
    return created_doc


def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i
    return num

def predict_class(text):
    pr1 = tfidf.predict_for_text(text)
    pr2 = w2v.predict_for_text(text, 150)
    pr3 = bert.predict_for_text(text)
    return most_frequent([pr1, pr2, pr3])


class check_doc_by_text(BaseModel):
    text: str
@app.post("/app/classification/text")
async def check_text(doc: check_doc_by_text):
    prediction = predict_class(doc.text)

    doc_type = session.query(document_types).filter(document_types.type == prediction).first()

    created_doc = documents(doc.text, doc_type.id)
    session.add(created_doc)
    session.commit()
    session.refresh(created_doc)

    prediction = predict_class(doc.text)
    new_prediction = predictions(prediction, created_doc.id)
    session.add(new_prediction)
    session.commit()
    session.refresh(new_prediction)

    return new_prediction


@app.post("/app/classification/file")
async def check_file(file: Annotated[UploadFile, Form()]):
    text = extract_text_from_file(file)
    prediction = predict_class(text)

    doc_type = session.query(document_types).filter(document_types.type == prediction).first()
    created_doc = documents(text, doc_type.id)
    session.add(created_doc)
    session.commit()
    session.refresh(created_doc)

    prediction = predict_class(text)
    new_prediction = predictions(prediction, created_doc.id)
    session.add(new_prediction)
    session.commit()
    session.refresh(new_prediction)
    return new_prediction


class feedback_data(BaseModel):
    predict_id: int
    feedback: int
@app.post("/app/feedback")
async def check_text(data: feedback_data):
    new_reaction = reaction(data.feedback, data.predict_id)
    session.add(new_reaction)
    session.commit()
    session.refresh(new_reaction)
    return new_reaction