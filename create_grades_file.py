import pandas as pd

# Sample student data
data = {
    "hours_studied": [2, 4, 6, 8, 10],
    "attendance": [60, 70, 80, 90, 100],
    "previous_grade": [50, 60, 65, 70, 75],
    "final_grade": [55, 63, 70, 78, 85]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("grades.csv", index=False)

print("✅ Sample grades.csv file has been created in the current folder.")
