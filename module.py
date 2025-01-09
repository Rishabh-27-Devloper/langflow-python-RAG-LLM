# Note: Replace **<YOUR_APPLICATION_TOKEN>** with your actual Application token
import requests
from typing import Optional

BASE_API_URL = "https://api.langflow.astra.datastax.com"
select = 1
LANGFLOW_ID = ["40c18e02-2462-4528-8f3b-d195c67206f1","aafd005d-cb75-4532-867b-725e1b089d39"][select]
FLOW_ID = ["f3d3bf28-ef4b-475b-856e-c62f9f91131f","b19d2de1-d4c4-43c1-ab66-ef70a5017a91"][select]
APPLICATION_TOKEN = ["AstraCS:HjGHBqGhKhzPReHjjDYYRUjh:ed0ca418c24e92770879d0515635f5f646198d638d80a4913ffe1a977417ee49","AstraCS:fOPkdhHbwxmWvmvBsjggRsof:2a2a190230d956af08b38d909824b675ecf4b67c11a81a37893641b1fea8f5c2"][select]
ENDPOINT = FLOW_ID+"?stream=false" # You can set a specific endpoint name in the flow settings

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = [{
  "Prompt-HSOH4": {},
  "ChatInput-7qVks": {},
  "ChatOutput-71Mwg": {},
  "GoogleGenerativeAIModel-Mybi0": {},
  "Memory-OFXhI": {},
  "AstraDB-5pjSG": {
    "advanced_search_filter": "{}",
    "api_endpoint": "https://08104d52-e171-44d1-8440-89586a84498a-us-east-2.apps.astra.datastax.com",
    "batch_size": None,
    "bulk_delete_concurrency": None,
    "bulk_insert_batch_concurrency": None,
    "bulk_insert_overwrite_concurrency": None,
    "collection_indexing_policy": "",
    "collection_name": "final_data",
    "embedding_choice": "Embedding Model",
    "keyspace": "",
    "metadata_indexing_exclude": "",
    "metadata_indexing_include": "",
    "metric": "cosine",
    "number_of_results": 4,
    "pre_delete_collection": False,
    "search_filter": {},
    "search_input": "average likes on static posts",
    "search_score_threshold": 0,
    "search_type": "Similarity",
    "setup_mode": "Sync",
    "token": "ASTRA_DB_APPLICATION_TOKEN"
  },
  "GoogleGenerativeAIModel-c2ETo": {},
  "Prompt-jKwTW": {},
  "Google Generative AI Embeddings-u3Wde": {},
  "ParseData-Nhnwe": {}
},{
  "Prompt-1mDeW": {},
  "ChatInput-jwrFS": {},
  "ChatOutput-lShCY": {},
  "GoogleGenerativeAIModel-IMmWB": {},
  "Memory-ZmY6N": {},
  "AstraDB-xAmvv": {},
  "GoogleGenerativeAIModel-fAYC3": {},
  "Prompt-D75jJ": {},
  "Google Generative AI Embeddings-riixU": {},
  "ParseData-m9nLT": {}
}
][select]

def run_flow(message: str,
  endpoint: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  application_token: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
    print(api_url)
    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    # print(payload)
    # print(headers)
    response = requests.post(api_url, json=payload, headers=headers)
    return response

def main(message,endpoint=ENDPOINT,output_type="chat",input_type="chat",application_token=APPLICATION_TOKEN,tweaks=TWEAKS):
    response = run_flow(
        message=message,
        endpoint=endpoint,
        output_type=output_type,
        input_type=input_type,
        tweaks=tweaks,
        application_token=application_token
    )
    return response.json()#['outputs'][0]['outputs'][0]['results']['message']['text']

if __name__ == "__main__":
    print(main("hii"))
