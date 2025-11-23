# ... (Initial imports and setup remain the same) ...

import requests
import json
import time

# --- API Key Configuration (This section is unchanged from the fix) ---
from kaggle_secrets import UserSecretsClient
user_secrets = UserSecretsClient()
secret_value_0 = user_secrets.get_secret("GEMINI_API_KEY")
API_KEY = secret_value_0 # The fix from the previous step

MODEL_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"

def generate_content(prompt, system_instruction=None, max_retries=3):
    """
    Calls the Gemini API to generate content based on the prompt using 
    exponential backoff for reliability.
    """
    headers = {'Content-Type': 'application/json'}
    
    # Construct the base payload
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        # Use Google Search grounding for up-to-date and factual responses
        "tools": [{"google_search": {}}] 
    }

    # 🚀 KEY CHANGE: Add system instruction to the payload if provided
    if system_instruction:
        # The system instruction defines the agent's persona and rules
        payload["config"] = {"systemInstruction": system_instruction} # Note: The structure for systemInstruction has been updated in some API versions to be within 'config'
                                                                    # However, based on the search result snippet 1.2, for REST API, it is often a top-level field or within a config object. 
                                                                    # We will use the common approach of passing it via the function argument and defining it in the payload.
        # Reworking to match the common python usage (often as a config key or top-level field depending on SDK/API version)
        # Using the systemInstruction parameter outside of the main contents list is the standard way to set persona.
        payload["systemInstruction"] = system_instruction # Setting it as a top-level key for a standard REST payload


    print("--- Calling Gemini API ---")
    
    for attempt in range(max_retries):
        try:
            # Append API key to URL for the request
            url = f"{MODEL_URL}?key={API_KEY}"
            
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

            # ... (Rest of the response parsing remains the same) ...
            result = response.json()
            candidate = result.get('candidates', [{}])[0]
            generated_text = candidate.get('content', {}).get('parts', [{}])[0].get('text', 'No content generated.')
            
            # Extract and format grounding sources
            sources = []
            grounding_metadata = candidate.get('groundingMetadata', {})
            attributions = grounding_metadata.get('groundingAttributions', [])
            
            for attr in attributions:
                web = attr.get('web', {})
                if web:
                    sources.append(f" - {web.get('title', 'Untitled')} ({web.get('uri', 'No URI')})")
            
            return generated_text, sources
            
        except requests.exceptions.RequestException as e:
            # ... (Error handling remains the same) ...
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
    """
    Main function to handle user input and display output, now including
    a specific customer service persona.
    """
    print("Welcome to the Gemini Customer Service Agent.")
    
    if not API_KEY and not os.environ.get("GEMINI_API_KEY"):
         print("Warning: API Key is not set. This script relies on the execution environment to inject the key.")

    # 🤖 NEW: Define the Customer Service Agent Persona
    SYSTEM_INSTRUCTION = (
        "You are 'Gemini Support,' an expert customer service agent for a global e-commerce company. "
        "Your tone must be **professional, empathetic, and concise**. "
        "Your mission is to resolve issues quickly and efficiently. "
        "Always start by greeting the customer and asking how you can help. "
        "If you cannot find a definitive answer, politely explain that you need to escalate the issue "
        "to a human specialist and provide them with a reference number (e.g., REF-4912)."
    )
    
    # Print the persona so the user knows the context
    print("\n--- Agent Persona ---")
    print(SYSTEM_INSTRUCTION)
    print("---------------------\n")
        
    # Get the user's prompt (the customer's question)
    user_prompt = input("Enter the customer's question (e.g., 'Where is my order?'):\n> ")
    
    if not user_prompt.strip():
        print("Prompt cannot be empty. Exiting.")
        return
 
    # 🔑 KEY CHANGE: Pass the SYSTEM_INSTRUCTION to the generate_content function
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
