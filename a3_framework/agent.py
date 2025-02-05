from .llm_wrapper import llm_with_tools_wrapper
from pydantic import BaseModel

class ResponsibilityAssignment(BaseModel):
    comments: str
    is_clear: bool

class A3Agent:
    def __init__(self, model='gpt-4o', toolkit_module=None):
        self.model = model
        self.responsibilities = ""
        self.session = [{
            "role": "system",
            "content": "You are an AI agent that will be tasked to perform tasks for the user."
        }]
        self.toolkit_module = toolkit_module

    def assign_responsibilities(self, responsibilities):
        self.responsibilities = responsibilities
        self.session.append({
            "role": "user",
            "content": f"You are tasked with the following responsibilities:\n\n[RESPONSIBILITIES]\n{self.responsibilities}[/RESPONSIBILITIES]. Do you have any clarifying questions? Is your responsibility clear?"
        })
        response = llm_with_tools_wrapper(self.session, model=self.model, response_format=ResponsibilityAssignment, toolkit_module=self.toolkit_module)
        return response

    def assign_task(self, task):
        formatted_message = {
            "role": "user",
            "content": task
        }
        self.session.append(formatted_message)
        response = llm_with_tools_wrapper(self.session, model=self.model, toolkit_module=self.toolkit_module)
        print(response)
        return response[-1]['content']
    