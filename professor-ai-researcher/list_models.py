import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the API key
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=api_key)

# List all available models and their capabilities
print("Available Models and Their Capabilities:")
print("-" * 50)
for model in genai.list_models():
    print(f"Model: {model.name}")
    print(f"Generation Methods: {model.supported_generation_methods}")
    print("-" * 50)