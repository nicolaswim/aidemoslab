import os
from langchain_openai import OpenAI
import openai

# Initialize your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize the Langchain LLM with OpenAI
llm = OpenAI()

class ConversationMemory:
    def __init__(self):
        self.memory = []

    def add_interaction(self, user_input, bot_response):
        self.memory.append({'user': user_input, 'bot': bot_response})

    def get_formatted_memory(self):
        # Format the conversation history for inclusion in the prompt
        formatted_memory = "\n".join([f"User: {interaction['user']}\nBot: {interaction['bot']}" for interaction in self.memory])
        return formatted_memory

class PostProcessing:
    word_count_list = []  # Class variable to store word counts for all interactions

    @staticmethod
    def log_word_counts(question, answer):
        question_word_count = len(question.split())
        answer_word_count = len(answer.split())
        # Store the word counts along with the question and answer
        PostProcessing.word_count_list.append({
            'question': question,
            'answer': answer,
            'question_word_count': question_word_count,
            'answer_word_count': answer_word_count
        })

    @staticmethod
    def print_word_counts():
        for item in PostProcessing.word_count_list:
            print(f"Question: {item['question']}, Answer: {item['answer']}, "
                  f"Question Word Count: {item['question_word_count']}, Answer Word Count: {item['answer_word_count']}")

class AdvancedMemoryChatbot:
    def __init__(self):
        self.memory = ConversationMemory()

    def ask_chatbot(self, question):
        # Generate a prompt with conversation history
        formatted_memory = self.memory.get_formatted_memory()
        prompt = f"{formatted_memory}\nUser: {question}\nBot:"
        response = llm.generate([prompt])
        bot_response = response.generations[0][0].text.strip()
        # Update memory with the new interaction
        self.memory.add_interaction(question, bot_response)
        # Log word counts for post-processing
        PostProcessing.log_word_counts(question, bot_response)
        return bot_response

def main():
    chatbot = AdvancedMemoryChatbot()
    print("Chatbot is ready. Type 'quit' to exit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = chatbot.ask_chatbot(user_input)
        print(f"Chatbot: {response}")

    # After the chat ends, print all word counts
    print("\n Word counts for all interactions:")
    PostProcessing.print_word_counts()

if __name__ == "__main__":
    main()