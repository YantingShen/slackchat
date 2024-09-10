from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

class SlackChatbot:
    def __init__(self, model_name='all-MiniLM-L6-v2', embeddings_file='processed_messages.pkl'):
        # Initialize sentence transformer model
        self.model = SentenceTransformer(model_name)
        
        # Load processed messages
        with open(embeddings_file, 'rb') as f:
            self.processed_messages = pickle.load(f)

    # Function to find most similar message and respond
    def chatbot_response(self, input_text):
        input_vector = self.model.encode(input_text)
        
        similarities = [cosine_similarity([input_vector], [msg[1]])[0][0] for msg in self.processed_messages]
        most_similar_idx = np.argmax(similarities)
        
        return self.processed_messages[most_similar_idx][0]

# Initialize the chatbot
chatbot = SlackChatbot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    response = chatbot.chatbot_response(user_input)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
