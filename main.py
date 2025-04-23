#!/usr/bin/env python
import sys
import warnings
import yaml
import os
from datetime import datetime
from dotenv import load_dotenv
from crew import TcApp
from utils import extract_entity_name, format_config_with_entity
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory

# Load environment variables from .env file
load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def load_config(config_path):
    """
    Load a YAML configuration file.
    
    Args:
        config_path: Path to the YAML configuration file
        
    Returns:
        The loaded configuration as a dictionary
    """
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def get_user_input(prompt_text):
    """
    Get user input with proper line editing support using prompt_toolkit.
    
    Args:
        prompt_text: The prompt to display to the user
        
    Returns:
        The user's input as a string
    """
    try:
        # Create a history object to store input history
        history = InMemoryHistory()
        
        # Get input from user with prompt_toolkit
        user_input = prompt(prompt_text, history=history)
        return user_input.strip()
    except Exception as e:
        print(f"Error getting input: {e}")
        return ""

def run():
    """
    Run the crew with user input for terms and conditions.
    """
    # Get user input with proper line editing support
    user_input = get_user_input("What terms and conditions would you like to find? ")
    
    # Extract the entity name from user input
    entity_name = extract_entity_name(user_input)
    
    if not entity_name:
        print("I couldn't identify which company, product, or service you're interested in.")
        print("Please try again with a more specific request, like:")
        print("  - What are the terms and conditions for Netflix?")
        print("  - Show me the T&C for Spotify")
        print("  - I need the terms for Amazon Prime")
        return
    
    print(f"\n🔍 Finding terms and conditions for: {entity_name}")
    print("⏳ This may take a few moments...\n")
    
    # Load the configuration files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    agents_config_path = os.path.join(base_dir, 'config', 'agents.yaml')
    tasks_config_path = os.path.join(base_dir, 'config', 'tasks.yaml')
    
    agents_config = load_config(agents_config_path)
    tasks_config = load_config(tasks_config_path)
    
    # Format the configurations with the entity name
    formatted_agents_config = format_config_with_entity(agents_config, entity_name)
    formatted_tasks_config = format_config_with_entity(tasks_config, entity_name)
    
    # Set up inputs for the crew
    inputs = {
        'entity_name': entity_name
    }
    
    try:
        # Create a temporary TcApp instance with the formatted configurations
        tc_app = TcApp()
        tc_app.agents_config = formatted_agents_config
        tc_app.tasks_config = formatted_tasks_config
        
        # Run the crew
        result = tc_app.crew().kickoff(inputs=inputs)
        
        # Print the result in a nice format
        print("\n📝 Summary of Terms and Conditions:")
        print("=" * 50)
        print(result)
        print("=" * 50)
        print("\n💡 Note: This is a summary of the key points. Please refer to the original document for complete details.")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "entity_name": "Example Company"
    }
    try:
        # Create a TcApp instance with the default configuration paths
        tc_app = TcApp()
        
        # Run the training
        tc_app.crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        # Create a TcApp instance with the default configuration paths
        tc_app = TcApp()
        
        # Run the replay
        tc_app.crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "entity_name": "Example Company",
        "current_year": str(datetime.now().year)
    }
    try:
        # Create a TcApp instance with the default configuration paths
        tc_app = TcApp()
        
        # Run the test
        tc_app.crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
