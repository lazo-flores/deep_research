---
title: deep_research
app_file: deep_research.py
sdk: gradio
sdk_version: 5.49.1
---
# Deep Research

AI Agents that research a given topic, generate a report in markdown, and email it to the user.

## Features

- 🔍 Automated web research using OpenAI agents
- 📝 Generates comprehensive markdown reports
- 📧 Email delivery of research reports
- 🚀 Deployed on Hugging Face Spaces with automatic GitHub integration
- 💬 Interactive Gradio chat interface

## Setup

### Prerequisites

- Python 3.11 or higher (tested with Python 3.12)
- An OpenAI API key
- Mailjet API credentials (for email functionality)

### Installation

1. **Install dependencies:**

   ```bash
   # Using uv (recommended)
   uv sync

   # OR using pip
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**

   Create a `.env` file in the project root:

   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   MAILJET_API_KEY=your_mailjet_api_key_here
   MAILJET_SECRET_KEY=your_mailjet_secret_key_here
   ```

### Running the Application

```bash
# Using uv (recommended)
uv run deep_research.py

# OR activate the virtual environment first
source .venv/bin/activate
python deep_research.py
```

The application will start a local Gradio server, typically at `http://localhost:7860`.

## Deployment

### Hugging Face Spaces

This project is configured for automatic deployment to Hugging Face Spaces via GitHub Actions. When you push changes to the main branch, GitHub Actions automatically syncs your app to Hugging Face.

### Manual Deployment

To manually deploy to Hugging Face Spaces:

```bash
# Activate your environment first (if not using uv run)
source .venv/bin/activate

# Deploy using gradio CLI
gradio deploy
```

## Project Structure

- `deep_research.py` - Main application entry point with Gradio UI
- `research_manager.py` - Orchestrates the research workflow
- `planner_agent.py` - Plans web searches for queries
- `search_agent.py` - Performs web searches
- `writer_agent.py` - Generates research reports
- `email_agent.py` - Sends email reports

## Key Dependencies

- `gradio==5.49.1` - Web UI framework
- `openai>=1.54.0` - OpenAI API client
- `openai-agents>=0.4.2` - OpenAI agents framework
- `huggingface-hub>=0.25.0` - Hugging Face integration
- `pydantic>=2.0.0` - Data validation
- `mailjet-rest>=1.3.0` - Email delivery
- `typer>=0.20.0` - CLI support

See `requirements.txt` for the complete list of dependencies.

## Troubleshooting

### Import Errors

If you encounter import errors, ensure you're running the application with `uv run` or from within an activated virtual environment:

```bash
# Option 1: Use uv run
uv run deep_research.py

# Option 2: Activate environment first
source .venv/bin/activate
python deep_research.py
```

### Version Compatibility

This project uses specific version pins to ensure compatibility between `gradio` and `huggingface-hub`. If you need to upgrade dependencies, test thoroughly before deploying.
