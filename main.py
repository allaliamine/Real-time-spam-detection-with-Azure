from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle
import re
import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords

app = FastAPI()

# Globals for model and vectorizer
model = None
vectorizer = None
nltk.data.path.append('./nltk_data')

class MessageInput(BaseModel):
    message: str


def init():
    global model, vectorizer

    model_path = "./model/Spam-Detection-Model.pkl"
    vectorizer_path = "./model/Spam-Detection-Vectorizer.pkl"

    # Load model and vectorizer
    with open(model_path, "rb") as mdl:
        model = pickle.load(mdl)

    with open(vectorizer_path, "rb") as vec:
        vectorizer = pickle.load(vec)

def clean_text(text):

    text = re.sub(r'http\S+|www\S+|https\S+|WWW\S+', '', text, flags=re.MULTILINE)
    text = re.sub('<.*?>', '', text)
    text = re.sub('[^a-zA-Z]', ' ', text).lower()
    words = nltk.word_tokenize(text)
    words = [w for w in words if w not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(w) for w in words]
    text = ' '.join(words)

    return text

def read_csv(file_path):
    df = pd.read_csv(file_path)
    
    if 'Email' not in df.columns or 'Message' not in df.columns:
        raise ValueError("CSV file must contain 'Email' and 'Message' columns")
    
    return df

@app.get('/send-email')
def send_email():
    file_path = './Dataset/real-time-data.csv'
    
    df = read_csv(file_path)
    
    selected_email = df.sample(n=1).iloc[0]
    
    email_info = {
        "email": selected_email['Email'],
        "message": selected_email['Message'],
    }
    
    return email_info

@app.get("/")
async def root():
    init()
    return {"message": "Spam Detection API is ready!"}


@app.post("/predict")
async def predict(data: MessageInput):

    if model is None or vectorizer is None:
        return {"error": "Model or vectorizer not loaded!"}

    message = data.message

    cleaned_message = clean_text(message)

    vectorized_data = vectorizer.transform([cleaned_message])

    prediction = model.predict(vectorized_data)

    result = "Spam" if prediction[0] == 1 else "Not Spam"

    return {"prediction": result}