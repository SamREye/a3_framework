import openai
import os
import inspect
import json

from .logger import log_event

if os.getenv("OPENAI_API_KEY") is None:
    raise ValueError("OPENAI_API_KEY is not set")
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_function_schemas(module):
    functions = []
    for name, func in inspect.getmembers(module, inspect.isfunction):
        if func.__module__ == module.__name__:
            # Only if function name starts with "tool_"
            if not name.startswith("tool_"):
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

def apply_tools(tool_message, toolkit_module):
    messages = []
    formatted_tool_message = {
        "role": "assistant",
        "content": None,
        "tool_calls": [
            {
                "id": tool_call.id,
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments
                },
                "type": "function"
            } for tool_call in tool_message.tool_calls
        ]
    }
    messages.append(formatted_tool_message)
    tool_responses = []
    for tool_call in tool_message.tool_calls:
        tool_id = tool_call.id
        function_name = tool_call.function.name
        arguments = tool_call.function.arguments
        args = json.loads(arguments)
        log_event("INFO", f"Calling tool: {function_name} with arguments: {args}")
        tool_response = getattr(toolkit_module, function_name)(**args)
        tool_msg = {
            "tool_call_id": tool_id,
            "role": "tool",
            "content": json.dumps(tool_response)
        }
        tool_responses.append(tool_msg)
        messages.append(tool_msg)
    return messages

def call_llm(messages, *, model='gpt-4o', response_format=None, toolkit_module=None):
    log_event("INFO", f"Calling LLM: {messages}")
    schemas = []
    if toolkit_module is not None:
        schemas = generate_function_schemas(toolkit_module)
    response = None
    if len(schemas) > 0 and response_format is not None:
        try:
            response = openai_client.beta.chat.completions.parse(
                model=model,
                messages=messages,
                tools=schemas,
                response_format=response_format)
        except Exception as e:
            log_event("ERROR", f"Error: {e}")
            raise e
    elif len(schemas) > 0 and response_format is None:
        try:
            response = openai_client.chat.completions.create(
                model=model,
                messages=messages,
                tools=schemas)
        except Exception as e:
            log_event("ERROR", f"Error: {e}")
            raise e
    elif response_format is not None:
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
            response = openai_client.chat.completions.create(
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

def llm_with_tools_wrapper(messages, *, model='gpt-4o', toolkit_module=None, response_format=None):
    response = call_llm(messages, model=model, toolkit_module=toolkit_module, response_format=response_format)
    if response.choices[0].finish_reason == "tool_calls":
        messages += apply_tools(response.choices[0].message, toolkit_module)
        return llm_with_tools_wrapper(messages, model=model, response_format=response_format, toolkit_module=toolkit_module)
    answer = response.choices[0].message.content
    formatted_response = {"role": "assistant", "content": answer}
    messages.append(formatted_response)
    if response_format is not None:
        myobj = response_format(**json.loads(answer))
        return myobj
    return messages