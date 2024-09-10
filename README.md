# Slack Chatbot

This project provides a Slack chatbot that can answer questions based on the saved embeddings of Slack chat history. The chatbot uses the `all-MiniLM-L6-v2` model from the `sentence-transformers` library to generate embeddings and find the most similar messages.

## Prerequisites

- Python 3.6+
- Slack SDK
- Sentence Transformers
- Scikit-learn
- NumPy

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/slack-chatbot.git
    cd slack-chatbot
    ```

2. Install the required packages:
    ```bash
    pip install slack_sdk sentence-transformers scikit-learn numpy
    ```

3. Set your Slack bot token as an environment variable:
    ```bash
    export SLACK_BOT_TOKEN='your-slack-bot-token'
    ```

## Usage

### 1. Download Slack History

To download messages from specific conversations and channels, run the `download_slack_history.py` script. Replace `'CHANNEL_ID'` with the actual channel ID.

bash
python process_slack_history.py


This will save the processed messages (embeddings) to a file named `processed_messages.pkl`.

### 3. Run the Chatbot

To run the chatbot and answer questions based on the saved embeddings, run the `chatbot.py` script.

bash
python chatbot.py


The chatbot will start and you can interact with it through the command line.

## Example

1. **Download Slack History**:
    ```bash
    python download_slack_history.py
    ```

2. **Process and Save Embeddings**:
    ```bash
    python process_slack_history.py
    ```

3. **Run the Chatbot**:
    ```bash
    python chatbot.py
    ```

## License

This project is licensed under the MIT License.

