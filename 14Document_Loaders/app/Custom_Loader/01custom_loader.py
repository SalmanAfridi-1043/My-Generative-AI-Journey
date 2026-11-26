from pathlib import Path
from langchain_core.documents import Document
from langchain_core.document_loaders import BaseLoader


class CustomTextLoader(BaseLoader):
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def lazy_load(self):

        text = self.file_path.read_text(encoding="utf-8")

        yield Document(
            page_content=text,
            metadata={
                "source": str(self.file_path),
                "loader": "CustomTextLoader",
                "file_type": self.file_path.suffix,
            },
        )


# Initialize custom loader
loader = CustomTextLoader("file.txt")

# Load documents
documents = loader.load()

# Display results
for document in documents:
    print("Content:")
    print(document.page_content)

    print("\nMetadata:")
    print(document.metadata)


# Important explanations:
# - BaseLoader: Base interface/class for custom document loaders.
# - __init__(): Receives and stores the file path.
# - lazy_load(): Implements document loading.
# - yield: Returns Document objects one at a time.
# - Document(): Creates a LangChain document containing text and metadata.
# - loader.load(): Uses the loader's implementation to return a list of documents.
# Important: You can customize this loader to read APIs, databases, JSON files, or other data sources.
