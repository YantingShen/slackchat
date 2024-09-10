import json
import pickle
import torch
from transformers import AutoModel, AutoTokenizer

class SlackHistoryProcessor:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        # Initialize Hugging Face model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def load_slack_history(self, file_path):
        with open(file_path, 'r') as f:
            messages = json.load(f)
        return messages

    def process_messages(self, messages):
        processed_messages = []
        for msg in messages:
            if "text" in msg:
                inputs = self.tokenizer(msg["text"], return_tensors='pt', truncation=True, padding=True)
                with torch.no_grad():
                    outputs = self.model(**inputs)
                embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
                processed_messages.append((msg["text"], embeddings, msg["ts"]))
        return processed_messages

    def save_processed_messages(self, processed_messages, output_file):
        with open(output_file, 'wb') as f:
            pickle.dump(processed_messages, f)
        print(f"Processed and saved {len(processed_messages)} messages to {output_file}")

# Process the updated dummy Slack history
processor = SlackHistoryProcessor()
messages = processor.load_slack_history('dummy_slack_history.json')
processed_messages = processor.process_messages(messages)
processor.save_processed_messages(processed_messages, 'processed_messages.pkl')