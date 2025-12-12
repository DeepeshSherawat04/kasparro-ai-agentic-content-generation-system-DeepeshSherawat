# check_agent.py
from langchain_ollama import ChatOllama
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate

from agents.langchain_tools import TOOLS

llm = ChatOllama(model="llama3.1:latest", temperature=0)

system_prompt = """
You are a tool-using assistant. Always call tools when needed.
Return only valid JSON when asked.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_structured_chat_agent(
    llm=llm,
    tools=TOOLS,
    prompt=prompt
)

executor = AgentExecutor(
    agent=agent,
    tools=TOOLS,
    verbose=True,
    handle_parsing_errors=True
)

print("\n🔍 Testing agent...")
response = executor.invoke({"input": "Read the product and return ONLY JSON with {\"ok\": true}"})
print("\nAgent output:\n", response["output"])
