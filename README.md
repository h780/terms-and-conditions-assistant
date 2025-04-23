# Terms & Conditions Assistant

A web-based application that helps users understand terms and conditions for various companies, products, and services.

## Features

- Simple web interface for entering company/product/service names
- Automated analysis of terms and conditions
- Clean, formatted summary of key points
- Example inputs for quick testing

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Make sure you have Ollama installed and running with the llama2 model:
   ```
   ollama pull llama2
   ollama serve
   ```
4. Set up your environment variables:
   - Copy the `.env.example` file to a new file named `.env`:
     ```
     cp .env.example .env
     ```
   - Edit the `.env` file and replace the placeholder values with your actual API keys and configuration

## Environment Variables

The following environment variables are required:

- `MODEL`: The Ollama model to use (default: `ollama/llama2`)
- `API_BASE_URL`: The base URL for the Ollama API (default: `http://localhost:11434/v1`)
- `SERPER_API_KEY`: Your Serper API key for web search functionality
- `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI models)

## Usage

1. Start the Gradio web interface:
   ```
   python app.py
   ```
2. Open the provided URL in your web browser
3. Enter a company, product, or service name in the input field
4. Click "Get Terms & Conditions" to generate a summary
5. View the formatted results in the output area

## Example Inputs

The app includes example inputs for:
- Netflix
- Spotify
- Amazon Prime

You can use these examples to quickly test the application.

## Troubleshooting

- If you encounter connection errors, ensure Ollama is running with `ollama serve`
- For API key errors, check that your `.env` file is properly configured
- If the app doesn't start, verify all dependencies are installed correctly

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and don't share them publicly
- The `.gitignore` file is configured to exclude sensitive files

## Project Structure

```
tc_assistant_app/
├── config/              # Configuration files for agents and tasks
│   ├── agents.yaml      # Agent definitions
│   └── tasks.yaml       # Task definitions
├── tools/               # Custom tools for the agents
├── crew.py              # CrewAI crew definition
├── main.py              # Main application entry point
├── app.py               # Gradio web interface
├── utils.py             # Utility functions
├── .env.example         # Example environment variables (safe to commit)
├── .gitignore           # Git ignore file
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## License

[MIT License](LICENSE)
