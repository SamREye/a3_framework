# A³ Framework

A³ (Authority, Agent, Auditor) is a Python library designed to facilitate a structured workflow for task management and evaluation using AI models. The framework integrates with OpenAI's API to perform text-based tasks, providing a seamless Authority → Agent → Auditor loop.

## Features

- **OpenAI Integration**: Utilizes OpenAI's API for generating and evaluating text.
- **Structured Workflow**: Implements a clear Authority → Agent → Auditor process.
- **Logging**: Provides detailed logging to console and file.
- **Configurable Retry Logic**: Allows for customizable retry attempts.
- **Task-Centric**: Designed for discrete tasks with no long-lived sessions.

## Installation

To install the A³ framework, ensure you have Python 3.7 or later, and run:

```bash
pip install git+https://github.com/samreye/a3-framework.git
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

def main():
    task = "Write a short product description including the keyword 'innovative'."
    authority = Authority()
    authority.set_agent_responsibilities("You are a text generation agent.")
    authority.set_auditor_standard("The text should be short and include the keyword 'innovative'. And must be longer than 100 words.")
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

- [Homepage](https://github.com/samreye/a3-framework)
- [Documentation](https://github.com/samreye/a3-framework/docs)
- [Source](https://github.com/samreye/a3-framework)
- [Issue Tracker](https://github.com/samreye/a3-framework/issues) 