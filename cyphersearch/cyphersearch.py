import os
import logging
from flask import Flask, request, render_template, flash
from neo4j import GraphDatabase
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Initialize Flask app
app = Flask(__name__)

# Securely set the secret key (use an environment variable)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_secret_key")  # Change "fallback_secret_key" for extra security

# Initialize Neo4j driver
uri = "neo4j+s://demo.neo4jlabs.com:7687"  # Replace with your Neo4j instance URI
username = "recommendations"
password = "recommendations"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Load Flan-T5 model and tokenizer
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")

# Function to generate Cypher query using Flan-T5
def generate_cypher_query(query):
    inputs = tokenizer.encode("Generate a Cypher query to retrieve movies from the database: " + query, return_tensors="pt")
    outputs = model.generate(inputs)
    cypher_query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Generated Cypher Query: {cypher_query}")  # Debugging
    return cypher_query

# Function to execute Cypher query in Neo4j
def execute_query(cypher_query):
    try:
        with driver.session() as session:
            result = session.run(cypher_query)
            return result.data()
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        flash("There was an error executing the Cypher query. Please try again.", "error")
        return []

# Route to display the search form and results
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_query = request.form["query"]
        if not user_query:
            flash("Please enter a query.", "warning")
            return render_template("index.html")

        cypher_query = generate_cypher_query(user_query)
        results = execute_query(cypher_query)

        if not results:
            flash("No results found.", "info")

        return render_template("index.html", results=results)

    return render_template("index.html")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

