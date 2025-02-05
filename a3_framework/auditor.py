from .llm_wrapper import llm_with_tools_wrapper
from pydantic import BaseModel

from enum import Enum

class StandardAssignment(BaseModel):
    comments: str
    is_clear: bool

class AuditorFeedback(BaseModel):
    passed: bool
    discrepancies: list[str]

class A3Auditor:
    def __init__(self, model='gpt-4o', toolkit_module=None):
        self.model = model
        self.base_prompt = {
            "role": "system",
            "content": "You are an auditor. You are given an output and you need to evaluate it according to the standard. You need to return a verdict and a list of reasons."
        }
        self.standard_session = [self.base_prompt]
        self.toolkit_module = toolkit_module

    def set_standard(self, standard):
        self.standard = standard
        self.standard_session.append({
            "role": "user",
            "content": f"Here's the standard you need to evaluate against:\n\n[STANDARD]\n{self.standard}\n[/STANDARD]. Do you have any clarifying questions? Is your responsibility clear?"
        })
        response = llm_with_tools_wrapper(self.standard_session, model=self.model, response_format=StandardAssignment, toolkit_module=self.toolkit_module)
        return response

    def evaluate(self, output):
        messages = [
            self.base_prompt,
            {
                "role": "system",
                "content": f"Standard: {self.standard}"
            },
            {
                "role": "user",
                "content": f"Output: {output}"
            }
        ]
        response = llm_with_tools_wrapper(messages, model=self.model, response_format=AuditorFeedback, toolkit_module=self.toolkit_module)
        return response
