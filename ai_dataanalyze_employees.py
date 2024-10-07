import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
import requests

load_dotenv()

def get_employees():
    base_url= os.getenv("EMPLOYEE_REQUEST_URL")
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        # Making the GET request
        response = requests.get(base_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            if "errors" in result:
                return "recordNotFound"
            return result  # Return JSON
            
        else:
            return f"Failed to retrieve data. Status code: {response.status_code}"
    
    except Exception as e:
        return str(e)

print(get_employees())
employees_response = pd.DataFrame(get_employees()) #Convert response to dataframe

api_type = "azure"
api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("API_VERSION")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment_name = os.getenv("DEPLOYMENT_NAME")
model_name = os.getenv("MODEL_NAME")

print(api_type)
print(api_base)
print(api_version)
print(api_key)
print(deployment_name)
print(model_name)

llm = AzureOpenAI(
    openai_api_key=api_key, 
    deployment_name=deployment_name, 
    model_name=model_name,
    api_version=api_version, 
    azure_endpoint=api_base)


agent = create_pandas_dataframe_agent(llm, employees_response, verbose=True, allow_dangerous_code=True)
agent.run("What is the amount of employees whose end date is between '2024-01-01' and 2024-06-30'?")
#agent.run("What is the amount of employees whose end date is null?")
#agent.run("Which teams exist?")
