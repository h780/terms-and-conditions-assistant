import warnings
warnings.filterwarnings("ignore", message="<built-in function callable> is not a Python type")
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
import yaml
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class TcApp():
    """TcApp crew for retrieving and summarizing terms and conditions documents"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def load_config(self, config_path):
        """Load a YAML configuration file."""
        # If config_path is already a dictionary, return it
        if isinstance(config_path, dict):
            return config_path
            
        # Otherwise, load from file
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        # Get the configuration directly or load it from file
        config = self.agents_config if isinstance(self.agents_config, dict) else self.load_config(self.agents_config)
        researcher_config = config['researcher']
        
        # Create tools with API key
        serper_tool = SerperDevTool(api_key=os.getenv('SERPER_API_KEY'))
        scrape_tool = ScrapeWebsiteTool()
        
        # Ensure the config is a dictionary with the required fields
        if isinstance(researcher_config, dict):
            return Agent(
                role=researcher_config.get('role', ''),
                goal=researcher_config.get('goal', ''),
                backstory=researcher_config.get('backstory', ''),
                allow_delegation=researcher_config.get('allow_delegation', False),
                verbose=False,  # Set to False to reduce output
                tools=[serper_tool, scrape_tool]
            )
        else:
            # If it's not a dictionary, use it as a role
            return Agent(
                role=str(researcher_config),
                tools=[serper_tool, scrape_tool],
                verbose=False  # Set to False to reduce output
            )

    @agent
    def reporting_analyst(self) -> Agent:
        # Get the configuration directly or load it from file
        config = self.agents_config if isinstance(self.agents_config, dict) else self.load_config(self.agents_config)
        analyst_config = config['reporting_analyst']
        
        # Ensure the config is a dictionary with the required fields
        if isinstance(analyst_config, dict):
            return Agent(
                role=analyst_config.get('role', ''),
                goal=analyst_config.get('goal', ''),
                backstory=analyst_config.get('backstory', ''),
                allow_delegation=analyst_config.get('allow_delegation', False),
                verbose=False  # Set to False to reduce output
            )
        else:
            # If it's not a dictionary, use it as a role
            return Agent(
                role=str(analyst_config),
                verbose=False  # Set to False to reduce output
            )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        # Get the configuration directly or load it from file
        config = self.tasks_config if isinstance(self.tasks_config, dict) else self.load_config(self.tasks_config)
        task_config = config['research_task']
        
        # Ensure the config is a dictionary with the required fields
        if isinstance(task_config, dict):
            return Task(
                description=task_config.get('description', ''),
                expected_output=task_config.get('expected_output', ''),
                agent=self.researcher()
            )
        else:
            # If it's not a dictionary, use it as a description
            return Task(
                description=str(task_config),
                agent=self.researcher()
            )

    @task
    def reporting_task(self) -> Task:
        # Get the configuration directly or load it from file
        config = self.tasks_config if isinstance(self.tasks_config, dict) else self.load_config(self.tasks_config)
        task_config = config['reporting_task']
        
        # Ensure the config is a dictionary with the required fields
        if isinstance(task_config, dict):
            return Task(
                description=task_config.get('description', ''),
                expected_output=task_config.get('expected_output', ''),
                agent=self.reporting_analyst(),
                output_file='report.md'
            )
        else:
            # If it's not a dictionary, use it as a description
            return Task(
                description=str(task_config),
                agent=self.reporting_analyst(),
                output_file='report.md'
            )

    @crew
    def crew(self) -> Crew:
        """Creates the TcApp crew for terms and conditions retrieval and summarization"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=False,  # Set to False to reduce output
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
