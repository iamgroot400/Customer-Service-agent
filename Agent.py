import requests
import json
import time


from kaggle_secrets import UserSecretsClient
user_secrets = UserSecretsClient()
secret_value_0 = user_secrets.get_secret("GEMINI_API_KEY")
API_KEY = secret_value_0

MODEL_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"

def generate_content(prompt, system_instruction=None, max_retries=3):
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}]
    }

    if system_instruction:
        payload["config"] = {"systemInstruction": system_instruction}
        payload["systemInstruction"] = system_instruction


    print("--- Calling Gemini API ---")
    
    for attempt in range(max_retries):
        try:
            url = f"{MODEL_URL}?key={API_KEY}"
            
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()

            result = response.json()
            candidate = result.get('candidates', [{}])[0]
            generated_text = candidate.get('content', {}).get('parts', [{}])[0].get('text', 'No content generated.')
            
            sources = []
            grounding_metadata = candidate.get('groundingMetadata', {})
            attributions = grounding_metadata.get('groundingAttributions', [])
            
            for attr in attributions:
                web = attr.get('web', {})
                if web:
                    sources.append(f" - {web.get('title', 'Untitled')} ({web.get('uri', 'No URI')})")
            
            return generated_text, sources
            
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                delay = 2 ** attempt
                print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Failed to generate content after {max_retries} attempts.")
                print(f"Error: {e}")
                return "An error occurred while connecting to the API.", []
        except json.JSONDecodeError:
            print("API response was not valid JSON.")
            return "Failed to parse API response.", []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "An unexpected error occurred.", []


def main():
    print("Welcome to the Gemini Customer Service Agent.")
    
    if not API_KEY and not os.environ.get("GEMINI_API_KEY"):
           print("Warning: API Key is not set. This script relies on the execution environment to inject the key.")

    SYSTEM_INSTRUCTION = (
        "You are 'Gemini Support,' an expert customer service agent for a global e-commerce company. "
        "Your tone must be **professional, empathetic, and concise**. "
        "Your mission is to resolve issues quickly and efficiently. "
        "Always start by greeting the customer and asking how you can help. "
        "If you cannot find a definitive answer, politely explain that you need to escalate the issue "
        "to a human specialist and provide them with a reference number (e.g., REF-4912)."
    )
    
    print("\n--- Agent Persona ---")
    print(SYSTEM_INSTRUCTION)
    print("---------------------\n")
        
    user_prompt = input("Enter the customer's question (e.g., 'Where is my order?'):\n> ")
    
    if not user_prompt.strip():
        print("Prompt cannot be empty. Exiting.")
        return
    
    generated_text, sources = generate_content(user_prompt, system_instruction=SYSTEM_INSTRUCTION)

    print("\n" + "="*50)
    print("GENERATED RESPONSE (Customer Service Agent)")
    print("="*50)
    print(generated_text)
    print("="*50)

    if sources:
        print("\nGROUNDING SOURCES (Google Search)")
        for source in sources:
            print(source)
        print("="*50)

if __name__ == "__main__":
    main()
