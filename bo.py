import nltk
from nltk.chat.util import Chat, reflections
from spellchecker import SpellChecker
from textblob import TextBlob
import random
import os

# Download once only (optional: you can preload in build step instead)
nltk.download('punkt', quiet=True)

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
    "headache": ("mild", "You might have a headache. Stay hydrated and rest in a quiet space."),
    "nausea": ("mild", "Nausea could be from fatigue or stress. Light meals and fluids help."),
    "fatigue": ("moderate", "Ongoing fatigue might need medical attention. Track your sleep and diet."),
    "cough": ("moderate", "Is your cough dry or wet? If it lasts more than 3 days, consider a check-up."),
    "fever": ("moderate", "Monitor your temperature. Over 101°F for more than 24 hrs? Consult a doctor."),
    "shortness of breath": ("severe", "This can be serious. Please seek urgent medical help."),
    "chest pain": ("severe", "Chest pain is a red flag. Please go to the emergency room immediately."),
}

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def suggest_stress_relief():
    return random.choice(stress_relief_suggestions)

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
