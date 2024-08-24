from fastapi import FastAPI
import uvicorn
from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo
from phi.llm.groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
app = FastAPI()

@app.post("/process-ingredients/")
async def process_ingredients(product_name: str):
    assistant = Assistant(
        llm=Groq(model="llama-3.1-70b-versatile"),
        tools=[DuckDuckGo()],
        description="You are a diet research expert and your job is to research and tell the ingredients list along with their composition of any given product in a specific JSON format.",
        instructions=[
            "Provide the response strictly in the following JSON format without any pretext or disclaimer",
            """Required Output format: "{\"product_name\":\"<ProductName>\",\"ingredients\":[{\"name\":\"<Ingredient1>\",\"composition\":\"<X%>\"},{\"name\":\"<Ingredient2>\",\"composition\":\"<Y%>\"}]}" """,
            "Add more ingredients as needed but in a JSON format",
            "don't add any pretext. Only "
        ],
        # debug_mode=True
    )
    
    # Generate response
    response = assistant.print_response(f"{product_name} Ingredients list", markdown=False)
    
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
