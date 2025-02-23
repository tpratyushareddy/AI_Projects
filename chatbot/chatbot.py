import logging
import openai
from neo4j import GraphDatabase
from rapidfuzz import process

# Setup logging
logging.basicConfig(filename="chatbot_logs.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# Neo4j connection details
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "n1234567")

# OpenAI API key setup
openai.api_key = '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'  # Replace with your OpenAI API key

# Connect to Neo4j
driver = GraphDatabase.driver(URI, auth=AUTH)

# Fetch all stored questions from Neo4j
def fetch_questions():
    with driver.session() as session:
        result = session.run("MATCH (q:Question) RETURN q.text")
        return [record["q.text"] for record in result]

# Find the best matching question
def find_best_match(user_question, stored_questions):
    match, score, _ = process.extractOne(user_question, stored_questions)
    return match if score > 70 else None  # Adjust threshold if needed

# Fetch answer for the best-matched question from Neo4j
def get_answer(question):
    with driver.session() as session:
        result = session.run(
            "MATCH (q:Question {text: $question})-[:ANSWERED_BY]->(a:Answer) RETURN a.text",
            question=question
        )
        record = result.single()
        return record["a.text"] if record else None

# Get answer from OpenAI's GPT-3 if no match is found in Neo4j
def get_openai_answer(user_question):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",  # You can also try other models like GPT-4
        prompt=user_question,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Chatbot loop
def chatbot():
    stored_questions = fetch_questions()  # Load questions once
    print("Chatbot is ready! Ask me a question (type 'exit' to quit).")
    
    while True:
        user_question = input("You: ")
        if user_question.lower() == "exit":
            break

        # Log the question
        logging.info(f"User asked: {user_question}")
        
        # First try to find a match in Neo4j
        best_match = find_best_match(user_question, stored_questions)
        
        if best_match:
            answer = get_answer(best_match)
            logging.info(f"Bot answered (Neo4j): {answer}")
            print(f"Bot: {answer}")
        else:
            # If no match in Neo4j, use OpenAI LLM to generate an answer
            answer = get_openai_answer(user_question)
            logging.info(f"Bot answered (OpenAI): {answer}")
            print(f"Bot: {answer}")

chatbot()

