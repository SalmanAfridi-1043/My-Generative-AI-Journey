from langchain_core.documents import Document

# Sample document content
text = """
LangChain is a framework for developing
applications powered by Large Language Models.
"""

# Document: LangChain's standard document representation.

# Convert text into a LangChain Document
document = Document(
    page_content=text, metadata={"source": "introduction.txt", "topic": "LangChain"}
)

print(document)
print(type(document))
print()

# Display document content
print("Document Content:")
print(document.page_content)

# Display metadata
print("\nDocument Metadata:")
print(document.metadata)
