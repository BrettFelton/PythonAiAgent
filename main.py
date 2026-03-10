import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from config import MAX_ITERS
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

    for _ in range(MAX_ITERS):
        try:
            final_response = generate_content(client, messages, args)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"Maximum iterations ({MAX_ITERS}) reached")
    sys.exit(1)

def generate_content(client, messages, args):
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        #model = "gemini-2.5-flash-lite",
        #model = "gemini-3.1-flash-lite-preview",
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
    
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call in response.function_calls:
        result = call_function(function_call, args.verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}")
        if args.verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_responses.append(result.parts[0])
    
    messages.append(types.Content(role="user", parts=function_responses))

if __name__ == "__main__":
    main()
