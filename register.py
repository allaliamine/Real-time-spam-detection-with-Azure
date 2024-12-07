from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes


credential = DefaultAzureCredential()

ml_client = MLClient(
    credential=credential,
    subscription_id="SUB_ID",
    resource_group_name="RES_GROUP_NAME",
    workspace_name="WORKSPACE_NAME",
)


mlflow_model = Model(
    path="/home/azureuser/cloudfiles/code/Users/<USERNAME>/Real-time-spam-detection-with-Azure/spam_detection_mlflow",
    type=AssetTypes.MLFLOW_MODEL,
    name="spam-detection-model",
    description="Custom model to predict spams and non-spams"
)

registered_model = ml_client.models.create_or_update(mlflow_model)
print(f"Model registered: {registered_model.name} (Version: {registered_model.version})")
