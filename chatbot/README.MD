# FAQ Chatbot with Neo4j and OpenAI

This chatbot is designed to answer frequently asked questions using a combination of Neo4j for stored answers and OpenAI's GPT model for fallback responses.

## Features
- **Neo4j Integration**: Fetches answers from a structured knowledge graph.
- **OpenAI GPT-3.5 Turbo**: Generates answers when a relevant question is not found in Neo4j.
- **RapidFuzz Matching**: Finds the best match for user questions from stored questions.
- **Logging**: Records interactions for debugging and improvements.

## Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/your-repo/chatbot.git
   cd chatbot
   ```

2. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Setup Neo4j**:
   - Install and start a local or cloud-based Neo4j instance.
   - Update the `URI` and `AUTH` variables in `chatbot.py` with your Neo4j credentials.

4. **Set Up OpenAI API Key**:
   - Obtain an API key from [OpenAI](https://platform.openai.com/signup/).
   - Replace `'your_openai_api_key'` in `chatbot.py` with your actual API key.

## Usage

Run the chatbot with:
```sh
python chatbot.py
```

Type your questions, and the chatbot will respond based on stored Neo4j answers or generate a response using OpenAI.

## File Structure

```
📂 chatbot/
 ├── chatbot.py          # Main chatbot logic
 ├── requirements.txt    # Dependencies list
 ├── README.md           # Project documentation
```

## Requirements

- Python 3.7+
- Neo4j running locally or in the cloud
- OpenAI API key

## Troubleshooting

If you encounter issues:
- Ensure your Neo4j database is running.
- Verify the OpenAI API key and check usage limits.
- Install all required dependencies (`pip install -r requirements.txt`).


