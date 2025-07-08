import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from joblib import dump  # for saving the model

# Load the dataset
df = pd.read_csv("student-mat.csv", sep=";")

# Choose features (inputs) and label (output)
features = ['G1', 'G2', 'studytime', 'failures', 'absences']
label = 'G3'  # Final grade

# Split into X (inputs) and y (output)
X = df[features]
y = df[label]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the trained model to a file
dump(model, 'grade_predictor_model.joblib')
print("✅ Model trained and saved successfully!")
from joblib import dump

# Save the trained model to file
dump(model, 'grade_predictor_model.joblib')
print("✅ Model saved as grade_predictor_model.joblib")
