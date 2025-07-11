from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent,AgentExecutor
from Tools import search_tool,wiki_tool,save_tool




# load_dotenv()




# class ResearchResponse(BaseModel):
#     topic: str
#     summary: str
#     sources: list[str]
#     tools_used: list[str]




# llm=ChatGroq(
#     model="llama3-8b-8192"
# )
# parser=PydanticOutputParser(pydantic_object=ResearchResponse)

# prompt=ChatPromptTemplate.from_messages(
# [
# (
#     "system","""You are a research assistant that will help generate a research paper.
#     Answer the user query and use neccessary tools.
#     Wrap the output in this format and provide no other text \n {format_instructions}""",
# ),
# ("placeholder","{chat_history}"),
# ( "human","{query}"
# ),
# (
#     "placeholder","{agent_scratchpad}"
# ),
# ]
#  ).partial(format_instructions=parser.get_format_instructions())

# tools=[search_tool]
# agent=create_tool_calling_agent(
#     llm=llm,
#     prompt=prompt,
#     tools=tools
# )

# agent_executor=AgentExecutor(
#     agent=agent,
#     tools=tools,
#     verbose=True
# )
# query=input("what can i help you research ?")
# raw_response=agent_executor.invoke(
#     {
#         "query": query,
#     }
# )
# print(raw_response)


# try:
#     structured_response=parser.parse(raw_response.get("output"))
#     print(structured_response)
# except Exception as e:
#     print("Error parsing response:", e , "Raw response - " , raw_response)

# filename: Main.py

from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from Tools import search_tool  # your DuckDuckGo tool
import re

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# Groq-compatible LLM
llm = ChatGroq(model="llama3-8b-8192")

# Output parser for structured response
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Prompt for model
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a research assistant. If you need to use any tool, tell the user what tool you want.
"Only say 'search: <your search term>' if you want to search the web."
{format_instructions}""",
        ),
        ("human", "{query}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

import json

def extract_json(text: str) -> str:
    """Extract first JSON object from text block."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model response.")
    return match.group(0)



# Input
query = input("What can I help you research? ")

# Step 1: Initial response
initial_response = llm.invoke(prompt.format(query=query))
print("Model response:\n", initial_response.content)

# Step 2: Check if model wants to use a tool
search_match = re.search(r"search\s*:\s*(.+)", initial_response.content, re.IGNORECASE)

tool_output = ""
tools_used = []
sources = []

if search_match:
    keyword = search_match.group(1).strip()
    print(f"\n🔍 Tool requested: Searching for '{keyword}'...\n")
    tool_output = search_tool.run(keyword)
    print("🔎 Tool result:\n", tool_output)
    tools_used.append("search")
    sources.append("DuckDuckGo")

    # Step 3: Feed tool result back to LLM
    follow_up_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Use this tool output to answer the user's query. Wrap in this JSON format:\n{format_instructions}"),
        ("human", "User asked: {query}\n\nTool output:\n{tool_output}")
    ]
    ).partial(format_instructions=parser.get_format_instructions())

    final_response = llm.invoke(follow_up_prompt.format(query=query, tool_output=tool_output))

    final_text = final_response.content
else:
    final_text = initial_response.content

# Step 4: Parse into structured response
try:
    json_text = extract_json(final_text)
    structured = parser.parse(json_text)
    if tools_used:
        structured.tools_used = tools_used
        structured.sources = sources
    print("\n✅ Structured Response:")
    print(structured.model_dump_json(indent=2))

except Exception as e:
    print("\n❌ Error parsing response:", e)
    print("🪵 Raw response:\n", final_text)

