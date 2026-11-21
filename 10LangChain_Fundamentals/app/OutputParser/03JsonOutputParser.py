from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os

load_dotenv()

model = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,
)

# returns pythong dictionary (json format)
parser = JsonOutputParser()

# create prompt
# prompt = ChatPromptTemplate.([
#     """
#     Provide information about {language}.

#     {format_instructions}
#     """
# ])

# # instructions format for output
# prompt = prompt.partial(format_instructions=parser.get_format_instructions())


# below is the compact version of above prompt
prompt = ChatPromptTemplate(
    [
        """Provide info about {language}
            {format_instructions}
        """
    ],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


chain = prompt | model | parser

response = chain.invoke({"language": "Python"})

print(response)
print(type(response))
