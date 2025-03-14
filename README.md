# Real-time Spam Detection with Azure

[![Azure](https://img.shields.io/badge/Azure-%230072C6.svg?style=for-the-badge&logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com)

## Table of Contents
- [Project Description](#project-description)
- [Key Features](#key-features)
- [Architecture Overview](#architecture-overview)
- [Technologies Used](#technologies-used)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contact](#contact)

## Project Description
A real-time spam detection system leveraging Microsoft Azure cloud services to process and classify text messages/data streams. The solution demonstrates:
- Real-time data ingestion and processing
- Machine learning model deployment
- Cloud-native architecture patterns


## Key Features
- Real-time message processing pipeline
- Azure-hosted machine learning model for spam classification
- Automatic scaling based on workload
- Integration with Azure storage solutions
- Alerting system for detected spam patterns


## Architecture Overview

![image](https://github.com/allaliamine/Real-time-spam-detection-with-Azure/tree/main/pictures/Architecture.png)


## Technologies Used
Cloud Services:

- Azure Event Hubs (Real-time Data Streaming)
- Azure Machine Learning
- Azure Web App (Hosting the model as an API)
- Azure App insight (Monitoring and logging)
- Azure Blob Storage
- Azure Communication Services (Communication)
- Azure Email Communication Services (email-based notifications)

Programming & Tools:

- Python (ML Model Development)
- Jupyter Notebooks (data analysis and model prototyping)
- Git & GitHub (Version control with CI/CD)
- FastAPI (API Development)
- Scikit-learn (Machine Learning Model Training)



## Requirements

- Active Azure subscription
- Required permissions for resource creation
- Python 3.12  (or higher)
- An IDE for python (e.g., VS Code, Pycharm)

## Installation

1. clone the repository :

```bash
git clone https://github.com/allaliamine/Real-time-spam-detection-with-Azure.git 
```
2. set up envirement variables:
```bash
cp .env.exemple .env
```
3. create Azure services and file up the .env file
- Azure EventHub : ```CONNECTION_STR```, ```EVENTHUB_NAME``` .
- Azure Blob Storage : ```AZURE_STORAGE_CONNECTION_STRING```, ```BLOB_CONTAINER_NAME```,```AZURE_TABLE_CONNECTION_STRING```, ```TABLE_NAME``` .
- Azure Communication Services : ```connection_string_email```, ```senderAddress``` .

4. Install python dependencies: 
```bash 
pip install -r requirements.txt
```
> [!TIP]
> It is recommended to create a virtual environment to install dependencies. This helps avoid version conflicts with packages that may already be installed globally.

5. deploy the API App to Azure Web App:
- You can deploy the API using GitHub or manually via the Azure CLI.
- for Azure CLI : 
```bash 
az webapp up --resource-group <resource-group-name> --name <app-name> --runtime "PYTHON:${Version of python here}"
```
> [!IMPORTANT]
> Ensure all Azure services are properly configured and accessible before deployment.





## Usage

To run the project, you need two terminals: one for running the sending script and the other for running the processing script.

Run the sending script:
```bash
python3 send-to-event-hub.py
```

Run the processing script:
```bash
python3 get-from-event-hub.py
```

#### Real-Time Email Notifications
To test real-time email notifications:

    1. Open the Datasets/generated-dataset.csv file.
    2.Replace the email address anir.linux111@gmail.com with an email address you have access to.
    3.Save the file and run the scripts again.


#### Exemple of Notifications

![image](pictures/notification_exemple.png =600x500)



## Contact

For any inquiries or feedback, please contact:

- [Allali Mohamed Amin](https://www.linkedin.com/in/m-amin-allali/)
- [Badri Insaf](https://www.linkedin.com/in/insaf-badri-588299248/)

