# %%
from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo
from phi.llm.groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

# %%
assistant = Assistant(
    llm=Groq(model="llama-3.1-70b-versatile"),
    tools=[DuckDuckGo()],
    description="You are diet research expert and your job is to research and tell the ingredients list along with their composition of any given product in a specific JSON format.",
    instructions=[
        "Provide the response strictly in the following JSON format without any pretextor disclaimer",
        """Required Output format: "{\"product_name\":\"<ProductName>\",\"ingredients\":[{\"name\":\"<Ingredient1>\",\"composition\":\"<X%>\"},{\"name\":\"<Ingredient2>\",\"composition\":\"<Y%>\"}]}" """,
        "Add more ingredients as needed but in a JSON format",
        "dont add any pretext. Only "
    ],
    # debug_mode=True
)
assistant.print_response("Lays Ingredients list", markdown=False)

# %%



