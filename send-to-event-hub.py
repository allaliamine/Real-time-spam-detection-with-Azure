from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient
from dotenv import load_dotenv
import requests
import asyncio
import json
import os



load_dotenv()

conn_string_eventHUB = os.getenv('CONNECTION_STR')
eventHUB_name = os.getenv('EVENTHUB_NAME')

EVENT_HUB_CONNECTION_STR = conn_string_eventHUB
EVENT_HUB_NAME = eventHUB_name


def fetch_api_data(api_url): 
    response = requests.get(api_url) 
    return response.json()

async def run(): 
    producer = EventHubProducerClient.from_connection_string( 
        conn_str=EVENT_HUB_CONNECTION_STR, 
        eventhub_name=EVENT_HUB_NAME 
        ) 
    
    async with producer: 

        api_url = "https://spam-api-e7c4ayf6dfcvedfh.francecentral-01.azurewebsites.net/send-email" 
        api_response = fetch_api_data(api_url) 
       
       
        api_response = fetch_api_data(api_url)

        event_data = json.dumps(api_response)

        event_data_bytes = event_data.encode("utf-8")

        event_data_batch = await producer.create_batch()
        event_data_batch.add(EventData(event_data_bytes))

        await producer.send_batch(event_data_batch)
        
async def main():
    i=0
    while True: 
        try: 
            i+=1
            await run()
            print(f"operation number {i}: Data sent to Event Hub")
        except Exception as e:
            print(f"An error occurred: {e}") 
            break

if __name__ == "__main__": 
    asyncio.run(main())