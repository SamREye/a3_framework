# ![A³ Framework Logo](a3-logo.png)

# A³ Framework

A³ (Authority, Agent, Auditor) is a Python library designed to facilitate a structured workflow for task management and evaluation using AI models. The framework integrates with OpenAI's API to perform text-based tasks, providing a seamless Authority → Agent → Auditor loop.

Read the [manifesto](https://agentdeployer.com/blog/a3-manifesto)

## Features

- **OpenAI Integration**: Utilizes OpenAI's API for generating and evaluating text.
- **Structured Workflow**: Implements a clear Authority → Agent → Auditor process.
- **Logging**: Provides detailed logging to console and file.
- **Configurable Retry Logic**: Allows for customizable retry attempts.
- **Task-Centric**: Designed for discrete tasks with no long-lived sessions.
- **Tool Integration**: Extend functionality by creating custom tools.

## Installation

To install the A³ framework, ensure you have Python 3.7 or later, and run:

```bash
pip install git+https://github.com/samreye/a3_framework.git
```

## Usage

### Setting Up

Before using the library, set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

### Example Script

Here's a basic example demonstrating how to use the A³ framework:

```python
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
```

### Creating Custom Tools

You can extend the A³ framework by creating custom tools. Tools are Python functions that start with `tool_` and can be used by the Agent or Auditor during task execution. Here's how you can create and use a custom tool:

1. **Define a Tool Function**: Create a Python function in your module. The function name must start with `tool_`.

   ```python
   # my_tools.py
   def tool_reverse_text(text):
       """Reverses the given text."""
       return text[::-1]
   ```

2. **Import and Use the Tool**: Import your module and pass it to the `Authority` class.

   ```python
   from a3_framework.authority import Authority
   import my_tools

   def main():
       task = "Write a short product description including the keyword 'innovative' in reverse."
       authority = Authority(toolkit_module=my_tools)
       authority.set_agent_responsibilities("You are a text generation agent. You generate a message based on the task, then you reverse it using a tool.")
       authority.set_auditor_standard("The text should be short and include the keyword 'innovative'. And should be reversed.")
       result = authority.run_task(task)
       print(result)

   if __name__ == "__main__":
       main()
   ```

### Running the Example

To run the example script, navigate to the `examples` directory and execute:

```bash
python text_generation_demo.py
```

## Project Structure

```
a3_framework/
├── __init__.py
├── authority.py
├── agent.py
├── auditor.py
├── logger.py
├── config.py
├── exceptions.py
├── llm_wrapper.py
└── ...
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact Samuel Bourque at [me@sambourque.com](mailto:me@sambourque.com).

## Links

- [Homepage](https://github.com/samreye/a3_framework)
- [Source](https://github.com/samreye/a3_framework)
- [Issue Tracker](https://github.com/samreye/a3_framework/issues) 