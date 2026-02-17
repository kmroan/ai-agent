import os, argparse, config
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions import available_functions

def main():
    parser = argparse.ArgumentParser(description="AI Slop")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("API key missing")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    gen_content(client, messages, args.verbose)
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")


def gen_content(client, messages,verbose):
    response= client.models.generate_content(
        model="gemini-2.5-flash", contents=messages, 
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=config.system_prompt, 
            temperature=0
        ),
    )
    if not response.usage_metadata:
        raise RuntimeError("No response :/")
    
    if verbose:
         print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
         print(f"Response tokens: {(response.usage_metadata.total_token_count - response.usage_metadata.prompt_token_count)} ")

    if not response.function_calls:
        print(f"Response:\n{response.text}")
        return
    
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")

if __name__ == "__main__":
    main()
