import os
from langchain_openai import OpenAI
import openai
import redis
import json

# Initialize your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize the Langchain LLM with OpenAI
llm = OpenAI()

# Initialize Redis connection
redis_host = 'localhost'
redis_port = 6379
redis_channel = 'chat_interactions'
r = redis.Redis(host=redis_host, port=redis_port)

class Interaction:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def to_json(self):
        return json.dumps({'question': self.question, 'answer': self.answer})

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return Interaction(data['question'], data['answer'])

class ConversationMemory:
    def __init__(self):
        self.memory = []

    def add_interaction(self, user_input, bot_response):
        self.memory.append({'user': user_input, 'bot': bot_response})

    def get_formatted_memory(self):
        formatted_memory = "\n".join([f"User: {interaction['user']}\nBot: {interaction['bot']}" for interaction in self.memory])
        return formatted_memory

class AdvancedMemoryChatbot:
    def __init__(self):
        self.memory = ConversationMemory()

    def ask_chatbot(self, question):
        formatted_memory = self.memory.get_formatted_memory()
        prompt = f"{formatted_memory}\nUser: {question}\nBot:"
        response = llm.generate([prompt])
        bot_response = response.generations[0][0].text.strip()
        self.memory.add_interaction(question, bot_response)

        interaction = Interaction(question, bot_response)
        
        # Convert the Interaction object to a JSON string for publishing
        interaction_json = interaction.to_json()
        
        # Publish the JSON string to Redis
        r.publish(redis_channel, interaction_json)

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

if __name__ == "__main__":
    main()
