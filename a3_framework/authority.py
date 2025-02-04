from .agent import A3Agent
from .auditor import A3Auditor
from .logger import log_event
from .config import MAX_LOOPS_DEFAULT

class Authority:
    def __init__(self, agent=None, auditor=None):
        self.agent = agent or A3Agent()
        self.auditor = auditor or A3Auditor()
        self.max_loops = MAX_LOOPS_DEFAULT
        log_event("INFO", f"Authority initialized with agent: {self.agent.model} and auditor: {self.auditor.model}")
    
    def set_auditor_standard(self, standard):
        log_event("INFO", f"Setting auditor standard: {standard}")
        response = self.auditor.set_standard(standard)
        response_obj = response.choices[0].message.parsed
        if not response_obj.is_clear:
            log_event("WARN", f"Auditor standard not clear. Comments: {response_obj.comments}")
            return {"status": "FAIL", "output": response_obj.comments}
        return {"status": "OK", "output": response_obj.comments}

    def set_agent_responsibilities(self, responsibilities):
        log_event("INFO", f"Setting agent responsibilities: {responsibilities}")
        response = self.agent.assign_responsibilities(responsibilities)
        response_obj = response.choices[0].message.parsed
        if not response_obj.is_clear:
            log_event("WARN", f"Agent responsibilities not clear. Comments: {response_obj.comments}")
            return {"status": "FAIL", "output": response_obj.comments}
        return {"status": "OK", "output": response_obj.comments}

    def run_task(self, task):
        log_event("INFO", f"Starting task: {task}")
        for attempt in range(self.max_loops):
            output = self.agent.assign_task(task)
            feedback = self.auditor.evaluate(output)
            feedback_obj = feedback.choices[0].message.parsed
            log_event("INFO", f"Attempt {attempt + 1}: {feedback_obj.passed}")
            if feedback_obj.passed:
                return {"status": "OK", "output": output}
        return {"status": "FAIL", "auditor_feedback": feedback_obj.discrepancies, "output": output}
