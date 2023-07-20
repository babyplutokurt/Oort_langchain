from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.tools import BaseTool

import os
os.environ["OPENAI_API_KEY"] = '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'

class ServiceCenterTool(BaseTool):
    name = "ServiceCenter"
    description = "如果想查询售后服务站点,请使用它"
    return_direct = True  # 直接返回结果

    def _run(self, query: str) -> str:
        print("\nServiceCenter query: " + query)
        return "您可以在以下链接中找到售后站点信息：[售后站点]:(https://www.lenovoimage.com/index.php/services/services_search)。在该链接中，您可以输入北京作为地区，然后搜索相关的售后站点信息。希望这可以帮到您！"

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("暂时不支持异步")
        
def service_qa(string):
    print(f"\n### 服务站点 ### {string} \n")
    ## IP -> tag 
    
    return "您可以在以下链接中找到售后站点信息：[售后站点]:(https://www.lenovoimage.com/index.php/services/services_search)。在该链接中，您可以输入北京作为地区，然后搜索相关的售后站点信息。希望这可以帮到您！"
        
def sales_qa(string):
    print(f"\n### 售前服务 ### {string} \n")
    return "这是一个售前服务"
    
def support_qa(string):
    print(f"\n### 售后服务 ### {string} \n")
    return "这是一个售后服务"

tools = [
    Tool(
        name = "ServiceCenter",
        #func=sales_qa.run,
        func=service_qa,
        return_direct = True,
        description="""
        当用户需要查找售后服务网点时候,使用它.
        此工具的输入应该是省份和城市的逗号分隔列表,表示省份和城市。
        例如，如果您想查询'厦门的服务网点'，则输入为'福建省,厦门市'
        例如，如果您想查询'附近服务网点'，则输入为'None,None'
        """
        
        ### D1 ### 根据Tool分析
        
        ### D2 ### chatgpt,分析省份城市信息
        ### D2 ### 如果没有省份城市信息,从IP获取省份城市信息
        
        ### D3 ### tag 获取对应售后站点信息,GPT 格式化输出
    ),
    Tool(
        name = "Sales",
        #func=sales_qa.run,
        func=sales_qa,
        return_direct = True,
        description="""
        售前服务,请使用它.
        此工具的输入应该是用户的原始问题,不需要做任何修饰
        """
    ),
    Tool(
        name = "Support",
        #func=support_qa.run,
        func=support_qa,
        return_direct = True,
        description="""
        售后服务,当用户想解决产品使用中的问题,提供技术支持以及处理退换货、维修和保修等事务.请使用它.
        此工具的输入应该是产品型号和问题的逗号分隔列表,表示型号和问题。
        例如，如果您想查询'联想M100W打印机卡纸了怎么办'，则输入为'M100W,卡纸了怎么办'
        例如，如果您想查询'卡纸了怎么办'，则输入为'None,卡纸了怎么办'
        """
        
        ### D1 ### Tool分析是否为一个完整的问题
        ### D2 ### 根据历史上下文组成一个独立问题
        
        ### D1 ### 根据Tool分析
        
        ### D2 ### 从问题中分析出设备型号,如果没有以用户传入tag为准
        
        ### D3 ### tag 获取对应段落,GPT 格式化输出
        
        ### 独立问题? ###
        ### 翻译? ###
        ### 售前? ###
        ### 售后? ###
        ### 
    ),
]

llm = OpenAI(temperature=0.5)

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, intermediate_steps=True
)

answer=agent.run("请推荐一款打印机,适合家用的")
#print(f"\nanswer:{answer} \n")
agent.run("联想M100W打印机,没有墨水了怎么办")
agent.run("发票机打印很淡怎么办")
agent.run("福建厦门售后网点")
agent.run("深圳售后网点")
agent.run("北京售后网点")
agent.run("附近售后网点")