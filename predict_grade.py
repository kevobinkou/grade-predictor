from joblib import load

# Load the saved model
model = load('grade_predictor_model.joblib')

print("🎓 Student Grade Prediction")
print("Please enter the following details:")

# Ask the user to input values
try:
    G1 = float(input("G1 (1st period grade): "))
    G2 = float(input("G2 (2nd period grade): "))
    studytime = float(input("Study time (1 to 4): "))
    failures = int(input("Number of past class failures: "))
    absences = int(input("Number of absences: "))

    # Create input sample for prediction
    student_data = [[G1, G2, studytime, failures, absences]]

    # Predict
    predicted_grade = model.predict(student_data)[0]
    print(f"\n📊 Predicted Final Grade (G3): {predicted_grade:.2f}")

    # Optional Feedback
    if predicted_grade >= 10:
        print("✅ Prediction: Likely to pass")
    else:
        print("⚠️ Prediction: At risk of failing")

except ValueError:
    print("❌ Please enter numeric values only.")
