import mlflow
import pickle
from sklearn.pipeline import Pipeline

# Paths to your model and vectorizer
vectorizer_path = "/home/azureuser/cloudfiles/code/Users/<USERNAME>/Real-time-spam-detection-with-Azure/model/Spam-Detection-Vectorizer.pkl"
model_path = "/home/azureuser/cloudfiles/code/Users/<USERNAME>/Real-time-spam-detection-with-Azure/model/Spam-Detection-Model.pkl"

# Load the vectorizer and model
with open(vectorizer_path, "rb") as f:
    vectorizer = pickle.load(f)
with open(model_path, "rb") as f:
    model = pickle.load(f)

# Combine them into a single pipeline (if applicable)
pipeline = Pipeline([("vectorizer", vectorizer), ("model", model)])

# Save the model as an MLflow artifact
mlflow.sklearn.save_model(
    sk_model=pipeline,
    path="./Real-time-spam-detection-with-Azure/spam_detection_mlflow",
)
