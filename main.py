import os, argparse, config
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions import available_functions, call_function

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

    for n in range(20):
        if n == 20:
            raise RuntimeError("maximum number of iterations is reached")

        fin = gen_content(client, messages, args.verbose)
        if fin:
            break
        
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

def gen_content(client, messages, verbose):
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

    if response.candidates:
        for rc in response.candidates:
            messages.append(rc.content)

    if not response.function_calls:
        print(f"Response:\n{response.text}")
        return True
    res = []
    for function_call in response.function_calls:
        func_res = call_function(function_call,verbose)
        if func_res.parts[0].function_response is None:
            raise RuntimeError("Function error occured :/")
        if func_res.parts[0].function_response.response is None:
            raise RuntimeError("Function error: no response? :/")
        res.append(func_res.parts[0])
        if verbose:
            print(f"-> {func_res.parts[0].function_response.response}")
    messages.append(types.Content(role="user", parts=res))
    return False
        
if __name__ == "__main__":
    main()
