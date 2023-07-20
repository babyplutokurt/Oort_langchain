import os
import pickle
from typing import Optional

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool
import yaml
from langchain.agents import create_json_agent, AgentExecutor
from langchain.agents.agent_toolkits import JsonToolkit
from langchain.chains import LLMChain
from langchain.llms.openai import OpenAI
from langchain.requests import TextRequestsWrapper
from langchain.tools.json.tool import JsonSpec

os.environ["OPENAI_API_KEY"] = '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'
os.environ['SERPAPI_API_KEY'] = '275dcc7d15cb189a36e6b13662c2e142c6d049c9ef406bddbab7826298777fa0'
with open("vectorstore.pkl", "rb") as f:
    vectorstore = pickle.load(f)


def get_chain(vectorstore_):
    qa = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(temperature=0, model='gpt-3.5-turbo'),
        vectorstore_.as_retriever(),
        condense_question_llm=ChatOpenAI(temperature=0, model='gpt-3.5-turbo'),
    )
    return qa


qa_chain = get_chain(vectorstore)
chat_history = []
'''
class CalculatorInput(BaseModel):
    question: str = Field()

def _handle_error(error: ToolException) -> str:
    return (
            "The following errors occurred during tool execution:"
            + error.args[0]
            + "Please try another tool."
    )
'''


class CustomSearchTool(BaseTool):
    name = "custom_search"
    description = "useful for when you need to answer questions about people"

    def _run(self, query, run_manager: Optional[CallbackManagerForToolRun] = None):
        result = qa_chain({"question": query, "chat_history": chat_history})
        chat_history.append((result["question"], result['answer']))
        return result

    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("custom_search does not support async")


with open("/Users/taolueyang/Oort/chat-your-data/Json_files/Account_balance.json") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
json_spec = JsonSpec(dict_=data, max_value_length=4000)
json_toolkit = JsonToolkit(spec=json_spec)

json_agent_executor = create_json_agent(
    llm=OpenAI(temperature=0), toolkit=json_toolkit, verbose=True, handle_parsing_errors=True
)


# json_agent_executor.run("what is the account which has the most balance?")


class BalanceSearchTool(BaseTool):
    name = "Balance_Search"
    description = "useful for when you need to answer questions about account and balance " \
                  ", you need to go through the Json file " \
                  "and check keys and values, Use this more than the normal search if the question is about Balance"

    def _run(self, query, run_manager: Optional[CallbackManagerForToolRun] = None):
        result = json_agent_executor.run(query)

        chat_history.append((query, result))
        return result

    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("custom_search does not support async")


with open("/Users/taolueyang/Oort/chat-your-data/Json_files/Blocks.json") as f:
    data1 = yaml.load(f, Loader=yaml.FullLoader)
json_spec1 = JsonSpec(dict_=data1, max_value_length=4000)
json_toolkit1 = JsonToolkit(spec=json_spec1)

json_agent_executor1 = create_json_agent(
    llm=OpenAI(temperature=0), toolkit=json_toolkit1, verbose=True, handle_parsing_errors=True
)


class BlockSearchTool(BaseTool):
    name = "Block_Search"
    description = "useful for when you need to answer questions about timestamp"

    def _run(self, query, run_manager: Optional[CallbackManagerForToolRun] = None):
        result = json_agent_executor1.run(query)

        chat_history.append((query, result))
        return result

    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("custom_search does not support async")
