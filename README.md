
#🤖 Gemini Customer Service Agent (Kaggle Edition)

This Python project demonstrates the integration of the Google Gemini API within a Kaggle Notebook environment to create a reliable and domain-specific Customer Service Agent.

The agent is powered by the high-performance gemini-2.5-flash model and utilizes Google Search grounding for factual, up-to-date responses.

✨ Features

    Custom Persona: Uses a System Instruction to enforce a professional, empathetic, and concise customer service persona, ensuring consistent brand communication.

    Factual Grounding: Leverages the Gemini API's integrated Google Search Tool to provide responses grounded in real-time, external data.

    Source Citation: Extracts and displays the exact web sources (title and uri) used by the model, allowing for transparent fact-checking.

    Reliable API Calls: Implements an Exponential Backoff mechanism to gracefully handle network errors and improve call reliability.

    Secure Secrets Management: Demonstrates the best practice for securely handling API keys on Kaggle using kaggle_secrets.

⚙️ How It Works

The core functionality is handled by the generate_content function, which performs the following steps:

    Authentication: Loads the GEMINI_API_KEY securely from the Kaggle environment.

    Payload Construction: Creates a JSON payload that includes the user's prompt, activates the Google Search tool, and injects the Customer Service System Instruction.

    API Request: Makes a robust HTTP POST request to the Gemini model endpoint.

    Parsing: Extracts the generated text and the associated groundingAttributions (sources) from the API response.

🚀 Getting Started (Kaggle Environment)

To run this project, you need a Kaggle account and a Gemini API Key.

Prerequisites

    Google AI Studio API Key: Get your key from Google AI Studio.

    Kaggle Secret: In your Kaggle Notebook, go to Add-ons -> Secrets and set a new secret with the name GEMINI_API_KEY and your key as the value.

Usage

    Run the Notebook: Execute all cells in the Kaggle Notebook.

    Enter Prompt: When prompted, enter a typical customer question (e.g., "I need to return an item, what's the process?").

    Review Output: The agent will respond using the defined persona, and the grounding sources will be listed below for validation.

Python

# Example of the system instruction used to define the agent's persona
SYSTEM_INSTRUCTION = (
    "You are 'Gemini Support,' an expert customer service agent for a global e-commerce company. "
    "Your tone must be professional, empathetic, and concise. ..."
)

📝 Code Structure

File/Function	Description
main()	Handles user input, defines the agent's persona, and prints the final output.
generate_content()	Core function responsible for making the API call, implementing exponential backoff, and parsing the response and sources.
API_KEY	Global variable holding the securely loaded Gemini API Key.
MODEL_URL	Specifies the REST endpoint for the gemini-2.5-flash-preview-09-2025 model.
