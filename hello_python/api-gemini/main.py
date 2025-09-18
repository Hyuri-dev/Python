from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

consulta = input("Ingrese su consulta: ")

client = genai.Client(api_key=os.environ.get("API_KEY"))

response = client.models.generate_content(
    model= "gemini-2.5-flash", contents = consulta
)

print(response.text)