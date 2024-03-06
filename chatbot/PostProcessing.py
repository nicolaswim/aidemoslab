import redis
import json
import time
from Chatbot import Interaction

# Initialize Redis connection
redis_host = 'localhost'
redis_port = 6379
redis_channel = 'chat_interactions'
r = redis.Redis(host=redis_host, port=redis_port)

class PostProcessing:

    total_word_count = 0  # Class variable to store the total word count

    @staticmethod
    def print_interaction(interaction):
        print(f"New Interaction Received: {interaction}")

    @staticmethod
    def count_words(text):
        # Simple word count by splitting text by spaces
        return len(text.split())

    @staticmethod
    def process_interaction(question, answer):
        # Count words in the current question and answer
        current_count = PostProcessing.count_words(question) + PostProcessing.count_words(answer)
        
        # Add to the total word count
        PostProcessing.total_word_count += current_count
        
        # Print the current interaction's word count and the updated total
        print(f"Current Interaction Word Count: {current_count}")
        print(f"Total Word Count So Far: {PostProcessing.total_word_count}")

def message_handler(message):
    # Assume message['data'] contains a JSON string with 'question' and 'answer'
    interaction_data = json.loads(message['data'].decode('utf-8'))
    
    # Access question and answer from the interaction data
    question = interaction_data['question']
    answer = interaction_data['answer']
    
    # Process the interaction for word counting and print the current total
    PostProcessing.process_interaction(question, answer)
    
    # You can still print the received interaction if needed
    print(f"New Interaction Received:\nQuestion: {question}\nAnswer: {answer}")

if __name__ == "__main__":
    pubsub = r.pubsub()
    pubsub.subscribe(**{redis_channel: message_handler})
    print(f"Subscribed to {redis_channel}. Listening for messages...")

    while True:
        message = pubsub.get_message()
        if message and message['type'] == 'message':
            message_handler(message)
        time.sleep(1)  # Sleep to reduce CPU usage
