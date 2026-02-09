import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API key missing")
    parser = argparse.ArgumentParser(description="AI Slop")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.5-flash", contents=messages)
    if response.usage_metadata is None:
        raise RuntimeError("No response :/")
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {(response.usage_metadata.total_token_count - response.usage_metadata.prompt_token_count)} ")
    print(f"Response:\n{response.text}")

if __name__ == "__main__":
    main()
