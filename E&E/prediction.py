import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor

# Read the data
predict_info = pd.read_csv("E&EPredict.csv", sep=";")

# Split the data into x/y
x = predict_info.drop("Salariu", axis=1)
y = predict_info["Salariu"]

# Split into training and test set
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Build a column transformer for one-hot encoding
categorical_features = ["Pozitie", "Limbaj", "Tehnologie", "Framework"]
numeric_features = ["Vechime"]
one_hot = OneHotEncoder(handle_unknown='ignore')
transformer = ColumnTransformer([
    ("one_hot", one_hot, categorical_features),
], remainder="passthrough")

# Fit and transform on the training set
x_train_transformed = transformer.fit_transform(x_train)

# Transform the test set
x_test_transformed = transformer.transform(x_test)

# Build machine learning model
model = RandomForestRegressor()
model.fit(x_train_transformed, y_train)
score = model.score(x_test_transformed, y_test)

# Print the initial model score
print("Initial Model Score:", score)

# Refit the model on new training data (for demonstration purposes, using the same data)
x_train_new, x_test_new, y_train_new, y_test_new = train_test_split(x, y, test_size=0.2, random_state=42)
x_train_transformed_new = transformer.transform(x_train_new)
model.fit(x_train_transformed_new, y_train_new)

# Evaluate the model on the new test set
score_new = model.score(transformer.transform(x_test_new), y_test_new)

# Print the refitted model score
print("Refitted Model Score:", score_new)