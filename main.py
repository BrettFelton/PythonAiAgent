import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions
from prompts import system_prompt

def main():
    parser = argparse.ArgumentParser(description="AI Agent Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    generate_content(client, messages, args)

def generate_content(client, messages, args):
    response = client.models.generate_content(
        #model = "gemini-2.5-flash",
        model = "gemini-3.1-flash-lite-preview",
        contents = messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0,
            tools=[available_functions],
        )
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if not response.function_calls:
        print("Response:")
        print(response.text)
        return

    for function_call in response.function_calls: 
        print(f"Calling function: {function_call.name}({function_call.args})")

if __name__ == "__main__":
    main()
