import nltk
from nltk.chat.util import Chat, reflections
from spellchecker import SpellChecker
from textblob import TextBlob
import random
import os
import joblib
import pandas as pd

# Load model and feature order
model = joblib.load("disease_model.pkl")
feature_order = joblib.load("feature_order.pkl")

# Mapping dictionaries
gender_map = {"male": 0, "female": 1}
binary_map = {"yes": 1, "no": 0}
bp_map = {"low": 0, "normal": 1, "high": 2}
chol_map = {"low": 0, "normal": 1, "high": 2}
def predict_disease_from_text(text):
    try:
        # Example expected input:
        # "Gender: Female, Age: 40, Fever: Yes, Cough: Yes, Fatigue: No, Difficulty Breathing: No, Blood Pressure: Normal, Cholesterol Level: High"
        input_dict = {}
        for item in text.split(","):
            key, value = item.split(":")
            input_dict[key.strip().lower()] = value.strip().lower()

        # Convert to model input
        data = {
            "Gender": gender_map.get(input_dict.get("gender"), 0),
            "Age": int(input_dict.get("age", 0)),
            "Fever": binary_map.get(input_dict.get("fever"), 0),
            "Cough": binary_map.get(input_dict.get("cough"), 0),
            "Fatigue": binary_map.get(input_dict.get("fatigue"), 0),
            "Difficulty Breathing": binary_map.get(input_dict.get("difficulty breathing"), 0),
            "Blood Pressure": bp_map.get(input_dict.get("blood pressure"), 1),
            "Cholesterol Level": chol_map.get(input_dict.get("cholesterol level"), 1),
        }

        df = pd.DataFrame([data])[feature_order]
        prediction = model.predict(df)[0]

        return f"Based on your symptoms, the predicted disease is: **{prediction}**."

    except Exception as e:
        return f"Sorry, I couldn't process your input. Error: {str(e)}"


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
