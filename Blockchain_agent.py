import os
from langchain.document_loaders import JSONLoader
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from Blockchain_tools import CustomSearchTool, BalanceSearchTool, BlockSearchTool

os.environ["OPENAI_API_KEY"] = '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'
os.environ['SERPAPI_API_KEY'] = '275dcc7d15cb189a36e6b13662c2e142c6d049c9ef406bddbab7826298777fa0'
llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')

loader = JSONLoader(
    file_path='./Json_files/Account_balance.json',
    jq_schema='.result[] ',
    text_content=False
)
data = loader.load()

tools = [BalanceSearchTool(), BlockSearchTool()]
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, handle_parsing_errors=True
)

agent.run("what is the account that has the most balance?")

# agent.run("what is the Timestamp of block 2165403")
'''
agent.run(
    "What did the president say about Ketanji Brown Jackson"
)

agent.run(
    "Did he mention who she succeeded"
)

agent.run(
    "What was his stance on Ukraine"
)
'''
