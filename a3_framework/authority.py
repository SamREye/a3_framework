from .agent import A3Agent
from .auditor import A3Auditor
from .logger import log_event
from .config import MAX_LOOPS_DEFAULT
import json

class Authority:
    def __init__(self, agent=None, auditor=None, toolkit_module=None):
        self.agent = agent or A3Agent(toolkit_module=toolkit_module)
        self.auditor = auditor or A3Auditor(toolkit_module=toolkit_module)
        self.max_loops = MAX_LOOPS_DEFAULT
        log_event("INFO", f"Authority initialized with agent: {self.agent.model} and auditor: {self.auditor.model}")
    
    def set_auditor_standard(self, standard):
        log_event("INFO", f"Setting auditor standard: {standard}")
        response = self.auditor.set_standard(standard)
        if not response.is_clear:
            log_event("WARN", f"Auditor standard not clear. Comments: {response.comments}")
            return {"status": "FAIL", "output": response.comments}
        return {"status": "OK", "output": response.comments}

    def set_agent_responsibilities(self, responsibilities):
        log_event("INFO", f"Setting agent responsibilities: {responsibilities}")
        response = self.agent.assign_responsibilities(responsibilities)
        if not response.is_clear:
            log_event("WARN", f"Agent responsibilities not clear. Comments: {response.comments}")
            return {"status": "FAIL", "output": response.comments}
        return {"status": "OK", "output": response.comments}

    def run_task(self, task):
        log_event("INFO", f"Starting task: {task}")
        for attempt in range(self.max_loops):
            output = self.agent.assign_task(task)
            log_event("INFO", f"Agent output: {output}")
            feedback = self.auditor.evaluate(output)
            log_event("INFO", f"Auditor feedback: {feedback}")
            log_event("INFO", f"Attempt {attempt + 1}: {feedback.passed}")
            if feedback.passed:
                return {"status": "OK", "output": output}
        return {"status": "FAIL", "auditor_feedback": feedback.discrepancies, "output": output}
