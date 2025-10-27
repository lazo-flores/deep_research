# Deep Research

AI Agents that research a given topic, generate a report in markdown, and email it to the user.

## Setup

### Prerequisites

- Python 3.11 or higher
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

3. **Resolve the 'agents' module issue:**

   ⚠️ **IMPORTANT:** The project currently has a missing dependency issue with the `agents` module.

   The imports `from agents import Agent, WebSearchTool, Runner, trace, gen_trace_id` are looking for an OpenAI agents SDK package that is not available as a standard PyPI package.

   **To fix this, you have two options:**

   **Option A: Check your course materials**
   - Your Udemy course or source may provide specific installation instructions
   - Look for additional setup steps or code updates

   **Option B: Install from OpenAI GitHub (if applicable)**
   ```bash
   pip install git+https://github.com/openai/openai-python.git
   ```
   
   Note: This may require updating the import statements in the code.

### Running the Application

Once the `agents` module issue is resolved:

```bash
# Using uv
uv run python deep_research.py

# OR using Python directly
python deep_research.py
```

## Project Structure

- `deep_research.py` - Main application entry point with Gradio UI
- `research_manager.py` - Orchestrates the research workflow
- `planner_agent.py` - Plans web searches for queries
- `search_agent.py` - Performs web searches
- `writer_agent.py` - Generates research reports
- `email_agent.py` - Sends email reports

## Dependencies

See `requirements.txt` for the list of required packages.
