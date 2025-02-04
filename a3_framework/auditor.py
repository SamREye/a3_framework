from .llm_wrapper import call_llm
from pydantic import BaseModel

from enum import Enum

class StandardAssignment(BaseModel):
    comments: str
    is_clear: bool

class AuditorFeedback(BaseModel):
    passed: bool
    discrepancies: list[str]

class A3Auditor:
    def __init__(self, model='gpt-4o'):
        self.model = model
        self.base_prompt = {
            "role": "system",
            "content": "You are an auditor. You are given an output and you need to evaluate it according to the standard. You need to return a verdict and a list of reasons."
        }
        self.standard_session = [self.base_prompt]

    def set_standard(self, standard):
        self.standard = standard
        self.standard_session.append({
            "role": "user",
            "content": f"Here's the standard you need to evaluate against:\n\n[STANDARD]\n{self.standard}\n[/STANDARD]. Do you have any clarifying questions? Is your responsibility clear?"
        })
        response = call_llm(self.standard_session, model=self.model, response_format=StandardAssignment)
        return response

    def evaluate(self, output):
        messages = [
            self.base_prompt,
            {
                "role": "system",
                "content": f"Standard: {self.standard}"
            },
            output
        ]
        response = call_llm(self.standard_session, model=self.model, response_format=AuditorFeedback)
        return response
