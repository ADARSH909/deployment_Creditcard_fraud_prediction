from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import json


# Load the trained model
model = joblib.load("model.pkl")

# Load the column names
# with open("columns.json", "r") as f:
#     columns = json.load(f)

with open('columns.json', 'r') as f:
    columns = json.load(f)['data_columns']
print(columns)





# Create the Flask app
app = Flask(__name__)

# Define the home page
@app.route("/")
def home():
    return render_template("index.html")

# Define the predict page
@app.route("/predict", methods=["POST"])
def predict():
    # Get the data from the POST request
    data = request.form.to_dict()

    # Create a DataFrame from the data
    df = pd.DataFrame(data, index=[0])

    # Reorder the columns to match the model
    df = df[columns]
    

    # Make the prediction
    prediction = model.predict(df)[0]
    # Determine if the transaction is fraudulent or not
    if prediction == 0:
        result = "Not Fraud Transaction"
    else:
        result = "Fraud Transaction"

    # Return the result as JSON
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run()
