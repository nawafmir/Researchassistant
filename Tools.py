from langchain_community.tools import WikipediaQueryRun,DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime



# # search=DuckDuckGoSearchRun()
# # search_tool=Tool(
# #     name="search",
# #     func=search.run,
# #     description="Search the web for information",
# # )
# # filename: Tools.py
# from langchain.tools import tool
# from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper

# search = DuckDuckGoSearchAPIWrapper()

# @tool
# def search_tool(query: str) -> str:
#     """Search the web using DuckDuckGo."""
#     return search.run(query)
# Tools.py (updated for ddgs)
from langchain.tools import tool
from ddgs import DDGS

def save_to_txt(data: str, filename: str = "search_results.txt"):
    timestamp= datetime.now().strftime("%Y%m%d_%H%M%S")
    formatted_text= f"Search Results - {timestamp}\n\n{data}"

    with open(filename, "a" , encoding="utf-8") as f:
        f.write(formatted_text + "\n\n")
    return f"Results saved to {filename}"
save_tool=Tool(
    name="save_to_txt",
    func=save_to_txt,
    description="Saves the search results to a text file with a timestamp.",
)




@tool
def search_tool(query: str) -> str:
    """Search the web using DuckDuckGo."""
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)
        return "\n".join([r["body"] for r in results])



api_wraper=WikipediaAPIWrapper(top_k_results=2,doc_content_chars_max=150)
wiki_tool=WikipediaQueryRun(api_wrapper=api_wraper)
