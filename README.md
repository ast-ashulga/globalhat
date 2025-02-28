# LangGraph Agent with Persistent Memory

This project demonstrates how to create a LangGraph agent with persistent memory capabilities. The agent can remember information across sessions, making it useful for maintaining context in conversations.

## Features

- ReAct agent pattern using LangGraph
- Persistent memory using Postgress storage
- Calculator tool for mathematical operations
- Memory management tools for storing and retrieving memories

## Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the agent:

```bash
python react_agent.py
```

The agent will:
1. Remember that you prefer dark mode
2. Recall this preference when asked

You can modify the example prompts in the script to test different memory scenarios.

## How It Works

### Memory Persistence

The agent uses a file-based persistence mechanism that saves checkpoints to a pickle file (`memory_checkpoints.pkl`). This allows the agent to maintain memory across different sessions.

The `FilePersistentMemorySaver` class:
- Loads existing checkpoints when initialized
- Saves checkpoints to disk after each update
- Provides a simple but effective persistence solution

### Alternative Persistence Options

The project is set up with file-based persistence for simplicity, but you can switch to other persistence options:

#### PostgreSQL (with vector search)

```bash
pip install psycopg-binary psycopg-pool langgraph-checkpoint-postgres
```

Requires:
- PostgreSQL server with pgvector extension
- Connection string in `.env`: `POSTGRES_URI=postgresql://username:password@localhost:5432/dbname`

#### SQLite

```bash
pip install langgraph-checkpoint-sqlite
```

Simple database solution without requiring a separate server.

#### MongoDB

```bash
pip install pymongo langgraph-checkpoint-mongodb
```

Requires:
- MongoDB server
- Connection string in `.env`: `MONGO_URI=mongodb://localhost:27017/`

## Project Structure

- `react_agent.py` - Main agent implementation with file-based persistence
- `requirements.txt` - Project dependencies
- `.env` - Environment variables (API keys, connection strings)
- `memory_checkpoints.pkl` - Generated file that stores agent memory

## Extending the Agent

You can extend this agent by:
1. Adding more tools to the agent's toolkit
2. Customizing the memory storage and retrieval logic
3. Implementing more sophisticated persistence mechanisms
4. Adding a web interface or API endpoints

## Troubleshooting

- **Memory not persisting**: Ensure the script has write permissions in the directory
- **API key errors**: Check that your `.env` file contains a valid OpenAI API key
- **Import errors**: Verify all dependencies are installed with `pip install -r requirements.txt`
