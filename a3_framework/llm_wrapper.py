import openai
import os
import inspect
import json

from .logger import log_event

if os.getenv("OPENAI_API_KEY") is None:
    raise ValueError("OPENAI_API_KEY is not set")
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_function_schemas(module, usable_tools):
    functions = []
    for name, func in inspect.getmembers(module, inspect.isfunction):
        if func.__module__ == module.__name__:
            if name not in usable_tools:
                continue
            params = inspect.signature(func).parameters
            properties = {param: {"type": "string"} for param in params}
            function = {
                "type": "function",
                "function": {
                    "name": name,
                    "description": func.__doc__ or "No description available.",
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": list(params.keys()),
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
            functions.append(function)
    return functions

# def apply_tools(tool_message):
#     messages = []
#     formatted_tool_message = {
#         "role": "assistant",
#         "content": None,
#         "tool_calls": [
#             {
#                 "id": tool_call.id,
#                 "function": {
#                     "name": tool_call.function.name,
#                     "arguments": tool_call.function.arguments
#                 },
#                 "type": "function"
#             } for tool_call in tool_message.tool_calls
#         ]
#     }
#     messages.append(formatted_tool_message)
#     tool_responses = []
#     for tool_call in tool_message.tool_calls:
#         tool_id = tool_call.id
#         function_name = tool_call.function.name
#         arguments = tool_call.function.arguments
#         args = json.loads(arguments)
#         tool_response = getattr(tools, function_name)(**args)
#         tool_msg = {
#             "tool_call_id": tool_id,
#             "role": "tool",
#             "content": json.dumps(tool_response)
#         }
#         tool_responses.append(tool_msg)
#         messages.append(tool_msg)
#     return messages

def call_llm(messages, *, model='gpt-4o', usable_tools=[], response_format=None):
    log_event("INFO", f"Calling LLM: {messages}")
    # schemas = generate_function_schemas(tools, usable_tools)
    response = None
    # if len(schemas) > 0 and response_format is not None:
    #     try:
    #         response = openai_client.beta.chat.completions.parse(
    #             model=model,
    #             messages=messages,
    #             tools=schemas,
    #             response_format=response_format)
    #     except Exception as e:
    #         log_event("ERROR", f"Error: {e}")
    #         raise e
    # elif len(schemas) > 0 and response_format is None:
    #     try:
    #         response = openai_client.beta.chat.completions.parse(
    #             model=model,
    #             messages=messages,
    #             tools=schemas)
    #     except Exception as e:
    #         log_event("ERROR", f"Error: {e}")
    #         raise e
    # el
    if response_format is not None:
        try:
            response = openai_client.beta.chat.completions.parse(
                model=model,
                messages=messages,
                response_format=response_format)
        except Exception as e:
            log_event("ERROR", f"Error: {e}")
            raise e
    elif response_format is None:
        try:
            response = openai_client.beta.chat.completions.parse(
                model=model,
                messages=messages)
        except Exception as e:
            log_event("ERROR", f"Error: {e}")
            raise e
    else:
        log_event("ERROR", "Invalid arguments")
        raise ValueError("Invalid arguments")
    log_event("INFO", f"Response: {response}")
    return response

# def llm_wrapper(formatted_message, *, model='gpt-4o', usable_tools=[], response_format=None):
#     messages = [formatted_message]
#     response = call_llm(messages, model, usable_tools, response_format)
#     if response.choices[0].finish_reason == "tool_calls":
#         messages += apply_tools(response.choices[0].message)
#         return llm_wrapper(messages, response_format)
#     answer = response.choices[0].message.content
#     formatted_response = {"role": "assistant", "content": answer}
#     messages.append(formatted_response)
#     return messages