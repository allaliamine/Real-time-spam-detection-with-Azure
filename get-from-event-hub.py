from azure.storage.blob import BlobServiceClient
from azure.eventhub import EventHubConsumerClient
from azure.communication.email import EmailClient
from dotenv import load_dotenv
import requests
import logging
import json
import time
import os

load_dotenv()

conn_string_eventHUB = os.getenv('CONNECTION_STR')
eventHUB_name = os.getenv('EVENTHUB_NAME')
conn_string_email_sender = os.getenv('connection_string_email')
senderADD = os.getenv('senderAddress')


CONNECTION_STR = conn_string_eventHUB
CONSUMER_GROUP = "$Default"
EVENTHUB_NAME = eventHUB_name
PREDICT_API_URL = "https://spam-api-e7c4ayf6dfcvedfh.francecentral-01.azurewebsites.net/predict"
CONN_STRING_BLOB = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = os.getenv('BLOB_CONTAINER_NAME')


def save_to_blob_storage(data, file_name): 

    try: 
        blob_service_client = BlobServiceClient.from_connection_string(CONN_STRING_BLOB) 

        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, 
                                                          blob=file_name)
        
        blob_client.upload_blob(data, overwrite=True) 
        print(f"Data saved to blob storage") 

    except Exception as ex: 
        print(f"Failed to save data to blob storage: {ex}")

    

def send_email(email, message, sender):
    try:
        connection_string = conn_string_email_sender
        client = EmailClient.from_connection_string(connection_string)

        message = {
            "senderAddress": f"{senderADD}",
            "recipients": {
                "to": [{"address": f"{email}"}]
            },
            "content": {
                "subject": "SPAM NOTIFICATION",
                "plainText": "Hello world via email.",
                "html": f"""
				<html>
					<body>
                        <h3>Hello a <a style="color:red;">SPAM</a> was detected !!</h3>
						<h4>It was sent by :{sender}</h4>
                        <h4>The Message :</h4>
                        <p>{message}</p>
					</body>
				</html>"""
            },
            
        }

        poller = client.begin_send(message)
        print("Message sent")

    except Exception as ex:
        print(ex)



def on_event(event):
     
    data = json.loads(event.body_as_str()) 
    email = data.get("email") 
    message = data.get("message") 
    sender = data.get("sender")

    response = requests.post(PREDICT_API_URL, json={"email": email, "message": message, "sender": sender}) 
    prediction = response.json().get("prediction")
    
    logging.info(f"Predicted result for {message}: {prediction}") 
    print("----------------------------------------------")
    print(f"Predicted result for {message}: {prediction}") 
    print()

    if prediction == "Spam": 
        send_email(email, message, sender)

    data_with_prediction = { 
        "email": email, 
        "message": message, 
        "sender": sender, 
        "prediction": prediction 
    } 
    
    save_to_blob_storage(json.dumps(data_with_prediction), f"{str(time.time()).replace(".", "_")}_data.json") 
    time.sleep(3)

def main(): 
    client = EventHubConsumerClient.from_connection_string( 
        conn_str=CONNECTION_STR, 
        consumer_group=CONSUMER_GROUP, 
        eventhub_name=EVENTHUB_NAME 
        )
    
    with client: 
        client.receive( 
            on_event=on_event, 
            starting_position="-1",
        ) 
        

if __name__ == "__main__":
    main()
