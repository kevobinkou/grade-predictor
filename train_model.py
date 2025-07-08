import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from joblib import dump

# Step 1: Load the dataset
df = pd.read_csv("grades.csv")

# Step 2: Define input features and target variable
X = df[["hours_studied", "attendance", "previous_grade"]]
y = df["final_grade"]

# Step 3: Split into training and testing sets (for better practice)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 5: Save the trained model
dump(model, "grade_predictor_model.joblib")

print("✅ Model trained and saved as grade_predictor_model.joblib")
