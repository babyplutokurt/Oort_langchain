from langchain.tools import tool
from pydantic import BaseModel, Field


class SearchInput(BaseModel):
    query: str = Field(description="should be a search query")


@tool("search", return_direct=True, args_schema=SearchInput)
def search_api(query: str) -> str:
    """Searches the API for the query."""
    return "Results"

print(search_api("what are you?"))