from a3_framework.authority import Authority

def main():
    task = "Write a short product description including the keyword 'innovative'."
    authority = Authority()
    authority.set_agent_responsibilities("You are a text generation agent.")
    authority.set_auditor_standard("The text should be short and include the keyword 'innovative'. And must be longer than 500 words.")
    result = authority.run_task(task)
    print(result)

if __name__ == "__main__":
    main() 