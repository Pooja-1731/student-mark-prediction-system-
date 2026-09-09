import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# Load dataset
data = pd.read_csv("student_marks.csv")

# Input features
X = data[[
    "attendance",
    "assignment_marks",
    "previous_exam_marks"
]]

# Target
y = data["final_marks"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create model
model = LinearRegression()

# Train model
model.fit(X_train, y_train)

# Save model
with open("student_marks_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model trained successfully!")
print("Model saved as student_marks_model.pkl")