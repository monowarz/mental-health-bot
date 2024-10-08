# app.py
from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import random

app = Flask(__name__)

# Initialize the chatbot
chatbot = ChatBot("MentalHealthBot")

# Train the chatbot on the English language corpus
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

# List of resources that can be shared with the user
mental_health_resources = [
    {"type": "article", "title": "Understanding Anxiety", "url": "https://www.example.com/anxiety"},
    {"type": "article", "title": "Dealing with Depression", "url": "https://www.example.com/depression"},
    {"type": "professional", "title": "Find a Therapist", "url": "https://www.example.com/find-therapist"},
    {"type": "professional", "title": "Mental Health Hotline", "url": "https://www.example.com/hotline"},
]

# Function to choose a random mental health resource
def get_resource():
    return random.choice(mental_health_resources)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_input = request.form["msg"]
    bot_response = str(chatbot.get_response(user_input))
    
    # If the user input contains a trigger word, provide a resource
    if any(word in user_input.lower() for word in ["help", "depressed", "anxiety", "stress", "therapist"]):
        resource = get_resource()
        return jsonify({"response": bot_response, "resource": resource})
    
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)