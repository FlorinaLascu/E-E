import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# Load the pre-trained model and transformer
model = RandomForestRegressor()
transformer = ColumnTransformer([("one_hot", OneHotEncoder(), ["Pozitie", "Limbaj", "Tehnologie", "Framework"])], remainder="passthrough")

def preprocess_input(input_data):
    input_df = pd.DataFrame(input_data, index=[0])
    transformed_input = transformer.transform(input_df)
    return transformed_input

def predict_salary(profession, language, technology, framework, vechime):
    input_data = {"Pozitie": profession, "Limbaj": language, "Tehnologie": technology, "Framework": framework, "Vechime": vechime}
    processed_input = preprocess_input(input_data)
    predicted_salary = model.predict(processed_input)[0]
    return predicted_salary