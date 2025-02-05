from a3_framework.authority import Authority
import a3_framework.sample_tools

def main():
    task = "Write a short product description including the keyword 'innovative' in reverse."
    authority = Authority(toolkit_module=a3_framework.sample_tools)
    authority.set_agent_responsibilities("You are a text generation agent. You generate a message based on the task, then you reverse it using a tool.")
    authority.set_auditor_standard("The text should be short and include the keyword 'innovative'. And should be reversed.")
    result = authority.run_task(task)
    print(result)

if __name__ == "__main__":
    main() 