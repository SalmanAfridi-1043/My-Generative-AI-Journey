from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


# 1. Create Wikipedia API wrapper | it connects to wikipedia functionality
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=300)


# 2. Create built-in tool | Creates the actual LangChain tool
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)


# 3. Inspect tool
# print("Name:", wiki_tool.name)
# print("Description:", wiki_tool.description)
# print("Arguments:", wiki_tool.args)


query = "Name all the GTA games launch by Rockstar"

# 4. Execute tool
# result = wiki_tool.invoke({"query": "LangChain"})


result = wiki_tool.invoke({"query": query})


print("\n\nWikipedia Result : ")
print(result)
