import pickle
import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer
from sklearn.metrics.pairwise import cosine_similarity

class SlackChatbot:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2', embeddings_file='processed_messages.pkl'):
        # Initialize Hugging Face model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        
        # Load processed messages
        with open(embeddings_file, 'rb') as f:
            self.processed_messages = pickle.load(f)

    # Function to find most similar message and respond
    def chatbot_response(self, input_text):
        inputs = self.tokenizer(input_text, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        input_vector = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        
        similarities = [cosine_similarity([input_vector], [msg[1]])[0][0] for msg in self.processed_messages]
        most_similar_idx = np.argmax(similarities)
        
        return self.processed_messages[most_similar_idx][0], self.processed_messages[most_similar_idx][2]

    # Function to take user question and return response
    def ask_question(self, question):
        response, timestamp = self.chatbot_response(question)
        return response, timestamp


