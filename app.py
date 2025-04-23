import gradio as gr
from main import TcApp, load_config, format_config_with_entity
import os
import traceback
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def process_tc_request(entity_name):
    """Process the terms and conditions request and return the result"""
    if not entity_name or entity_name.strip() == "":
        return "❌ Please enter a company, product, or service name."
    
    try:
        print(f"Processing request for: {entity_name}")
        
        # Load configurations
        base_dir = os.path.dirname(os.path.abspath(__file__))
        agents_config_path = os.path.join(base_dir, 'config', 'agents.yaml')
        tasks_config_path = os.path.join(base_dir, 'config', 'tasks.yaml')
        
        print(f"Loading configs from: {agents_config_path} and {tasks_config_path}")
        
        agents_config = load_config(agents_config_path)
        tasks_config = load_config(tasks_config_path)
        
        # Format configurations
        formatted_agents_config = format_config_with_entity(agents_config, entity_name)
        formatted_tasks_config = format_config_with_entity(tasks_config, entity_name)
        
        # Set up inputs
        inputs = {
            'entity_name': entity_name
        }
        
        print("Creating TcApp instance...")
        
        # Create TcApp instance
        tc_app = TcApp()
        tc_app.agents_config = formatted_agents_config
        tc_app.tasks_config = formatted_tasks_config
        
        print("Running crew...")
        
        # Run the crew
        result = tc_app.crew().kickoff(inputs=inputs)
        
        print("Crew execution completed")
        
        return f"# 📝 Summary of Terms and Conditions for {entity_name}\n\n{result}"
        
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}\n\n"
        error_msg += "```\n"
        error_msg += traceback.format_exc()
        error_msg += "\n```"
        print(error_msg)
        return error_msg

# Create custom CSS for Helvetica font
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Helvetica+Neue&display=swap');
* {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
}
"""

# Create the Gradio interface
with gr.Blocks(title="Terms & Conditions Assistant", theme=gr.themes.Soft(), css=custom_css) as demo:
    gr.Markdown("# 🤖 Terms & Conditions Assistant")
    gr.Markdown("Enter the name of a company, product, or service to get their terms and conditions summary.")
    
    with gr.Row():
        entity_input = gr.Textbox(
            label="Company/Product/Service Name",
            placeholder="e.g., Netflix, Spotify, Amazon Prime"
        )
        submit_btn = gr.Button("Get Terms & Conditions", variant="primary")
    
    # Add examples
    gr.Examples(
        examples=[
            ["Netflix"],
            ["Spotify"],
            ["Amazon Prime"]
        ],
        inputs=entity_input
    )
    
    output = gr.Markdown(
        label="Results"
    )
    
    submit_btn.click(
        fn=process_tc_request,
        inputs=entity_input,
        outputs=output,
        show_progress=True
    )

# Launch the app
if __name__ == "__main__":
    print("Starting Gradio app...")
    print("Make sure Ollama is running with: ollama serve")
    demo.launch(share=True) 