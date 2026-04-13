import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.linear_model import LogisticRegression

# Load dataset
data = pd.read_csv("dataset/resume_job_dataset.csv")

# Combine text
data["combined"] = data["resume"] + " " + data["job"]

X = data["combined"]
y = data["match"]

# Vectorization
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.3, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, predictions))
print("Classification Report:\n", classification_report(y_test, predictions))

# Save model
joblib.dump(model, "resume_model.pkl")
joblib.dump(vectorizer, "resume_vectorizer.pkl")

print("✅ Model trained and saved successfully")
