from crewai import Agent, Task, Crew, Process
from interpreter import interpreter
from langchain.tools import tool
import platform
import json


# Detect the current operating system
current_os = platform.system()

# load the config file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# llm and interpreter config
llm = config.get("llm_model")
interpreter.offline = True
interpreter.auto_run = False  
interpreter.llm.model = config.get("interpreted_model")
interpreter.llm.api_base = config.get("ollama_url")
interpreter.verbose = True
interpreter.llm.max_retries = 20

# Initialize the Command Generator Agent (first agent)
command_generator_agent = Agent(
    role="CLI Command Generator",
    goal="interpret user requests and generate the precise CLI command based on the shell environment",
    backstory="I am a command-line assistant skilled in understanding natural language instructions and converting them into precise terminal commands for different shell environments (CMD, PowerShell for Windows, Bash for Linux/macOS). I provide only the command, with no extra explanation or execution.",
    llm="ollama/llama3.2"
)

crew = Crew(
    agents=[command_generator_agent],
    tasks=[],
    verbose=True,
)

print("Welcome to your Command Line Assistant! Type your prompt below (type 'quit' to exit):")

while True:
    # Get user input
    user_input = input(">>> ")

    # Check for exit condition
    if user_input.lower() in ["quit", "exit", "q", "bye"]:
        print("Goodbye!")
        break

    
    shell = "PowerShell" if current_os == "Windows" else "Bash"

    task_description = (
            f"Given the following user prompt: '{user_input}', provide the precise CLI command in {shell} for the detected operating system ({current_os})."
        )

    # Create a user task
    user_task = Task(
        description=task_description,
        expected_output="The precise CLI command, without any extra text.",
        agent=command_generator_agent,
    )

    try:
        # Add the task to the crew and execute it
        crew.tasks = [user_task]
        result = crew.kickoff()

        # Print the generated command
        print(f"Generated Command: {result}")

        # Interpret the generated command
        interpreter.chat(str(result) + f'on the {current_os} os')
    
    except Exception as e:
        print(f"An error occurred: {e}")
