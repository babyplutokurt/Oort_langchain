import pickle
from Blockchain_tools import CustomSearchTool
from query_data import get_chain
import os
import os
import pickle
from pprint import pprint
from langchain.document_loaders import JSONLoader
import yaml
from langchain.agents import create_json_agent, AgentExecutor
from langchain.agents.agent_toolkits import JsonToolkit
from langchain.chains import LLMChain
from langchain.llms.openai import OpenAI
from langchain.requests import TextRequestsWrapper
from langchain.tools.json.tool import JsonSpec
from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import ToolException
from pydantic import BaseModel, Field
from langchain.tools.base import ToolException
from langchain import SerpAPIWrapper
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from Blockchain_tools import CustomSearchTool
os.environ["OPENAI_API_KEY"] = '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'
os.environ['SERPAPI_API_KEY'] = '275dcc7d15cb189a36e6b13662c2e142c6d049c9ef406bddbab7826298777fa0'

if __name__ == "__main__":
    with open("vectorstore.pkl", "rb") as f:
        vectorstore = pickle.load(f)

    qa_chain = get_chain(vectorstore)

    llm = ChatOpenAI(temperature=0)
    tools = [CustomSearchTool()]
    agent = initialize_agent(
        tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )

    chat_history = []
    print("Chat with your docs!")
    while True:
        print("You:")
        question = input()
        result = agent.run({"question": question, "chat_history": chat_history})
        print("AI:")
        print(result)
        # chat_history.append((question, result))

