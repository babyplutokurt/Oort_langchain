import pickle
from query_data import get_chain
import os

os.environ["OPENAI_API_KEY"] = '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'
os.environ['SERPAPI_API_KEY'] = '275dcc7d15cb189a36e6b13662c2e142c6d049c9ef406bddbab7826298777fa0'

if __name__ == "__main__":
    with open("vectorstore.pkl", "rb") as f:
        vectorstore = pickle.load(f)
    qa_chain = get_chain(vectorstore)
    chat_history = []
    print("Chat with your docs!")
    while True:
        print("You:")
        question = input()
        result = qa_chain({"question": question, "chat_history": chat_history})
        chat_history.append((question, result["answer"]))
        # print('Chat History: ', chat_history)
        print("AI:")
        print(result["answer"])


# What did the president say about Kentaji Brown Jackson
#
# Did he mention Stephen Breyer?
#
# What was his stance on Ukraine