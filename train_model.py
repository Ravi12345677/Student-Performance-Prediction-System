import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

data = pd.read_csv("dataset/student_data.csv")

X = data[['attendance',
          'study_hours',
          'assignment_score',
          'previous_marks']]

y = data['final_marks']

model = RandomForestRegressor()
model.fit(X, y)

pickle.dump(model,
            open('models/student_model.pkl', 'wb'))

print("Model Trained Successfully")