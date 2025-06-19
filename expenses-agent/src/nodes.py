from .agent_state import ExpensesAgentState
from .llm import gemini_llm, messages

def gemini_node(state: ExpensesAgentState):
  return { "messages": gemini_llm.invoke(messages + state["messages"]) }
