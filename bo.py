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

# Symptom to severity + response map
symptom_responses = {
    "headache":      ("mild",     "You might have a headache. Stay hydrated and rest in a quiet space."),
    "nausea":        ("mild",     "Nausea could be from fatigue or stress. Light meals and fluids help."),
    "fatigue":       ("moderate", "Ongoing fatigue might need medical attention. Track your sleep and diet."),
    "cough":         ("moderate", "Is your cough dry or wet? If it lasts more than 3 days, consider a check-up."),
    "fever":         ("moderate", "Monitor your temperature. Over 101°F for more than 24 hrs? Consult a doctor."),
    "shortness of breath": ("severe", "This can be serious. Please seek urgent medical help."),
    "chest pain":    ("severe",   "Chest pain is a red flag. Please go to the emergency room immediately."),
}

# Function for sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  # Range: -1 (negative) to 1 (positive)

# Function to suggest stress-relief techniques
def suggest_stress_relief():
    return random.choice(stress_relief_suggestions)

# Function to handle user input and generate a response
def custom_response(user_input):
    input_lower = user_input.lower()
    matched = []

    for keyword, (severity, response) in symptom_responses.items():
        if keyword in input_lower:
            matched.append(f"[{severity.upper()}] {response}")

    if matched:
        return " ".join(matched)

    sentiment = analyze_sentiment(user_input)
    if sentiment < 0:
        return suggest_stress_relief()

    return "I'm here to help. Please tell me more about what you're feeling."

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
    print(f"Bo: {response}")
