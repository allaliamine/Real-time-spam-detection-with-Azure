import os
import json
import pickle
import re
from azureml.core.model import Model
import nltk
from nltk.stem import WordNetLemmatizer

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')



def init():
    global model
    # Load the entire pipeline (which includes the vectorizer and the model) using pickle
    model_path = "../spam_detection_mlflow/model.pkl"
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)



def clean_text(text):

    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+|WWW\S+', '', text, flags=re.MULTILINE)
    # Remove HTML tags
    text = re.sub('<.*?>', '', text)
    # Remove non-alphabetic characters and convert to lowercase
    text = re.sub('[^a-zA-Z]', ' ', text).lower()
    # Tokenize the text
    # words = nltk.word_tokenize(text)
    # # Remove stopwords
    # words = [w for w in words if w not in stopwords.words('english')]
    # # Stem the words
    # lemmatizer = WordNetLemmatizer()
    # words = [lemmatizer.lemmatize(w) for w in words]
    # # Join the words back into a string
    # text = ' '.join(words)
    return text    
    

def run(data):
    try:
        input_data = json.loads(data)
        
        # Extract the text field from the input data
        text = input_data['input_data']['text']
        
        cleaned_text = clean_text(text)
        
        # Use the model pipeline to predict
        prediction = model.predict([cleaned_text])
        
        # Map the prediction to a human-readable label
        predicted_label = "Spam" if prediction[0] == 1 else "Non-Spam"
        
        # Return the prediction as a JSON response
        return json.dumps({'prediction': predicted_label})
    except Exception as e:
        # Handle errors and return the error message
        error = str(e)
        return json.dumps({'error': error})



# just to test the functions
# if __name__ =="__main__":

#     init()
    
#     data = {
#                 "input_data": {
#                     "text": "Congratulations! You've won a free iPhone. Click here to claim your prize!"
#                 }
#             }

#     data_json = json.dumps(data)



#     prediction = run(data_json)
#     print(prediction)
