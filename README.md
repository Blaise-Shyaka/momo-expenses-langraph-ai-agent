# momo-expenses-langraph-ai-agent

This is an AI-assistant that lets you initiate payments and log expenses using natural language or voice.
It's integrated with [MoMo API](https://momodeveloper.mtn.com/) and could support other modes of payments in the future.
It would understand commands like "Pay 30k for my internet bill" or "How much did I spend on fuel in the past month?".

Chat interactions are triggered from an MCP client built with copilot-kit, communicating with an MCP server that orchestrates tool calls via Gemini-powered LangGraph.

## Current Architecture

The project currently consists of:
- **Expenses Agent**: LangGraph-powered agent for expense tracking using Gemini
- **Expenses API**: FastAPI backend with SQLite database for expense management
- **UI**: Next.js frontend with Assistant UI for chat interactions
- **Database**: SQLite for storing expenses and categories

## Running the Project Locally

The project consists of several components that need to be started individually. The project can only be run locally at the moment.

Clone the repository:
```shell
git clone https://github.com/Blaise-Shyaka/momo-expenses-langraph-ai-agent.git
```

---

### 1. API

Handles business logic and writes expenses to a SQLite database.

**Steps:**

```bash
cd expenses-api         # Navigate to the API directory
pip install -r requirements.txt   # Install dependencies
uvicorn main:app       # Start the API server
```

---

### 2. LangGraph Agent

Langgraph tool-calling agent.

**Steps:**

```bash
cd expenses-agent         # Navigate to the agent directory
pip install -r requirements.txt   # Install dependencies
cp .env.example .env      # Copy environment example and update values
langgraph dev             # Start the LangGraph agent
```

> 💡 Ensure all required API keys and environment variables are correctly set in `.env`.

---

### 3. UI

The frontend interface you’ll use to interact with the agent. Runs at `http://localhost:3000`.

**Steps:**

```bash
cd ui/momo-expenses-agent   # Navigate to the UI directory
npm install                 # Install frontend dependencies
touch .env                  # Create an environment file
```

Add the following environment variables to `.env` (replace `LANGCHAIN_API_KEY` with your actual key):

```
LANGGRAPH_API_URL=http://127.0.0.1:2024
LANGCHAIN_API_KEY=ls...13
NEXT_PUBLIC_LANGGRAPH_ASSISTANT_ID=chat
```

Then start the Next.js development server:

```bash
npm run dev
```

---

### ✅ You’re Ready!

With all services running, you can now interact with the agent through the local UI.

## 🗺️ Roadmap

### Phase 1: Payment Integration & Architecture Improvements 🔴

#### 1.1 MoMo Payment Agent
- [ ] Create dedicated agent for MoMo API integration
- [ ] Implement payment initiation workflows
- [ ] Add payment status tracking

#### 1.2 MCP Server Migration
- [ ] Migrate from direct LangGraph to MCP (Model Context Protocol) server architecture
- [ ] Implement MCP server to orchestrate both expenses and payment agents

### Phase 2: Mobile Application Development 🔴

#### 2.1 Mobile App Foundation
- [ ] **Framework Selection**: React Native or Flutter for cross-platform development
- [ ] Implement core mobile UI components and navigation
- [ ] Add mobile-optimized chat interface 
- [ ] Integrate mobile-specific features. (Initiate payments by taking a picture of a MoMo poster)

### Phase 3: Enhanced User Experience

#### 3.1 Human-in-the-Loop (HITL)
- [ ] Add confirmation prompts
- [ ] Implement review and correction mechanisms

#### 3.2 Conversation Threading
- [ ] Implement persistent conversation threads
- [ ] Add thread management (create, delete, archive)

#### 3.3 Internationalization & Localization 🟢
- [ ] **Multi-language Support**: English, French, Kinyarwanda

### Phase 4: Data & Memory Enhancements

#### 4.1 Persistent Memory System
- [ ] Implement long-term conversation memory
- [ ] Add user preference learning and adaptation
- [ ] Create contextual memory for recurring patterns
- [ ] Implement semantic search across conversation history
- [ ] Add memory summarization and pruning mechanisms

#### 4.2 Database Migration 🔴
- [ ] **Evaluate database options**: PostgreSQL, MongoDB, or cloud solutions
- [ ] Implement backup and recovery procedures
- [ ] Add database monitoring and health checks

### Phase 5: Security & Multi-tenancy

#### 5.1 User Authentication & Authorization 🔴
- [ ] Implement OAuth 2.0 / OpenID Connect integration
- [ ] Add multi-factor authentication (MFA)
- [ ] Create role-based access control (RBAC)
- [ ] Implement session management and security
- [ ] Add API rate limiting and abuse protection

### Phase 5: Advanced Features

#### 5.1 Analytics & Insights
- [ ] Add expense analytics and reporting dashboard
- [ ] Create budget tracking and alerts
- [ ] Implement export functionality (PDF, CSV, Excel)

#### 5.2 Integration Ecosystem
- [ ] Add calendar integration for scheduled payments

### Technical Debt & Improvements

#### Ongoing Enhancements
- [ ] Add comprehensive error handling and logging
- [ ] Implement automated testing suite (unit, integration, e2e)

---

**Priority Legend:**
- 🔴 High Priority (Core functionality)
- 🟡 Medium Priority (User experience)
- 🟢 Low Priority (Nice to have)

**Timeline Estimate:** 3 - 6 months for full roadmap completion
