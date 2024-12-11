from fastapi import FastAPI
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


@app.get("/")
async def root():
    init()
    return {"message": "Spam Detection API is ready!"}


@app.get("/predict/{data}")
async def predict(data: str):
    if model is None or vectorizer is None:
        return {"error": "Model or vectorizer not loaded!"}

    data = clean_text(data)

    vectorized_data = vectorizer.transform([data])

    prediction = model.predict(vectorized_data)

    result = "Spam" if prediction[0] == 1 else "Not Spam"

    return {"prediction": result}
