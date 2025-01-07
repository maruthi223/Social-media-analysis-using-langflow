# from langflow.load import run_flow_from_json
from dotenv import load_dotenv
import requests
from typing import Optional
import json
import os

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "39cdaafa-cc9d-4659-9975-8bd02a62358f"
APPLICATION_TOKEN = os.getenv("LANGFLOW_TOKEN")


# def ask_ai():
#     TWEAKS = {
#         "ChatInput-CROj7": {
#             "input_value": "what is the engagement rate of reels compared to Carousel and static images"
#         }
#     }

#     result = run_flow_from_json(flow="hackathon.json",
#                                 input_value="message",
#                                 fallback_to_env_vars=True,
#                                 tweaks=TWEAKS)

#     return result[0].outputs[0].results["text"].data["text"]
# result= ask_ai()

def get_macros(profile):
    TWEAKS = {
    }
    return run_flow(profile, tweaks=TWEAKS, application_token=APPLICATION_TOKEN)


def run_flow(message: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  application_token: Optional[str] = None) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/customer-1"

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
    response = requests.post(api_url, json=payload, headers=headers)
    
    # return json.loads(response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"])
    return (response.json()['outputs'][0]['outputs'][0]['results']['message']['data']['text'])

result = get_macros("what is the engagement rate of reels compared to Carousel and static images")
print(result)