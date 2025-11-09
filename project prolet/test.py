from google.generativeai import configure, list_models
import os
from dotenv import load_dotenv

# Load your API key
load_dotenv()
configure(api_key=os.getenv("GEMINI_API_KEY"))

print("🔍 Checking available models for your API key...\n")

# List all available models
for model in list_models():
    name = model.name
    methods = model.supported_generation_methods
    version = "v1" if "v1" in str(model) else "v1beta"  # rough guess
    
    print(f"✅ Model: {name}")
    print(f"   Supported methods: {methods}")
    print(f"   Likely API version: {version}")
    print("-" * 50)