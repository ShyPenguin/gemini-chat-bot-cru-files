import os, sys
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import Client, types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Gemini API Key Not Found")


    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()


    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for i in range(10):
        response = generate_content(client, messages,args.verbose)
        if response:
            sys.exit(0)
            break
        if i == 10:
            print(f"Something went wrong")
    sys.exit(1)

def generate_content(client: Client, messages: list[types.Content], verbose: bool):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        print("Response:")
        print(response.text)
        return "Success"

    function_responses = []
    for function_call in response.function_calls:
        result = call_function(function_call, verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_responses.append(result.parts[0])
    messages.append(types.Content(role="user", parts=function_responses))

if __name__ == "__main__":
    main()


# def in_session():
#     response = client.models.generate_content(
#         model='gemini-2.5-flash',
#         contents=messages,
#         config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
#     )

#     if response.usage_metadata == None:
#         raise RuntimeError("usage_metadata was not accessable")

#     results = []
#     if response.function_calls != None:
#         for function_call in response.function_calls:
#             function_call_result = call_function(function_call)

#             parts_result = function_call_result.parts
#             if len(parts_result) < 1:
#                 raise Exception(f"Error: parts should be non-empty")
#             if not isinstance(parts_result[0].function_response, types.FunctionResponse):
#                 raise Exception(f"Error: function_response should be type FunctionResponse")
#             if parts_result[0].function_response.response == None:
#                 raise Exception("Error: response of function_response shouldn't be None")
            
#             results.append(parts_result[0])
#             function
#             if args.verbose:
#                 print(f"-> {function_call_result.parts[0].function_response.response}")
            
#             messages.append(types.Content(role="user", parts=parts_result[0].function_response.response))
