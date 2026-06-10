import pandas as pd
import random

data = []

for i in range(1000):

    attendance = random.randint(50, 100)
    study_hours = random.randint(1, 10)
    assignment_score = random.randint(40, 100)
    previous_marks = random.randint(40, 100)

    final_marks = (
        attendance * 0.25 +
        assignment_score * 0.35 +
        previous_marks * 0.35 +
        study_hours * 0.5
    )

    final_marks = min(round(final_marks), 100)

    data.append([
        attendance,
        study_hours,
        assignment_score,
        previous_marks,
        final_marks
    ])

df = pd.DataFrame(
    data,
    columns=[
        "attendance",
        "study_hours",
        "assignment_score",
        "previous_marks",
        "final_marks"
    ]
)

df.to_csv("dataset/student_data.csv", index=False)

print("Dataset Generated Successfully")