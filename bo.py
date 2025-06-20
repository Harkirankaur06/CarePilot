import nltk
from nltk.chat.util import Chat, reflections
import requests
from spellchecker import SpellChecker
from textblob import TextBlob
import random

# Download NLTK data
nltk.download('punkt')

# Function to make API requests to Gemini (commented out since we don't have access)
# def gemini_request(user_input):
#     headers = {
#         'Authorization': f'Bearer {API_KEY}',
#         'Content-Type': 'application/json'
#     }
#     data = {"message": user_input}
#     response = requests.post(GEMINI_API_URL, json=data, headers=headers)
#     return response.json()

# Spell checker
spell = SpellChecker()

# Predefined stress-relief suggestions
stress_relief_suggestions = [
    "Try taking deep breaths for a few minutes.",
    "Consider going for a short walk outside.",
    "Practice mindfulness or meditation.",
    "Listen to your favorite music to lift your spirits.",
    "Write down your feelings in a journal.",
    "Engage in physical activities like stretching or yoga.",
    "Talk to someone you trust about how you feel."
]

# Function for sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  # Range: -1 (negative) to 1 (positive)

# Function to suggest stress-relief techniques
def suggest_stress_relief():
    return random.choice(stress_relief_suggestions)

# Function to handle user input and generate a response
def custom_response(user_input):
    # Check sentiment
    sentiment = analyze_sentiment(user_input)
    
    # If the sentiment is negative (indicating stress)
    if sentiment < 0:
        return suggest_stress_relief()
    
    # Fallback response if no specific pattern matched
    return "I'm here to help. Please share more about how you're feeling."

# Create Chatbot
pairs = [
    [r"(.*)", ["Let me check that for you...",]]
]

chatbot = Chat(pairs, reflections)

# Start conversation
print("Hi, I'm here to help. Type 'quit' to exit the chat.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        print("Goodbye! Take care!")
        break

    # Correct typos
    corrected_input = ' '.join([spell.candidates(word).pop() if spell.candidates(word) else word for word in user_input.split()])
    
    response = custom_response(corrected_input)
    print(f"Bot: {response}")
