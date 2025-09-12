# momo-expenses-langraph-ai-agent

This is an AI-assistant that lets you log expenses using natural language or voice.

Chat interactions are triggered from an MCP client built with copilot-kit, communicating with an MCP server that orchestrates tool calls via Gemini-powered LangGraph.

## 🚀 Running the Project Locally

Follow these steps to run the project on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/Blaise-Shyaka/momo-expenses-langraph-ai-agent.git
cd momo-expenses-langraph-ai-agent
```

### 2. Set Up Environment Variables

Each of the following directories contains an `.env.example` file:

* `expenses-agent`
* `expenses-api`
* `ui`

For each of them:

```bash
cd <directory-name>
cp .env.example .env
# Edit the .env file to update values as needed
```

### 3. Start the Application

Back in the project root directory, run:

```bash
docker compose --build up
```

### 4. Access the App

Once the containers are up, open your browser and navigate to:

[http://localhost:3000](http://localhost:3000)

## Current Architecture

The project currently consists of:
- **Expenses Agent**: LangGraph-powered agent for expense tracking using Gemini
- **Expenses API**: FastAPI backend for expense management
- **UI**: CopilotKit Assistant UI for chat interactions
