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
        result = poller.result()
        print("Message sent")

    except Exception as ex:
        print(ex)



def on_event(partition_context, event):
     
    data = json.loads(event.body_as_str()) 
    email = data.get("email") 
    message = data.get("message") 
    sender = data.get("sender")

    response = requests.post(PREDICT_API_URL, json={"email": email, "message": message, "sender": sender}) 
    prediction = response.json().get("prediction")
    
    logging.info(f"Predicted result for {message}: {prediction}") 

    print(f"Predicted result for {message}: {prediction}") 
    print()

    if prediction == "Spam": 
        send_email(email, message)
        time.sleep(8)

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
