from flask import Flask, render_template, request, jsonify, redirect, url_for
import csv
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='template')

@app.route("/")
def hello_world():
    return render_template('test.html')

@app.route("/biodata/")
def amalika_biodata():
    return render_template('biodata.html')

@app.route("/cv/")
def amalika_cv():
    return render_template('cv.html')

@app.route("/portofolio/")
def amalika_port():
    return render_template('portofolio.html')

@app.route("/hobby/")
def amalika_hobby():
    return render_template('hobby.html')

@app.route("/favorites/")
def amalika_fav():
    return render_template('favorites.html')



def fibonacci(n):
    fib_sequence = [1, 1]

    for i in range(n):
        fib_sequence.append(fib_sequence[i] + fib_sequence[i+1])

    return fib_sequence[:n]

@app.route("/fibonacci/", methods=['GET', 'POST'])
def custom_fibonacci_page():
    if request.method == 'POST':
        try:
            n = int(request.form['custom_length'])
            result = fibonacci(n)
            return render_template('fibonacci2.html', custom_length=n, result=result)
        except ValueError:
            error_message = "Masukkan angka valid."
            return render_template('fibonacci2.html', error_message=error_message)

    return render_template('fibonacci2.html')



@app.route("/csv_to_json/", methods=["GET", "POST"])
def csv_to_json():
    if request.method == "POST":
        # Check if the post request has the file part
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]

        # If the user does not select a file, browser sends an empty file without a filename
        if file.filename == "":
            return "No selected file"

        # Check if the file is allowed (optional)
        allowed_extensions = {"csv"}
        if "." not in file.filename or file.filename.rsplit(".", 1)[1].lower() not in allowed_extensions:
            return "Invalid file type. Please upload a CSV file."

        # Save the file to the server
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        # Read the CSV file and convert it to JSON
        json_data = convert_csv_to_json(file_path)

        # Return the JSON response
        return jsonify(json_data)

    return render_template("csv_to_json.html")

def convert_csv_to_json(file_path):
    with open(file_path, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        json_data = [row for row in csv_reader]

    return json_data




@app.route("/form_submit/", methods=["POST"])
def form_submit():
    # Retrieve form data
    name = request.form.get("name")
    age = request.form.get("age")

    # Process the data (you can save it to a database, etc.)
    # For now, just redirect to a thank you page
    return redirect(url_for("thank_you", name=name, age=age))

@app.route("/thank_you/")
def thank_you():
    # Access the submitted data from the URL parameters
    name = request.args.get("name")
    age = request.args.get("age")

    # Render a thank you page
    return f"<h2>Thank you, {name} ({age} years old)!</h2>"


