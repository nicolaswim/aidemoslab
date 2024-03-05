import os
from langchain_openai import OpenAI
import openai

def ask_chatbot(question, conversation_history):
    # Initialize the Langchain LLM with OpenAI
    llm = OpenAI()

    # Add the current question to the conversation history
    conversation_history.append(f"You: {question}")
    # Prepare the prompt by joining the conversation history with new lines
    prompt = "\n".join(conversation_history)
    # The generate method expects a list of strings, hence [prompt]
    response = llm.generate([prompt])
    # Assuming the structure of the response allows this direct access
    answer_text = response.generations[0][0].text
    # Add the chatbot's response to the conversation history
    conversation_history.append(f"Chatbot: {answer_text}")
    return answer_text, conversation_history

def main():
    # Initialize your OpenAI API key
    openai.api_key = os.getenv('OPENAI_API_KEY')

    conversation_history = []
    print("Chatbot is ready. Type 'quit' to exit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response, conversation_history = ask_chatbot(user_input, conversation_history)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()
