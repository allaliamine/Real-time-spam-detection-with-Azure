import logging
import requests
import json
from azure.eventhub import EventHubConsumerClient
import time

CONNECTION_STR = "######"
CONSUMER_GROUP = "$Default"
EVENTHUB_NAME = "######"
PREDICT_API_URL = "https://spam-api-e7c4ayf6dfcvedfh.francecentral-01.azurewebsites.net/predict"



from azure.communication.email import EmailClient

def send_email(email, message):
    try:
        connection_string = "#########"
        client = EmailClient.from_connection_string(connection_string)

        message = {
            "senderAddress": "##########",
            "recipients": {
                "to": [{"address": f"{email}"}]
            },
            "content": {
                "subject": "SPAM NOTIFICATION",
                "plainText": "Hello world via email.",
                "html": f"""
				<html>
					<body>
                        <h4>Hello a <a style="color:red;">SPAM</a> was detected</h4>
						<h6>the message :</h6>
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

    # Call the predict API 

    response = requests.post(PREDICT_API_URL, json={"email": email, "message": message}) 
    prediction = response.json().get("prediction")
    
    logging.info(f"Predicted result for {message}: {prediction}") 

    print(f"Predicted result for {message}: {prediction}") 
    print()

    if prediction == "Spam": 
        send_email(email, message)
        time.sleep(8)
    # If the content is detected as spam, send an alert email 
    # if prediction.get("is_spam"): 
    #     # send_alert_email(email, message) 
    #     partition_context.update_checkpoint(event)

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
