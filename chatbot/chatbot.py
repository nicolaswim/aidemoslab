import os
from langchain_openai import OpenAI  # Updated import based on deprecation warning
from langchain.chains import LLMChain  # Updated import based on deprecation warning
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory

# Load the OPENAI_API_KEY from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

template = """
You are a chatbot that is unhelpful.
Your goal is to not help the user but only make jokes.
Take what the user is saying and make a joke out of it

{chat_history}
Human: {human_input}
Chatbot:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"], 
    template=template
)
memory = ConversationBufferMemory(memory_key="chat_history")

llm_chain = LLMChain(
    llm=OpenAI(api_key=openai_api_key),  # Ensure you're using the correct parameter for the API key
    prompt=prompt, 
    verbose=True, 
    memory=memory
)

# Example usage with print to explicitly show output
response = llm_chain.predict(human_input="Is a pear a fruit or vegetable?")
print("Response:", response)

response = llm_chain.predict(human_input="What was one of the fruits I first asked you about?")
print("Response:", response)
