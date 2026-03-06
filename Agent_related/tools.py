from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

def wikipediaQueryRunner_with_error_handling():
    class SafeWikipediaQueryRunner(WikipediaQueryRun):
        def run(self, query: str) -> str:
            try:
                return super().run(query)
            except Exception as e:
                return f"Error querying Wikipedia: {str(e)}"

    return SafeWikipediaQueryRunner(api_wrapper=WikipediaAPIWrapper())









