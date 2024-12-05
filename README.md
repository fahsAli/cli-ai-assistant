# cli-ai-assistant
cli-ai-assistant is an intelligent command-line assistant powered by AI. It is designed to interpret natural language instructions and convert them into precise shell commands, which can then be executed using the Open Interpreter. The assistant is capable of adapting to different operating systems (PowerShell for Windows, Bash for Linux) and is capable of performing various tasks based on user input.

## Features
* **AI-Powered Command Generation:** Uses an AI model (e.g., Ollama's mistral) to interpret natural language input and generate shell commands for both Windows and Linux
* **Interactive CLI Interface:** Prompts the user to input commands and executes them on the corresponding shell environment.
* **Task Management:** Integrates with CrewAI to manage tasks, agents, and processes.

## Dependencies
To run the project, you need to install the following dependencies:

**Open Interpreter**
```bash
    pip install open-interpreter
```

**CrewAI**
```bash
    pip install crewai 'crewai[tools]'
```

**Langchain**
```bash
    pip install langchain
    pip install langchain[tools]
```

**ollama**
You will need to set up Ollama locally, which can be installed [here](https://ollama.com/)

```bash
    ollama start
```

## configuration
Before running the assistant, make sure to set up the configuration file (config.json). Here's an example configuration:

```json
{
  "llm_model": "ollama/codestral",
  "interpreted_model": "ollama_chat/codestral",
  "ollama_url": "http://localhost:11434"
}
```

### AI Model Customization
This project uses codestral as the default AI model, but you can easily switch to other models for better performance.

To install a different model, run:

```bash
    ollama pull <model_name>
```

## Running the Assistant
```bash
    python cli-ai-assistant.py
```

## Future Improvements
* **Memory for Agents:** Enable agents to remember past interactions and improve their responses over time.
* **Multi-Agent and Multi-Model Support:** Implement a system where multiple agents and models can work together for more complex tasks.
* **User Interface:** Develop a user-friendly interface for easier interaction with the system.
* **Model Performance:** Explore and integrate additional models to enhance performance and efficiency.
