from fastapi import FastAPI
import uvicorn
from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo
from phi.llm.groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
app = FastAPI()

from io import StringIO 
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


import re

def clean_text(text):
    # Remove escape sequences
    cleaned_text = re.sub(r'\x1b\[[0-9;]*m', '', text)
    
    # Remove pipe characters and other unnecessary characters
    cleaned_text = re.sub(r'[|]', '', cleaned_text)
    
    # Remove unnecessary white spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text

@app.post("/process-ingredients/")
async def process_ingredients(product_name: str):
    assistant = Assistant(
        llm=Groq(model="gemma2-9b-it"),
        tools=[DuckDuckGo()],
        description="You are a diet research expert and your job is to research and tell the ingredients list along with their composition of any given product in a specific JSON format.",
        instructions=[
            "Provide the response strictly in the following JSON format without any pretext or disclaimer",
            """Required Output format: "{\"product_name\":\"<ProductName>\",\"ingredients\":[{\"name\":\"<Ingredient1>\",\"composition\":\"<X grams/mg>\"},{\"name\":\"<Ingredient2>\",\"composition\":\"<Y grams/mg>\"}]}" """,
            "Add more ingredients as needed but in a JSON format",
            "ONLY Respond back with json. Nothing extra."
        ],
        # debug_mode=True
    )
    
    # Generate response
    output = assistant.run(f"{product_name} Ingredients list", stream=False)
    print(f"Agent Raw Response: {output}")
    # The string response from the AI agent
    response = f'{{"response": {output}}}'

# Convert the string to a Python dictionary
    response_dict = json.loads(response)

# Now clean_response is a proper dictionary
    print(json.dumps(response_dict, indent=4))
    # assistant.print_response(f"{product_name} Ingredients list", markdown=False)
    # response_data = json.loads(response)
    # ingredients = [ingredient["name"] for ingredient in response_data["ingredients"]]
    # ingredient_query = ', '.join(ingredients)
    
    # # Send the query to Wolfram Alpha API
    # wolfram_url = f"http://api.wolframalpha.com/v2/query?input={ingredient_query}&format=plaintext&output=JSON&appid={WOLFRAM_API_KEY}"
    # wolfram_response = requests.get(wolfram_url)
    
    # if wolfram_response.status_code == 200:
    #     wolfram_data = wolfram_response.json()
    #     # Extract necessary information from Wolfram's response (depends on the API structure)
    #     nutritional_info = wolfram_data["queryresult"]["pods"]  # Example of how to parse the response
    # else:
    #     nutritional_info = {"error": "Failed to retrieve data from Wolfram API"}
    
    # return {"response": response_data, "nutritional_info": nutritional_info}
    # response_data = json.loads(response)
    # return {"response": cleaned_text}
    return response_dict

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
