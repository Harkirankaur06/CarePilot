import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load dataset
df = pd.read_csv("Dataset.csv")

# Preprocessing
binary_cols = ["Fever", "Cough", "Fatigue", "Difficulty Breathing"]
df[binary_cols] = df[binary_cols].replace({"Yes": 1, "No": 0})

df["Gender"] = df["Gender"].map({"Male": 0, "Female": 1})
df["Blood Pressure"] = df["Blood Pressure"].map({"Low": 0, "Normal": 1, "High": 2})
df["Cholesterol Level"] = df["Cholesterol Level"].map({"Low": 0, "Normal": 1, "High": 2})

# Features and label
X = df.drop(["Disease", "Outcome Variable"], axis=1)
y = df["Disease"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model and feature order
joblib.dump(clf, "disease_model.pkl")
joblib.dump(X.columns.tolist(), "feature_order.pkl")

print("Model training complete and saved.")
