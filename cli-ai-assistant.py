from crewai import Agent, Task, Crew
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
interpreter.auto_run = True  
interpreter.llm.model = config.get("interpreted_model")
interpreter.llm.api_base = config.get("ollama_url")
interpreter.verbose = True
interpreter.llm.max_retries = 20

# initializing open interpreter as a tool
class CLITool:
    @tool('cli-executor')
    def execute_command(command: str):
        """ Execute the command in the terminal """
        print(f">>> Executing command: {command}")
        result = interpreter.chat(command)
        return result


# Initialize the Command Generator Agent
command_generator_agent = Agent(
    role="CLI Command Executor",
    goal=(
        f"Interpret user requests, generate the precise CLI command for this environment ({current_os}), "
        "and execute the command using the provided tools. Return the execution result to the user."
    ),
    backstory=(
        "I am a command-line assistant skilled in understanding natural language instructions, "
        "generating precise terminal commands, and executing them directly in the user's environment. "
        "I support PowerShell for Windows, as well as Bash for Linux."
    ),
    tools=[CLITool.execute_command],    
    llm=llm
)

# Initialize the Crew
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

    # Determine the shell based on the operating system
    shell = "PowerShell" if current_os == "Windows" else "Bash"

    # Create the task description
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

    except Exception as e:
        print(f"An error occurred: {e}")
