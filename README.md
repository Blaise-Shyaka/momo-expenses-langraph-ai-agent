# momo-expenses-langraph-ai-agent

This is an AI-assistant that lets you initiate payments and log expenses using natural language or voice.
It's integrated with [MoMo API](https://momodeveloper.mtn.com/) and could support other modes of payments in the future.
It would understand commands like "Pay 30k for my internet bill" or "How much did I spend on fuel in the past month?".

Chat interactions are triggered from an MCP client built with copilot-kit, communicating with an MCP server that orchestrates tool calls via Gemini-powered LangGraph. 